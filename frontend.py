import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Update if deployed

st.set_page_config(page_title="AI Customer Support", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #f5f7fa; }
    .title { text-align: center; color: #4CAF50; font-size: 36px; font-weight: bold; }
    .subheader { text-align: center; font-size: 18px; color: #666; }
    .stButton > button { width: 100%; background-color: #4CAF50; color: white; border-radius: 8px; }
    .stTextInput, .stTextArea { border-radius: 10px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p class='title'>💡 AI Customer Support</p>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>AI-driven ticket summarization, routing, and resolution system.</p>", unsafe_allow_html=True)

# --- Input ---
ticket_text = st.text_area("📝 Enter Customer Query", height=150)

if st.button("Process Ticket 🚀"):
    with st.spinner("Analyzing..."):
        try:
            # --- API Calls ---
            summary_response = requests.post(f"{API_URL}/summarize", json={"text": ticket_text})
            summary = summary_response.json().get("summary", "No summary available")

            team_response = requests.post(f"{API_URL}/route", json={"text": ticket_text})
            team = team_response.json().get("assigned_team", "No team assigned")

            recommendation_response = requests.post(f"{API_URL}/recommend", json={"text": ticket_text})
            recommendation = recommendation_response.json().get("recommendation", "No recommendation available")

            time_estimate_response = requests.post(f"{API_URL}/estimate-time", json={"text": ticket_text})
            time_estimate = time_estimate_response.json().get("resolution_time", "No time estimate available")

            # --- Display Results ---
            st.success("✅ Ticket Processed!")
            st.subheader("📌 Summary:")
            st.info(summary)

            st.subheader("🛠 Assigned Team:")
            st.success(team)

            st.subheader("💡 Suggested Resolution:")
            st.warning(recommendation)

            st.subheader("⏳ Estimated Resolution Time:")
            st.error(time_estimate)

        except requests.exceptions.RequestException as e:
            st.error(f"❌ API request failed: {e}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")

st.markdown("---")
st.markdown("💻 Built for a Hackathon | ⚡ Powered by **Ollama + FastAPI + Streamlit**")