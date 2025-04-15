import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import re

# ---------- SETUP ----------
st.set_page_config(page_title="Collector's Corner Newsletter Builder", layout="centered")
st.title("📰 Monthly Collector’s Corner Newsletter Generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add your OpenAI API key in Streamlit Cloud > Settings > Secrets

# ---------- SCRAPER FUNCTION ----------
def scrape_website_content(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, 'html.parser')

        title = soup.find('h1')
        description = soup.find('div', class_='product-single__description')
        all_paragraphs = soup.find_all('p')
        paragraphs = "\n".join(p.get_text() for p in all_paragraphs)

        combined = ""

        if title:
            combined += f"Title: {title.get_text()}\n"
        if description:
            combined += f"Description: {description.get_text()}\n"

        combined += f"\nExtra Paragraphs:\n{paragraphs}"

        return combined[:3500]
    except Exception as e:
        return f"Error scraping: {e}"

# ---------- GPT-4 GENERATION FUNCTION ----------
def generate_newsletter_from_content(raw_text, month):
    prompt = f"""
You are a vinyl collector and newsletter editor creating the "Collector’s Corner — {month} Edition" for Music Record Shop.

Summarize this content into the following format. Each section should be 1–3 sentences:

## 🎯 Featured Pressing
...

## 📈 Valuation Tip
...

## 🆕 Just In
...

## 🗞️ Collector Buzz
...


Content:
{raw_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------- EXTRACTOR FUNCTION ----------
def extract_section(label, text):
    match = re.search(f"{re.escape(label)}:(.*?)(?=\n\S|$)", text, re.DOTALL)
    return match.group(1).strip() if match else ""

# ---------- FORM LOGIC ----------
month = st.selectbox("Edition Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

url = st.text_input("🔗 Paste a product or blog URL")

if st.button("🧠 Generate from URL"):
    with st.spinner("Scraping and summarizing..."):
        raw_text = scrape_website_content(url)
        if "Error scraping" in raw_text:
            st.error(raw_text)
        else:
            ai_output = generate_newsletter_from_content(raw_text, month)
            st.session_state["featured_pressing"] = extract_section("🎯 Featured Pressing", ai_output)
            st.session_state["valuation_tip"] = extract_section("📈 Valuation Tip", ai_output)
            st.session_state["just_in"] = extract_section("🆕 Just In", ai_output)
            st.session_state["industry_news"] = extract_section("🗞️ Collector Buzz", ai_output)
            st.success("Newsletter content generated!")

# Editable fields
featured_pressing = st.text_area("🎯 Featured Pressing", value=st.session_state.get("featured_pressing", ""))
valuation_tip = st.text_area("📈 Valuation Tip", value=st.session_state.get("valuation_tip", ""))
just_in = st.text_area("🆕 Just In (New Arrivals)", value=st.session_state.get("just_in", ""))
industry_news = st.text_area("🗞️ Collector News + Industry Buzz", value=st.session_state.get("industry_news", ""))
spotlight = st.text_area("💬 Collector Spotlight (Optional)")
cta = st.text_input("📢 Call to Action (Optional)", placeholder="Link to Pressing Value Tool or Trade-In App")

if st.button("🧠 Generate Newsletter Preview"):
    st.markdown("---")
    st.markdown(f"## 📰 Collector’s Corner — {month} Edition")
    st.markdown("From Music Record Shop\n")
    st.markdown("### 🎯 Featured Pressing of the Month")
    st.markdown(featured_pressing)
    st.markdown("### 📈 Valuation Tip of the Month")
    st.markdown(valuation_tip)
    st.markdown("### 🆕 Just In: New Arrivals")
    st.markdown(just_in)
    st.markdown("### 🗞️ Collector News + Industry Buzz")
    st.markdown(industry_news)
    if spotlight:
        st.markdown("### 💬 Collector Spotlight")
        st.markdown(spotlight)
    if cta:
        st.markdown("### 📢 Want to Sell or Trade Records?")
        st.markdown(f"{cta}")



