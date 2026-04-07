import streamlit as st
import requests

st.set_page_config(page_title="Jarvis Multi-Agent", page_icon="🤖")
st.title("🤖 Jarvis AI Orchestrator")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask Jarvis to manage your life..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call your FastAPI backend
    with st.spinner("Agents are thinking..."):
        try:
            response = requests.post(
                "http://localhost:8000/query",
                json={"query": prompt, "user_id": "user_streamlit"}
            )
            data = response.json()
            
            ai_response = data["final_response"]
            
            # Show what the agents did in an expander
            with st.expander("🔍 See Agent Trace"):
                st.json(data["logs"])

            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")
