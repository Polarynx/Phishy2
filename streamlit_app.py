import streamlit as st
from openai import OpenAI


# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to send email content to GPT for phishing evaluation
def gpt_check(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity assistant. Analyze email or message content and determine if it is a phishing attempt."
                },
                {
                    "role": "user",
                    "content": f"Is this message a phishing attempt? Give a clear YES or NO answer, and explain why:\n\n{text}"
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error with GPT API: {str(e)}"
# Set up Streamlit app
st.set_page_config(page_title="PhishyWeb", page_icon="🐟")
st.title("🐟 PhishyWeb: Phishing Message Detector")

# Text input from user
input_text = st.text_area("Paste a suspicious email or message here:", height=250)

# Main analysis button
if st.button("🔍 Analyze"):
    if input_text.strip() == "":
        st.warning("Please enter a message before analyzing.")
    else:
        with st.spinner("Analyzing with AI..."):
            result = gpt_check(input_text)
            st.subheader("🧠 GPT Analysis")
            st.info(result)
