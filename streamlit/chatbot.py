import streamlit as st
import requests

st.title("RAG Chatbot (Holistic Health Expert)")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.text_input("You:", "", key="input")

if st.button("Send") and user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    try:
        response = requests.post(
            "http://localhost:8000/rag-query",
            json={"query": user_input},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state['messages'].append({
                "role": "bot",
                "content": data.get("answer", "No answer returned."),
                "reasoning": data.get("reasoning", "")
            })
        else:
            st.session_state['messages'].append({
                "role": "bot",
                "content": f"Error: {response.text}",
                "reasoning": ""
            })
    except Exception as e:
        st.session_state['messages'].append({
            "role": "bot",
            "content": f"Exception: {str(e)}",
            "reasoning": ""
        })

for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
        if msg.get('reasoning'):
            with st.expander("Show reasoning"):
                st.write(msg['reasoning']) 