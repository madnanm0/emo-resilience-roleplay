import streamlit as st
from openai import OpenAI
import openai
import time
import os

st.set_page_config(page_title="EMO – Emotional Resilience Roleplay", layout="centered")
st.title("EMO – Emotional Resilience Roleplay 🌱")

# Step 1: Get user email
email = st.text_input("Enter your email to request access:")

# ✅ APPROVED USERS (hardcoded list OR load from secrets)
approved_emails = ["your.email@example.com", "team.member@gmail.com"]

# ✅ If user is not approved yet
if email and email not in approved_emails:
    st.warning("🚫 You are not yet approved to use this app.")
    st.info("📧 Please contact the administrator at mr.adnan.manzor@gamil.com to request access.")

    # Log unapproved emails to a text file (one-time entry)
    log_file = "access_requests.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            requested = f.read().splitlines()
    else:
        requested = []

    if email not in requested:
        with open(log_file, "a") as f:
            f.write(email + "\n")

    st.stop()

# ✅ If no email entered at all
if not email:
    st.info("Please enter your email to continue.")
    st.stop()
