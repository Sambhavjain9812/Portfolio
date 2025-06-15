import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import json
from typing import List, Dict
import time
import asyncio
from textblob import TextBlob

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Punjabi": "pa",
    "Hindi": "hi",
    "Tamil": "ta",
    "Bengali": "bn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Himachali/Pahadi": "hi",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Odia": "or"
}

TONE_OPTIONS = {
    "Formal": "Use polite and professional language.",
    "Neutral": "Use a balanced and natural tone.",
    "Informal": "Use casual and conversational language."
}

class TranslationManager:
    def __init__(self):
        self.chunk_size = 1500
        self.overlap_size = 200
        self.context_window = []
    
    def detect_language(self, text: str) -> str:
        """Auto-detect the language of input text."""
        try:
            detected_lang = TextBlob(text).detect_language()
            return detected_lang
        except:
            return "en"
    
    def chunk_text_with_context(self, text: str) -> List[Dict]:
        """Split text into chunks while maintaining context"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for i, word in enumerate(words):
            current_chunk.append(word)
            current_length += len(word) + 1
            
            if current_length >= self.chunk_size:
                overlap_words = words[i+1:i+1+self.overlap_size] if i+1 < len(words) else []
                
                chunks.append({
                    'main_text': ' '.join(current_chunk),
                    'overlap_text': ' '.join(overlap_words),
                    'position': len(chunks)
                })
                
                current_chunk = words[max(0, i-50):i+1]
                current_length = sum(len(w) + 1 for w in current_chunk)
        
        if current_chunk:
            chunks.append({
                'main_text': ' '.join(current_chunk),
                'overlap_text': '',
                'position': len(chunks)
            })
        
        return chunks
    
    def create_translation_prompt(self, chunk: Dict, mode: str, target_language: str, tone: str, domain: str = None) -> str:
        """Create appropriate prompt based on translation mode and tone"""
        tone_instruction = TONE_OPTIONS.get(tone, "Use natural language.")
        
        if mode == "normal":
            prompt = f"""Translate the following text to {target_language}.
            Apply the tone: {tone_instruction}
            
            Text: {chunk['main_text']}"""
        else:  # contextual
            context = f"Domain: {domain}\n" if domain else ""
            previous_context = self.context_window[-1] if self.context_window else ""
            
            prompt = f"""Perform a contextual translation to {target_language}.
            {context}
            Previous context: {previous_context}
            Apply the tone: {tone_instruction}
            
            Text to translate: {chunk['main_text']}"""
        
        return prompt
    
    def translate_chunk(self, chunk: Dict, mode: str, target_language: str, tone: str, domain: str = None) -> str:
        """Translate a single chunk of text and stream output."""
        prompt = self.create_translation_prompt(chunk, mode, target_language, tone, domain)
        
        try:
            completion = client.chat.completions.create(
                model="Gemma2-9b-It",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3 if mode == "normal" else 0.4,
                max_tokens=2048,
                top_p=1,
                stream=True,
            )

            translation = ""
            for chunk_response in completion:
                part = chunk_response.choices[0].delta.content or ""
                translation += part
                st.write(part, end="")  # Stream output in real-time

            if mode == "contextual":
                self.context_window.append(translation)
                if len(self.context_window) > 5:
                    self.context_window.pop(0)

            return translation
        except Exception as e:
            st.error(f"Translation failed: {e}")
            return ""

async def translate_chunks_async(chunks, mode, target_language, tone):
    """Perform async batch translation of text chunks."""
    tasks = [asyncio.to_thread(st.session_state.translation_manager.translate_chunk, chunk, mode, target_language, tone) for chunk in chunks]
    return await asyncio.gather(*tasks)

async def handle_translation(input_text, translation_mode, target_language, tone):
    """Handle full translation process asynchronously."""
    chunks = st.session_state.translation_manager.chunk_text_with_context(input_text)
    translated_chunks = await translate_chunks_async(chunks, translation_mode.lower(), target_language, tone)
    return " ".join(translated_chunks)

def main():
    st.set_page_config(page_title="  Advanced Smart Translator", layout="wide")
    
    if 'translation_manager' not in st.session_state:
        st.session_state.translation_manager = TranslationManager()
    
    st.title("  Advanced Smart Translator")

    with st.expander("  Translation Settings", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            translation_mode = st.radio("Translation Mode", ["Normal", "Contextual"])
        with col2:
            target_language = st.selectbox("Select Target Language", list(SUPPORTED_LANGUAGES.keys()))
        with col3:
            tone = st.selectbox("Select Translation Tone", list(TONE_OPTIONS.keys()))

    st.subheader("  Enter Text for Translation")
    input_text = st.text_area("Enter text:", height=200)

    if input_text:
        detected_lang = st.session_state.translation_manager.detect_language(input_text)
        st.write(f"  Detected Language: {detected_lang}")

    if st.button("  Translate"):
        if not input_text:
            st.error("Please enter some text.")
            return
        
        final_translation = asyncio.run(handle_translation(input_text, translation_mode, target_language, tone))
        
        st.subheader(f" {target_language} Translation")
        st.write(final_translation)

        # Provide download option
        if final_translation:
            st.download_button(
                label="Download Translation",
                data=final_translation,
                file_name=f"translated_text_{target_language}.txt",
                mime="text/plain",
            )

if __name__ == "__main__":
    main()

