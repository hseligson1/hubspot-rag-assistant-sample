import streamlit as st
import requests

st.set_page_config(page_title="HubSpot Assistant", page_icon="🤖")

st.title("🤖 HubSpot Docs Assistant")
st.markdown("Ask any question based on the [HubSpot developer docs](https://developers.hubspot.com/docs/llms-full.txt)")

# Input from user
user_question = st.text_input("Enter your question here:")

if st.button("Ask") and user_question:
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:8000/ask",  # Backend must be running
            json={"question": user_question}
        )
        if response.status_code == 200:
            data = response.json()
            st.markdown("### ✅ Answer")
            st.write(data["answer"])
            
            st.markdown("---")
            st.markdown("### 📚 Sources")
            for i, src in enumerate(data["sources"], 1):
                st.markdown(f"**{i}.** {src}")
        else:
            st.error("❌ Error: Could not get a response from the backend.")
