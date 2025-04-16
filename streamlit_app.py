import streamlit as st
from openai import OpenAI
import re

# ---------- SETUP ----------
st.set_page_config(page_title="Collector's Corner Newsletter Builder", layout="centered")
st.title("📰 Collector’s Corner Newsletter Generator")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- GPT GENERATION ----------
def generate_newsletter(raw_input, month):
    prompt = f"""
You're helping create a collector newsletter called "Collector’s Corner — {month} Edition" for Music Record Shop.

Turn the rough ideas below into clean newsletter sections using this exact format:

## 🎯 Featured Pressing
[Polished description]

## 📈 Valuation Tip
[Insightful collector tip]

## 🆕 Just In
- [Record 1]
- [Record 2]
- [Record 3]

## 🗞️ Collector Buzz
[Industry news, RSD info, or fun fact]

Input Notes:
{raw_input}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------- EXTRACT SECTIONS ----------
def extract_section(text, header):
    pattern = rf"## {re.escape(header)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

# ---------- UI ----------
month = st.selectbox("📅 Select Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

user_notes = st.text_area("📝 Paste Rough Notes Here", height=250, placeholder="""
- Ziggy Stardust UK 1st press just arrived
- Tip: look for matrix ‘BGBS 0864-2E’
- RSD: Smashing Pumpkins reissue + live set
- Discogs trending: Pearl Jam bootlegs
""")

if st.button("🧠 Generate Newsletter"):
    with st.spinner("Building your Collector’s Corner..."):
        output = generate_newsletter(user_notes, month)
        st.session_state["full_newsletter"] = output
        st.session_state["featured"] = extract_section(output, "🎯 Featured Pressing")
        st.session_state["tip"] = extract_section(output, "📈 Valuation Tip")
        st.session_state["just_in"] = extract_section(output, "🆕 Just In")
        st.session_state["buzz"] = extract_section(output, "🗞️ Collector Buzz")

# ---------- OUTPUT ----------
if "full_newsletter" in st.session_state:
    st.markdown("### 🎯 Featured Pressing")
    st.text_area("Copy this", value=st.session_state["featured"], height=100)

    st.markdown("### 📈 Valuation Tip")
    st.text_area("Copy this", value=st.session_state["tip"], height=100)

    st.markdown("### 🆕 Just In")
    st.text_area("Copy this", value=st.session_state["just_in"], height=100)

    st.markdown("### 🗞️ Collector Buzz")
    st.text_area("Copy this", value=st.session_state["buzz"], height=120)

    st.markdown("---")
    st.markdown("### 📰 Full Newsletter Preview")
    st.markdown(st.session_state["full_newsletter"])


