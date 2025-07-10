import streamlit as st
from transformers import pipeline

# Load the phishing classifier pipeline from HuggingFace
@st.cache_resource
def load_model():
    return pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-phishing")

clf = load_model()

# Streamlit UI
st.set_page_config(page_title="PhishyWeb", page_icon="🐟")
st.title("🐟 PhishyWeb: Phishing Message Detector (ML-Based)")

input_text = st.text_area("Paste a suspicious email or message below:", height=250)

if st.button("🔍 Analyze with AI"):
    if not input_text.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Scanning message..."):
            try:
                result = clf(input_text[:512])[0]  # Truncate to 512 tokens
                label = result['label']
                score = round(result['score'] * 100, 2)

                st.subheader("🤖 ML Model Verdict")
                if "not" in label.lower():
                    st.success(f"🟢 Not Phishing ({score}%)")
                else:
                    st.error(f"🔴 Phishing Detected ({score}%)")

            except Exception as e:
                st.error(f"❌ Error: {e}")
