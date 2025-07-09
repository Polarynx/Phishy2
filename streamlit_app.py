import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_check(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cybersecurity assistant. Analyze email or message content and determine if it is a phishing attempt."},
                {"role": "user", "content": f"Is this message a phishing attempt? Give a clear YES or NO answer, and explain why:\n\n{text}"}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error with GPT API: {str(e)}"

st.set_page_config(page_title="PhishyWeb", page_icon="🐟")
st.title("🐟 PhishyWeb: Phishing Message Detector")

input_text = st.text_area("Paste a suspicious email or message here:", height=250)

if st.button("🔍 Analyze"):
    if not input_text.strip():
        st.warning("Please enter a message before analyzing.")
    else:
        with st.spinner("Analyzing with AI..."):
            result = gpt_check(input_text)
            st.subheader("🧠 GPT Analysis")
            st.info(result)
