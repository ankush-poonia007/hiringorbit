import streamlit as st
from agent import ask_agent

st.set_page_config(page_title="HiringOrbit", page_icon="🌍")

st.title("🌍 HiringOrbit")
st.subheader("Location-Aware Intelligence Agent")

location = st.text_input("Enter your city/location:", placeholder="e.g. Jaipur, Rajasthan")
query = st.text_input("What are you looking for?", placeholder="e.g. engineering colleges, tech companies, ML meetups")

if st.button("Search"):
    if location and query:
        with st.spinner("Searching..."):
            response, raw_results = ask_agent(query, location)
        
        st.markdown("### 📍 Places Found")
        st.text(raw_results)
        
        st.markdown("### 🤖 Agent Recommendation")
        st.write(response)
    else:
        st.warning("Please enter both location and query.")