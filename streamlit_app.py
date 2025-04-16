import streamlit as st
from openai import OpenAI
import re

# ---------- SETUP ----------
st.set_page_config(page_title="Collector's Corner Newsletter Builder", layout="centered")
st.title("📰 Collector’s Corner Newsletter Generator")

# 🔐 OpenAI Setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- GPT GENERATION ----------
def generate_newsletter(raw_input, month):
    prompt = f"""
You are creating a vinyl collector newsletter titled "Collector’s Corner — {month} Edition" for Music Record Shop.

Use the messy ideas below and turn them into a clean, structured, collector-savvy newsletter.

Format exactly like this:

## 🎯 Featured Pressing
[Polished description]

## 📈 Valuation Tip
[Insightful collector tip]

## 🆕 Just In
- [Record 1]
- [Record 2]
- [Record 3]

## 🗞️ Collector Buzz
[Industry news, trend, or fun fact]

Here are the notes to work from:
{raw_input}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------- SECTION PARSER ----------
def extract_section(text, header):
    pattern = rf"## {re.escape(header)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

# ---------- UI FORM ----------
month = st.selectbox("📅 Select Newsletter Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

user_notes = st.text_area("📝 Paste Your Rough Newsletter Notes Here", height=250, placeholder="""
- Bowie Ziggy Stardust UK 1st Press just arrived
- Tip: check matrix ‘BGBS 0864-2E’ for authentic glam press
- RSD hype: Smashing Pumpkins reissues + live sets
- Pearl Jam bootlegs trending on Discogs
""")

if st.button("🧠 Generate Newsletter"):
    with st.spinner("Creating your Collector’s Corner..."):
        newsletter_md = generate_newsletter(user_notes, month)
        st.session_state["newsletter_text"] = newsletter_md

# ---------- PREVIEW ----------
if "newsletter_text" in st.session_state:
    st.markdown("---")
    st.markdown(f"## 📬 Preview: Collector’s Corner — {month} Edition")
    st.markdown(st.session_state["newsletter_text"])

