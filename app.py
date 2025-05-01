import streamlit as st
from openai import OpenAI
import openai
import time

# Setup
st.set_page_config(page_title="EMO – Emotional Resilience Roleplay", layout="centered")
st.title("EMO – Emotional Resilience Roleplay 🌱")
st.markdown("**Explore your emotions and discover personalized action plans for emotional resilience.**")

# GPT-4o client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Track last submission to prevent spam clicks
if "last_submit_time" not in st.session_state:
    st.session_state.last_submit_time = 0

# Emotional scenarios
scenarios = {
    "You were rejected from a dream opportunity.": [
        "Blame yourself and feel worthless",
        "Reflect on what you learned",
        "Try to numb the pain through distraction",
        "Talk to someone you trust"
    ],
    "A friend betrayed your trust.": [
        "Cut them off immediately",
        "Talk to them openly",
        "Hold the grudge quietly",
        "Reflect on your own feelings first"
    ],
    "You made a mistake in front of others.": [
        "Hide and avoid everyone",
        "Laugh it off and move on",
        "Replay it constantly in your head",
        "Ask for feedback to improve"
    ]
}

# User input
scenario = st.selectbox("Choose a scenario to explore:", list(scenarios.keys()))
user_choice = st.radio("What would you do?", scenarios[scenario])

# Submission
if st.button("Submit"):
    now = time.time()
    if now - st.session_state.last_submit_time < 30:
        st.warning("⏱ Please wait a few seconds before submitting again.")
    else:
        st.session_state.last_submit_time = now
        with st.spinner("Creating your personalized resilience plan..."):
            prompt = f"""
You are a licensed CBT therapist AI. A user has shared the following emotional situation:

Scenario: "{scenario}"
User's response: "{user_choice}"

Give a personalized emotional resilience strategy in the format of an action plan that is simple and easy to follow.
Structure your response like this:

1. **Understand the Emotion**: (Briefly explain what emotion the user is likely feeling and why)
2. **Cognitive Reframe**: (How can the user reframe their negative thought?)
3. **Behavioral Action**: (A specific, simple step the user can take today)
4. **Self-Compassion Reminder**: (End with a gentle, encouraging statement to build emotional resilience)
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.subheader("🧭 EMO's Action Plan for You")
                st.markdown(response.choices[0].message.content)

            except openai.RateLimitError:
                st.error("⚠️ Too many requests. Please wait a bit and try again.")

            except Exception as e:
                st.error(f"🚨 An unexpected error occurred: {str(e)}")
