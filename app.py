import streamlit as st
from openai import OpenAI
import openai
import time

# Page setup
st.set_page_config(page_title="EMO – Emotional Resilience Roleplay", layout="centered")
st.title("EMO – Emotional Resilience Roleplay 🌱")
st.markdown("**Explore your emotions and receive personalized CBT-based action plans.**")

# Step 1: Email login and approval check
email = st.text_input("Enter your email to request access:")

# Load approved users (preferred: use Streamlit secrets)
approved_emails = st.secrets.get("approved_emails", [])

# Approval-first logic
if email and email not in approved_emails:
    st.warning("🚫 You are not yet approved to use this app.")
    st.info("📧 Please contact the administrator at your-email@example.com to request access.")
    
    # Optional: Log the request
    with open("access_requests.txt", "a") as f:
        f.write(f"{email}\n")
    st.stop()

if not email:
    st.stop()

# GPT-4o client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize cooldown
if "last_submit_time" not in st.session_state:
    st.session_state.last_submit_time = 0

# Roleplay scenarios
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

# User selects scenario and choice
scenario = st.selectbox("Choose a scenario to explore:", list(scenarios.keys()))
user_choice = st.radio("What would you do?", scenarios[scenario])

# Submission block
if st.button("Submit"):
    now = time.time()
    if now - st.session_state.last_submit_time < 30:
        st.warning("⏱ Please wait a few seconds before submitting again.")
    else:
        st.session_state.last_submit_time = now
        with st.spinner("Creating your personalized action plan..."):
            prompt = f"""
You are a licensed CBT therapist AI. A user has shared the following emotional situation:

Scenario: "{scenario}"
User's response: "{user_choice}"

Create a personalized emotional resilience strategy in this structure:

1. **Understand the Emotion**: Briefly explain what the user is likely feeling and why.
2. **Cognitive Reframe**: Help the user rethink the situation in a healthier way.
3. **Behavioral Action**: Recommend one small action they can take today.
4. **Self-Compassion Reminder**: End with a gentle, affirming message.
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.subheader("🧭 EMO's Personalized Action Plan")
                st.markdown(response.choices[0].message.content)

            except openai.RateLimitError:
                st.error("⚠️ Too many requests. Please wait and try again.")
            except Exception as e:
                st.error(f"🚨 Unexpected error: {str(e)}")
