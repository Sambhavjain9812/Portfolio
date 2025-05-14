import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

from google.generativeai import GenerativeModel, configure
import streamlit as st
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Ensure that the API key exists
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Set it in your environment please.")
    st.stop()

configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-2.0-flash')

def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Define the state shape for the graph
class GraphState(TypedDict):
    user_data: dict
    progress: dict

def user_input_node(state: GraphState):
    st.header("User Profile Setup")
    goal = st.selectbox("Fitness Goal", 
                         ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility"], 
                         key="goal_select")
    age = st.number_input("Age", min_value=10, max_value=100, step=1, key="age_input")
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, step=1, key="weight_input")
    height = st.number_input("Height (cm)", min_value=100, max_value=250, step=1, key="height_input")
    activity_level = st.selectbox("Activity Level", 
                                  ["Sedentary", "Moderate", "Active", "Overly Active"], 
                                  key="activity_select")
    preferences = st.text_area("Dietary/Workout Preferences", key="preferences_area")

    if st.button("Submit Profile", key="submit_profile"):
        user_data = {
            "goal": goal,
            "age": age,
            "weight": weight,
            "height": height,
            "activity_level": activity_level,
            "preferences": preferences,
        }
        state["user_data"] = user_data
        st.session_state["graph_state"] = state
        return {"user_data": user_data, "progress": {}}
    return state

# def workout_plan_node(state: GraphState):
#     st.header("Workout Plan")
#     if not state.get("user_data"):
#         st.write("Please submit your profile first.")
#         return state

#     user_data = state["user_data"]
#     prompt = (f"Generate a workout plan for: Goal: {user_data['goal']}, "
#               f"Level: {user_data['activity_level']}, Preferences: {user_data['preferences']}")
#     workout_plan = generate_response(prompt)
#     st.write(workout_plan)
#     if st.button("Next: Diet Plan", key="next_diet_plan"):
#         return state
#     return state

# def diet_plan_node(state: GraphState):
#     st.header("Diet Plan")
#     if not state.get("user_data"):
#         st.write("Please submit your profile first.")
#         return state

#     user_data = state["user_data"]
#     prompt = (f"Generate a diet plan for: Goal: {user_data['goal']}, "
#               f"Level: {user_data['activity_level']}, Preferences: {user_data['preferences']}")
#     diet_plan = generate_response(prompt)
#     st.write(diet_plan)
#     if st.button("Next: Track Progress", key="next_track_progress"):
#         return state
#     return state

def workout_plan_node(state: GraphState):
    st.header("Workout Plan")
    if not state.get("user_data"):
        st.write("Please submit your profile first.")
        return state

    user_data = state["user_data"]
    # Improved prompt with more context, user data, timeframe, and output formatting instructions.
    prompt = (
        f"You are a professional fitness trainer. "
        f"Generate a detailed weekly workout plan for a person whose goal is {user_data['goal'].lower()}. "
        f"User profile details: Age: {user_data['age']} years, Weight: {user_data['weight']} kg, "
        f"Height: {user_data['height']} cm, Activity Level: {user_data['activity_level']}. "
        f"Additional preferences: {user_data['preferences'] if user_data['preferences'] else 'None'}. "
        "Include a warm-up, detailed exercise descriptions with sets, reps, and rest intervals, and a cool-down routine. "
        "Present the plan in clear bullet points or as a day-by-day schedule. in short paragraphs."
    )
    workout_plan = generate_response(prompt)
    st.write(workout_plan)
    if st.button("Next: Diet Plan", key="next_diet_plan"):
        return state
    return state


def diet_plan_node(state: GraphState):
    st.header("Diet Plan")
    if not state.get("user_data"):
        st.write("Please submit your profile first.")
        return state

    user_data = state["user_data"]
    # Improved prompt with a nutrition expert persona, detailed user data, and instructions for formatting the meal plan.
    prompt = (
        f"You are a certified nutritionist. "
        f"Generate a detailed weekly diet plan for a person with the following profile: "
        f"Goal: {user_data['goal'].lower()}, Age: {user_data['age']} years, Weight: {user_data['weight']} kg, "
        f"Height: {user_data['height']} cm, Activity Level: {user_data['activity_level']}. "
        f"Additional dietary/workout preferences: {user_data['preferences'] if user_data['preferences'] else 'None'}. "
        "Include meal options for breakfast, lunch, dinner, and snacks for each day of the week, "
        "ensuring balanced nutrition, portion sizes, and approximate caloric values where appropriate. "
        "Format the plan in a clear, organized manner with headers for each day. in short"
    )
    diet_plan = generate_response(prompt)
    st.write(diet_plan)
    if st.button("Next: Track Progress", key="next_track_progress"):
        return state
    return state


def tracker_node(state: GraphState):
    st.header("Daily Progress Tracker")
    workout_log = st.text_area("Workout Log (Optional)", key="workout_log_area")
    diet_log = st.text_area("Diet Log (Optional)", key="diet_log_area")
    weight_change = st.text_input("Weight Change (Optional)", key="weight_change_input")

    if st.button("Log Progress", key="log_progress"):
        progress = {
            "workout_log": workout_log,
            "diet_log": diet_log,
            "weight_change": weight_change,
        }
        state["progress"] = progress
        st.session_state["graph_state"] = state
        return {"progress": progress, "user_data": state.get("user_data", {})}
    # Optional restart button for starting over
    if st.button("Restart", key="restart"):
        new_state = {"user_data": {}, "progress": {}}
        st.session_state["graph_state"] = new_state
        return new_state
    return state

# Build the graph without the question node
graph = StateGraph(GraphState)
graph.add_node("user_input", user_input_node)
graph.add_node("workout_plan", workout_plan_node)
graph.add_node("diet_plan", diet_plan_node)
graph.add_node("tracker", tracker_node)

graph.add_edge("user_input", "workout_plan")
graph.add_edge("workout_plan", "diet_plan")
graph.add_edge("diet_plan", "tracker")
graph.set_entry_point("user_input")

app = graph.compile()

if "graph_state" not in st.session_state:
    st.session_state["graph_state"] = {"user_data": {}, "progress": {}}

state: GraphState = st.session_state["graph_state"]

for output in app.stream(state):
    for key, value in output.items():
        if key == "__end__":
            continue
        state.update(value)
    st.session_state["graph_state"] = state
