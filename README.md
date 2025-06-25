# 🏠 AI Real Estate Advisor

**Aiming to simplify real estate planning through AI, this project was built with a focus on usability, insight, and scalability.**  
This application was built by me during **Round 2 (Final Round)** of the **Central India Hackathon 2.0 (23–24 June 2025)** organized by *Suryodaya College of Engineering & Technology, Nagpur*.

---

## 📌 Project Overview

**AI Real Estate Advisor** is a multilingual Streamlit web app that helps users in India make informed real estate investment decisions using AI-driven insights and financial strategy tools. By integrating the **Gemini API** (Google's Gen AI), it generates detailed reports tailored to user goals like buying a flat, building a house, or planning joint investments.

The application provides real estate investors with intelligent analysis, market simulation, and cost planning through a step-by-step interactive workflow. It supports CSV-based project management, AI-powered strategy generation, and multilingual UI.

---

## 🔑 Key Features

- ✅ Step-by-step investment planning workflow  
- 📊 14+ analytical tools (build vs. buy, rent forecasts, resale projections, etc.)  
- 🌐 Multilingual support (English, Hindi, Marathi)  
- 📁 Project management system using CSV-based data persistence  
- 🤖 Gemini AI integration for generating financial strategies and reports  
- 📍 Mock market data simulations based on Indian cities and localities  
- 📉 Construction cost breakdowns, environmental risk analysis, vendor suggestions, and more  

---

## 🛠️ Libraries Used

- `streamlit`  
- `google-generativeai >= 0.4.0`  
- `pandas`  
- `requests`  
- `tabulate`  

---

## 🚀 How to Run the Application

You can run this app locally or in a cloud-based Python environment like **GitHub Codespaces** or **Replit**.

### Step To Run The Application

**Step 1: Install Requirements**
pip install -r requirements.txt

**Step 2: Add Gemini API Keys**
Open the main script and replace the GEMINI_API_KEYS list with your valid API keys:
GEMINI_API_KEYS = ["your_api_key_1", "your_api_key_2"]

**Step 3: Launch the App**
streamlit run app.py

## 🙌 Support
If you found this project helpful, please consider giving it a ⭐ on GitHub repository — it helps others discover the project and supports future improvements.
