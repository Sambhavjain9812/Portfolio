# Fitness Routine Bot

## Overview
This project is a **Fitness Routine Bot** built using **Streamlit**, **LangGraph**, and **Google Gemini API**. It generates personalized **workout** and **diet plans** based on user input and allows users to track their progress.

## Features
- **User Profile Setup**: Collects fitness goals, age, weight, height, activity level, and preferences.
- **Workout Plan Generator**: Uses Google Gemini API to create a customized weekly workout routine.
- **Diet Plan Generator**: Generates a personalized meal plan based on user preferences.
- **Daily Progress Tracker**: Allows users to log workouts, diet, and weight changes.
- **Interactive Flow**: Implements a multi-step flow using **LangGraph** to guide users through the fitness routine setup.

## Tech Stack
- **Python**
- **Streamlit** (for UI)
- **LangGraph** (for workflow management)
- **Google Gemini API** (for AI-powered plan generation)
- **dotenv** (for environment variable management)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/fitness-bot.git
cd fitness-bot
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up API Key
Create a `.env` file and add your **Google Gemini API key**:
```sh
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the App
```sh
streamlit run app.py
```

## Usage
1. **Enter Your Profile Details**
   - Choose a fitness goal (Weight Loss, Muscle Gain, etc.)
   - Provide age, weight, height, activity level, and preferences.
   
2. **Get Your Personalized Workout Plan**
   - AI generates a structured weekly workout routine.
   
3. **Receive a Custom Diet Plan**
   - AI suggests a meal plan based on user inputs.
   
4. **Track Your Progress**
   - Log workouts, diet, and weight changes daily.
   
## Live Demo
[Click here to try the Fitness Routine Bot](https://portfolio-tdhpjodtnkodz5hzz6hnrg.streamlit.app/)

## File Structure
```
fitness-bot/
│── app.py             # Main Streamlit app
│── requirements.txt   # Required dependencies
│── .env               # API Key storage (ignored in Git)
│── README.md          # Project documentation
```



