import streamlit as st
import requests
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import ollama

# ---------------------- BACKEND CODE ---------------------- #
class ChatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                # Parse incoming JSON data
                request_json = json.loads(post_data.decode('utf-8'))
                user_message = request_json.get("message", "")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_data = {"error": f"Invalid JSON: {e}"}
                self.wfile.write(json.dumps(error_data).encode())
                return

            # Get AI response from Ollama
            try:
                response = ollama.chat(model="phi", messages=[{"role": "user", "content": user_message}])
                ai_reply = response.get("message", "No response from AI")
            except Exception as e:
                ai_reply = f"Error calling Ollama: {e}"

            # Send JSON response back
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_data = {"response": ai_reply}
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_error(404, "Endpoint not found")

def run_backend_server():
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, ChatHandler)
    print("Backend server running on http://127.0.0.1:8000")
    httpd.serve_forever()

# Start the backend server in a separate thread
backend_thread = threading.Thread(target=run_backend_server, daemon=True)
backend_thread.start()

# Wait briefly to ensure the backend is up
time.sleep(2)

# ---------------------- FRONTEND CODE ---------------------- #

st.set_page_config(page_title="Ollama AI Chatbot", layout="centered")

st.markdown("""
    <style>
    .chat-container { max-width: 600px; margin: auto; }
    .user-message { background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: left; }
    .ai-message { background-color: #EAEAEA; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: left; }
    .stTextInput, .stButton > button { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🤖 Ollama AI Chatbot</h1>", unsafe_allow_html=True)

# Initialize session state for messages if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display the chat conversation
with st.container():
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-message'>{msg['content']}</div>", unsafe_allow_html=True)

# Input box for user message
user_input = st.text_input("Type your message:", "")

if st.button("Send") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    try:
        # Send POST request to backend endpoint /chat
        r = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
        r_json = r.json()
        ai_reply = r_json.get("response", "No response from backend.")
    except Exception as e:
        ai_reply = f"Error connecting to backend: {e}"
    st.session_state["messages"].append({"role": "ai", "content": ai_reply})
    st.rerun()  # ✅ FIX: Using st.rerun() instead of st.experimental_rerun()
