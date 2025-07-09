import streamlit as st
import re

# Load rules
def load_keywords(file_path):
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f.readlines()]

def score_email(text, keywords, bad_domains):
    score = 0
    findings = []

    text_lower = text.lower()
    urls = re.findall(r'(https?://[^\s]+)', text)

    for keyword in keywords:
        if keyword in text_lower:
            findings.append(f"🔑 Keyword found: *{keyword}*")
            score += 1

    for url in urls:
        for domain in bad_domains:
            if domain in url:
                findings.append(f"🔗 Suspicious URL: {url}")
                score += 2

    return findings, score

st.set_page_config(page_title="PhishyWeb", page_icon="🐟")
st.title("🐟 PhishyWeb: Phishing Message Detector")

# Session state for clearing input
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def reset():
    st.session_state.submitted = False
    st.session_state.input_text = ""

# Text input and submit button
input_text = st.text_area("Paste a suspicious email or message here:", key="input_text", height=250)
submit = st.button("Analyze")
reset_button = st.button("Reset")

# Reset logic
if reset_button:
    reset()

# Analyze logic
if submit:
    st.session_state.submitted = True

if st.session_state.submitted and input_text:
    keywords = load_keywords("phishing_rules/keywords.txt")
    bad_domains = load_keywords("phishing_rules/suspicious_domains.txt")

    findings, score = score_email(input_text, keywords, bad_domains)

    st.subheader("🔍 Results")
    for f in findings:
        st.markdown(f"- {f}")

    st.markdown("---")
    st.subheader("📊 Risk Score: " + str(score))
    if score >= 5:
        st.error("🟥 HIGH RISK – Likely phishing")
    elif score >= 3:
        st.warning("🟧 MEDIUM RISK – Suspicious signs detected")
    else:
        st.success("🟩 LOW RISK – No major red flags")
