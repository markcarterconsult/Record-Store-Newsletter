import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# ---------- SETUP ----------
st.set_page_config(page_title="Collector's Corner Newsletter Builder", layout="centered")
st.title("📰 Monthly Collector’s Corner Newsletter Generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add this in Streamlit Cloud > Settings > Secrets

# ---------- SCRAPER FUNCTION ----------
def scrape_website_content(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, 'html.parser')

        # Try grabbing Shopify-style product title + description
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

# ---------- AI GENERATION ----------
def generate_newsletter_from_content(raw_text, month):
    prompt = f"""
You are writing a vinyl collector newsletter titled "Collector’s Corner — {month} Edition" for Music Record Shop.

Summarize the following page content into these sections:
1. 🎯 Featured Pressing (1–2 sentences explaining what makes it collectible)
2. 📈 Valuation Tip (a collector trick or matrix to look for)
3. 🆕 Just In (list 2–3 cool records mentioned or implied)
4. 🗞️ Collector Buzz (industry or vinyl trend-related wrap-up)

Web Page Content:
{raw_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------- FORM UI ----------
month = st.selectbox("Edition Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

# URL for scraping
url = st.text_input("🔗 Paste a product/blog page URL to generate newsletter from")

if st.button("🧠 Generate from URL"):
    with st.spinner("Scraping and summarizing..."):
        raw_text = scrape_website_content(url)
        if "Error scraping" in raw_text:
            st.error(raw_text)
        else:
           def generate_newsletter_from_content(raw_text, month):
    prompt = f"""
You are a vinyl collector and newsletter editor creating the "Collector’s Corner — {month} Edition".

Summarize this content from a product/blog page into the following **exact format**, using 1–3 sentences per section:

🎯 Featured Pressing: ...
📈 Valuation Tip: ...
🆕 Just In: ...
🗞️ Collector Buzz: ...

Content to summarize:
{raw_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content


# Editable form fields
featured_pressing = st.text_area("🎯 Featured Pressing", value=st.session_state.get("featured_pressing", ""))
valuation_tip = st.text_area("📈 Valuation Tip", value=st.session_state.get("valuation_tip", ""))
just_in = st.text_area("🆕 Just In (New Arrivals)", value=st.session_state.get("just_in", ""))
industry_news = st.text_area("🗞️ Collector News + Industry Buzz", value=st.session_state.get("industry_news", ""))
spotlight = st.text_area("💬 Collector Spotlight (Optional)")
cta = st.text_input("📢 Call to Action (Optional)", placeholder="Link to Pressing Value Tool or Trade-In App")

# Newsletter Preview
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



