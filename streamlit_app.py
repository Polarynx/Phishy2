import streamlit as st
from transformers import pipeline
import torch

st.set_page_config(page_title="PhishyWeb", layout="centered")
st.title("🧠 PhishyWeb - Email Phishing Detector")
st.write("Paste any email or message below to check if it's phishing.")

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

clf = load_model()

# Text input
text_input = st.text_area("📩 Paste the email or message here:", height=200)

if st.button("🔍 Analyze Message"):
    if text_input.strip() == "":
        st.warning("Please paste a message before analyzing.")
    else:
        with st.spinner("Analyzing..."):
            result = clf(text_input)
            label = result[0]['label']
            score = result[0]['score']

            # Interpret result
            if label == 'NEGATIVE':  # use for potential phishing
                if score >= 0.9:
                    verdict = "🔴 Likely Phishing (High Confidence)"
                elif score >= 0.6:
                    verdict = "🟠 Suspicious"
                else:
                    verdict = "🟢 Possibly Safe"
            else:
                verdict = "🟢 Safe"


            st.markdown(f"### 🧾 Verdict: {verdict}")
            st.markdown(f"**Model Confidence:** `{score:.2%}`")

# Footer
st.markdown("---")
st.markdown("Made by Polarynx | Powered by HuggingFace Transformers")

