import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# ---------- SETUP ----------
st.set_page_config(page_title="Collector's Corner Newsletter Builder", layout="centered")
st.title("📰 Monthly Collector’s Corner Newsletter Generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add your OpenAI key in Streamlit secrets

# ---------- SCRAPE FUNCTION ----------
def scrape_website_content(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'li'])
        content = '\n'.join([p.get_text() for p in paragraphs])
        return content[:3000]  # Limit for token safety
    except Exception as e:
        return f"Error scraping: {e}"

# ---------- AI GENERATION FUNCTION ----------
def generate_newsletter_from_content(raw_text, month):
    prompt = f"""
You are writing a vinyl collector newsletter called "Collector’s Corner — {month} Edition" based on this scraped content:

{raw_text}

Create the following sections (1–3 sentences each):
🎯 Featured Pressing
📈 Valuation Tip
🆕 Just In (3 items)
🗞️ Industry News
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# ---------- FORM FIELDS ----------
month = st.selectbox("Edition Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

# -------- URL INPUT + GENERATE --------
url = st.text_input("🔗 Paste a blog post, product page, or article URL to pull content from")

if st.button("🧠 Generate from URL"):
    with st.spinner("Scraping and generating..."):
        raw_text = scrape_website_content(url)
        if "Error scraping" in raw_text:
            st.error(raw_text)
        else:
            ai_output = generate_newsletter_from_content(raw_text, month)

            # Auto-fill the fields
            sections = ai_output.split("\n\n")
            for sec in sections:
                if "🎯" in sec:
                    st.session_state["featured_pressing"] = sec.split("🎯 Featured Pressing")[-1].strip()
                elif "📈" in sec:
                    st.session_state["valuation_tip"] = sec.split("📈 Valuation Tip")[-1].strip()
                elif "🆕" in sec:
                    st.session_state["just_in"] = sec.split("🆕 Just In")[-1].strip()
                elif "🗞️" in sec:
                    st.session_state["industry_news"] = sec.split("🗞️ Industry News")[-1].strip()
            st.success("Fields generated! You can now edit them below.")

# ---------- MAIN FORM ----------
featured_pressing = st.text_area("🎯 Featured Pressing", value=st.session_state.get("featured_pressing", ""))
valuation_tip = st.text_area("📈 Valuation Tip", value=st.session_state.get("valuation_tip", ""))
just_in = st.text_area("🆕 Just In (New Arrivals)", value=st.session_state.get("just_in", ""))
industry_news = st.text_area("🗞️ Industry Buzz + Collector News", value=st.session_state.get("industry_news", ""))
spotlight = st.text_area("💬 Collector Spotlight (Optional)")
cta = st.text_input("📢 Call to Action (Optional)", placeholder="Link to Pressing Value Tool or Trade-In App")

# ---------- PREVIEW OUTPUT ----------
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

