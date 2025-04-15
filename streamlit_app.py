import streamlit as st

st.set_page_config(page_title="Collector's Corner Newsletter Builder", layout="centered")
st.title("📰 Monthly Collector’s Corner Newsletter Generator")

# Newsletter Fields
month = st.selectbox("Edition Month", [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
])

featured_pressing = st.text_area("🎯 Featured Pressing", placeholder="Example: Radiohead – OK Computer (1997, UK 1st Pressing)...")
valuation_tip = st.text_area("📈 Valuation Tip", placeholder="Example: Look for 'RL' in the runout of Led Zeppelin II...")
just_in = st.text_area("🆕 Just In (New Arrivals)", placeholder="Example: - Nirvana – Unplugged in NY\n- MF DOOM – MM..FOOD")
industry_news = st.text_area("🗞️ Industry Buzz + Collector News", placeholder="Example: RSD drops announced for next month...")
spotlight = st.text_area("💬 Collector Spotlight (Optional)", placeholder="Example: Mark from STL shares his rare Pearl Jam find...")
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
