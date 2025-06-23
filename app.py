# app.py – Streamlit Real Estate Advisor

"""
🏠 Real Estate Advisor: Your Personal AI-Powered Property Guide

This app helps users understand whether it's better to buy, build, or invest
in real estate based on income, timeframe, and current market rates. It uses
Gemini (Google Generative AI) to give insights and strategies.

▶ Run:
    streamlit run app.py

🔑 This version uses a list of hardcoded API keys and randomizes their use.
   For better security in production, use Streamlit Secrets.

📦 Requirements (add to requirements.txt):
    streamlit
    google-generativeai>=0.4.0
    pandas
    requests
    tabulate  <-- Added dependency to fix the error
"""

import os
import random
import textwrap

import pandas as pd
import requests
import streamlit as st

try:
    import google.generativeai as genai
except ImportError:
    st.error("Gemini API library not found. Please run 'pip install google-generativeai' in your environment.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# Gemini Setup with Multiple Keys
# ─────────────────────────────────────────────────────────────────────────────

# --- Hardcoded API Key List ---
# WARNING: This is NOT a secure practice for production apps.
# Replace the placeholder keys with your 10 actual Gemini API keys.
GEMINI_API_KEYS = [
    "AIzaSyADl4G5aVaq3xw73HJiPDalelfqFH_XHCI",
    "AIzaSyBvx7uEa_JvFsnwyoubw380dg4HUOr9ASY",
    "AIzaSyBzlXxId2a40kQA-eiYWAGqPkJDjSdUXwk",
    "AIzaSyBb-KXLYLyRO4o2TFAeiOQNv4fG54O0GEU",
    "AIzaSyAxlYjiaWxTYFEUqxExiQ65zb0gGiYOGl8",
    "AIzaSyCTD7RfMmVTma0XP7o2uBysOreXipWR-pk",
    "AIzaSyCTHkBJxADynfyDnwvOOHrXj9y-jLP-x0M",
    "AIzaSyDyfUhcitS-wLxHahWJCIl66NEeB8n0tEc",
    "AIzaSyAb1ed4pTAIzOgQhOanAIW2ldXY3WXLjnE",
    "AIzaSyCGIQOMYnRUl-RjKKFJkI9RZcL0xq16uIw",
]

# Filter out any placeholder keys that haven't been replaced
valid_api_keys = [key for key in GEMINI_API_KEYS if "YOUR_API_KEY" not in key]

if not valid_api_keys:
    st.error("🔐 No valid Gemini API Keys found. Please add your keys to the `GEMINI_API_KEYS` list in the code.")
    st.info("💡 You can get an API key from Google AI Studio: https://ai.google.dev/")
    st.stop()

# Randomly select one key from the list for this app run
selected_key = random.choice(valid_api_keys)
genai.configure(api_key=selected_key)
MODEL = genai.GenerativeModel("gemini-1.5-flash")


@st.cache_data(ttl=600)
def ask_gemini(prompt: str, temperature: float = 0.4) -> str:
    """Sends prompt to Gemini API and returns the response text."""
    try:
        response = MODEL.generate_content(prompt, generation_config={"temperature": temperature})
        return response.text
    except Exception as err:
        st.error(f"⚠️ An error occurred with the Gemini API: {err}", icon="🤖")
        return "Sorry, I couldn't process your request. This may be due to a rate limit on the selected API key. Try reloading the page to use a different key."


# ─────────────────────────────────────────────────────────────────────────────
# Sample Market Data
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Fetching market data...", ttl=3600)
def get_price_data(city: str) -> pd.DataFrame:
    """Returns mock real estate data."""
    city_hash = hash(city.lower())
    base_land_price = 5000 + (city_hash % 2000)
    base_construction_cost = 1800 + (city_hash % 500)

    data = {
        "Property Type": ["Small Plot", "Medium Plot", "Large Plot", "2BHK Flat", "3BHK Villa"],
        "Area (sqft)": [1200, 1800, 2400, 1100, 2000],
        "Land Price (₹/sqft)": [base_land_price, base_land_price + 500, base_land_price + 1000, "N/A", "N/A"],
        "Construction Cost (₹/sqft)": [base_construction_cost, base_construction_cost + 200, base_construction_cost + 400, "N/A", "N/A"],
        "Ready Property Price (₹)": ["N/A", "N/A", "N/A", 6000000 + (city_hash % 2000000), 12000000 + (city_hash % 4000000)],
    }
    return pd.DataFrame(data)


# ─────────────────────────────────────────────────────────────────────────────
# Streamlit Interface
# ─────────────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="Real Estate Advisor", page_icon="🏠", layout="wide")

    # --- Header ---
    st.title("🏠 Real Estate Advisor")
    st.markdown("Your personal AI consultant for making smart real estate decisions in India.")

    # --- Sidebar for User Inputs ---
    with st.sidebar:
        st.header("🔍 Your Profile")
        name = st.text_input("Your Name", placeholder="e.g., Priya", key="user_name")
        income = st.number_input("Your Annual Household Income (₹)", min_value=100000, value=1000000, step=50000, format="%d", key="user_income")
        timeframe = st.slider("Investment Timeframe (in years)", min_value=1, max_value=30, value=5, key="user_timeframe")
        city = st.text_input("Preferred City", value="Nagpur", key="user_city")
        st.markdown("---")
        get_plan_button = st.button("🧠 Generate My Real Estate Plan", use_container_width=True, type="primary")
        st.markdown("---")
        st.caption("📢 **Disclaimer:** The advice provided is AI-generated and for informational purposes only. Always consult with a qualified financial advisor.")

    # --- Main Content Area ---
    st.subheader(f"📈 Market Snapshot: {city.title()}")
    df_prices = get_price_data(city)
    st.dataframe(df_prices, use_container_width=True, hide_index=True)

    st.divider()

    # --- AI Advisory Section ---
    st.subheader("💡 Your Personalized Strategy")
    if get_plan_button:
        if not all([name, income, city]):
            st.warning("Please fill in all the details in the sidebar to get your plan.", icon="⚠️")
        else:
            prompt = textwrap.dedent(f"""
                As an expert real estate and financial advisor in India, create a personalized real estate plan for {name}.

                **Client Profile:**
                - Name: {name}
                - Location: {city}, India
                - Annual Household Income: ₹{income:,.0f}
                - Investment Timeframe: {timeframe} years

                **Current Market Data for {city}:**
                {df_prices.to_markdown(index=False)}

                **Your Task:**
                Generate a friendly, encouraging, and clear advisory report in Markdown. Include these sections:
                1.  **Executive Summary:** A brief summary of the recommendation.
                2.  **Buy vs. Build Analysis:** Pros, cons, and rough cost estimates for both.
                3.  **Financial Strategy:** Affordability, savings plan, and financing options.
                4.  **Actionable Steps:** A step-by-step plan for the next 1-2 years.
                5.  **Friendly Closing:** A positive and motivational closing statement.
                Use bolding and bullet points for readability.
            """)
            with st.spinner("🤖 Crafting your personalized real estate plan..."):
                response = ask_gemini(prompt)
            st.markdown(response, unsafe_allow_html=True)
    else:
        st.info("Enter your details in the sidebar and click 'Generate My Real Estate Plan' to get started.")

    # --- NEW: Custom Prompt Box for Follow-up Questions ---
    st.divider()
    with st.expander("💬 Ask a Follow-up Question"):
        custom_question = st.text_area(
            "Have more questions? Ask here!",
            placeholder="e.g., What are the best areas to buy land in this city? or What are the tax benefits of a home loan?"
        )
        if st.button("✉️ Ask Gemini"):
            if not custom_question:
                st.warning("Please enter a question first.", icon="🤔")
            elif not all([name, income, city]):
                 st.warning("Please fill in your profile details in the sidebar first.", icon="⚠️")
            else:
                prompt = textwrap.dedent(f"""
                    You are a real estate and financial advisor AI for India. A user named {name} from {city} with an annual income of ₹{income:,.0f} is asking a follow-up question.
                    
                    **User's Original Context:**
                    - Location: {city}, India
                    - Annual Income: ₹{income:,.0f}
                    - Timeframe: {timeframe} years
                    - Market Data: {df_prices.to_markdown(index=False)}

                    **User's Question:**
                    "{custom_question}"

                    **Your Task:**
                    Answer the user's question clearly and concisely, keeping their profile and the provided market data in mind. Be helpful and professional.
                """)
                with st.spinner("🤔 Thinking..."):
                    response = ask_gemini(prompt, temperature=0.5)
                st.markdown(response, unsafe_allow_html=True)


if __name__ == "__main__":
    main()