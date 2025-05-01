import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="EMO – Emotional Resilience Roleplay", layout="centered")

st.title("EMO – Emotional Resilience Roleplay 🌱")
st.markdown("**Helping you build emotional strength through AI-powered storytelling.**")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

scenario = st.selectbox("Choose a scenario to explore:", list(scenarios.keys()))
user_choice = st.radio("What would you do?", scenarios[scenario])

if st.button("Submit"):
    with st.spinner("Processing your emotional journey..."):
        prompt = f"""
You are a compassionate CBT therapist AI.
Scenario: "{scenario}"
User's choice: "{user_choice}"
Respond with empathy, explain the likely emotion, and suggest one CBT-based coping strategy.
"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.subheader("🧠 EMO's Reflection")
        st.write(response.choices[0].message.content)
