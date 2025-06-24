# app.py – Streamlit Real Estate Advisor (Multi-Tool, Multi-Language, FSI-Aware, Printable, Multi-Step, & File-based)

"""
🏠 AI Real Estate Advisor: Your Guided Project Planner

This is a comprehensive, multi-language version that combines a guided workflow
with a robust project storage system and advanced analysis tools.

FEATURES (Updated):
- **15 Advanced Calculators:** Includes Build vs. Buy, Hyper-Local Price & Rent Analysis,
  Detailed Cost Breakdown, Material Prices, Payback Calculator, Resale Predictor,
  Green Cost & Savings Estimators, Location Quality Score, Comparative Locality Analysis,
  and NEW Flood/Eco-Zone Alert, Vendor Suggestions, & a Loan/Subsidy Guide.
- **Stateful Tool Navigation:** Seamlessly switch between the main report and advanced tools.
- **Multi-Language Support:** UI and AI responses in English, Hindi, and Marathi.
- **FSI & Investment Workflows:** Specialized forms for FSI calculations and co-ownership.
- **Printable Reports:** A "Print" button to save the generated AI strategy as a PDF.
- **Individual Project Files:** Each project is saved as a unique CSV in a 'projects' directory.
- **Enhanced Sidebar:** A dynamic sidebar for full project management.

▶ Run:
    streamlit run app.py

📦 Requirements (add to requirements.txt):
    streamlit
    google-generativeai>=0.4.0
    pandas
    numpy
"""

import os
import random
import textwrap
import math
import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta

# --- Directory for storing individual project files ---
PROJECTS_DIR = "projects"
os.makedirs(PROJECTS_DIR, exist_ok=True)

try:
    import google.generativeai as genai
except ImportError:
    st.error("Gemini API library not found. Please run 'pip install google-generativeai' in your environment.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# Gemini Setup & Translation
# ─────────────────────────────────────────────────────────────────────────────
# WARNING: For production, use Streamlit Secrets (st.secrets). Hardcoding keys is insecure.
GEMINI_API_KEYS = [
    # Add your Gemini API keys here
    "AIzaSyAejvlhIRTaB3-36e-1kXkSn-EaoQasIlA", "AIzaSyDNHN7T5apK6VckmgQJ3AY_5oCgXkwtyuc",
]
valid_api_keys = [key for key in GEMINI_API_KEYS if "YOUR_API_KEY" not in key]

if not valid_api_keys:
    st.error("🔐 No valid Gemini API Keys found. Please add your keys to the GEMINI_API_KEYS list in the code.")
    st.stop()

selected_key = random.choice(valid_api_keys)
genai.configure(api_key=selected_key)
MODEL = genai.GenerativeModel("gemini-1.5-flash")

# --- Translation Dictionary (Heavily Expanded for New Features) ---
TRANSLATIONS = {
    'en': {
        # --- Core App ---
        "language_name": "English", "app_title": "AI Real Estate Advisor", "project_manager_title": "Project Manager",
        "active_project_caption": "Active Project", "switch_project_button": "🔄 Switch Project", "danger_zone_header": "🚨 Danger Zone",
        "delete_confirm_checkbox": "Confirm deletion", "delete_project_button": "❌ Delete Project Permanently", "project_deleted_success": "Project '{project_name}' has been deleted.",
        "project_file_not_found_warning": "Project file for '{project_name}' not found.", "delete_project_error": "Error deleting project: {e}",
        "create_new_project_header": "➕ Create New Project", "new_project_name_label": "Enter a Unique Project Name", "start_new_project_button": "Start New Project",
        "project_name_exists_error": "Project name already exists.", "enter_project_name_warning": "Please enter a project name.",
        "load_existing_project_header": "📂 Load Existing Project", "select_project_placeholder": "Choose a project...", "load_project_button": "Load Project",
        "project_loaded_success": "Project '{project_name}' loaded successfully!", "load_project_error": "Failed to load project '{project_name}': {e}",
        "disclaimer_info": "AI-generated advice. Always consult a professional before making financial decisions.",
        "welcome_message": "👋 **Welcome!** To begin, please create a new project or load an existing one from the sidebar.", "current_project_header": "Current Project: **{project_name}**",
        "step1_header": "STEP 1: Your Personal Details", "full_name_label": "Full Name", "dob_label": "Date of Birth", "contact_label": "Email or Phone",
        "income_label": "Annual Household Income (₹)", "next_goal_button": "Next: Define Your Goal", "fill_all_details_error": "Please fill in all details.",
        "step2_header": "STEP 2: What is Your Primary Goal?", "select_goal_label": "Select your goal", "buy_flat": "Buy a Flat", "build_house": "Build a House",
        "buy_plot": "Buy a Plot", "mixed_investment": "Mixed / Investment", "next_specifics_button": "Next: Add Specifics",
        "step3_header": "STEP 3: Specifics for '{intent_type}'", "location_budget_header": "Location & Budget", "target_city_label": "Target City",
        "localities_label": "Preferred Localities (comma-separated)", "pincode_label": "Pin Code", "budget_label": "Total Budget (₹)",
        "need_loan_checkbox": "Need a loan?", "subsidy_checkbox": "Interested in subsidy schemes?", "main_purpose_label": "Main purpose?",
        "self_use": "Self Use", "rental_income": "Rental Income", "resale_investment": "Resale / Investment", "mixed_components_label": "Select all that apply:",
        "flat_details_header": "Flat Details", "flat_size_label": "Flat Size", "plot_construction_potential_header": "Plot & Construction Potential",
        "plot_area_label": "Plot Area (sq. ft)", "construction_details_header": "Construction Details", "built_up_area_label": "Target Built-up Area (sq. ft)",
        "floors_label": "Number of Floors Planned", "extra_floors_rent_checkbox": "Plan extra floors for rent?", "contract_type_label": "Contract Type",
        "vendors_label": "Specific Vendors Needed?", "green_features_label": "Desired Green Features", "timeline_label": "Estimated Build Timeline (Months)",
        "preferences_concerns_header": "Preferences & Concerns", "connectivity_label": "Connectivity Importance", "amenities_label": "Proximity to Schools/Hospitals",
        "pollution_label": "Pollution Concern Level", "crime_label": "Crime Concern Level", "investment_goals_header": "Investment Goals",
        "target_rent_label": "Target Monthly Rent Income (₹)", "target_resale_label": "Target Resale Price (₹)", "save_proceed_button": "Save Project & Proceed to Analysis",
        "step4_header": "STEP 4: Review and Generate AI Strategy", "project_saved_success": "Your project is saved. Review the details below and generate your personalized financial plan.",
        "view_details_expander": "View/Hide Your Saved Project Details", "market_snapshot_header": "📈 Market Snapshot: {city}", "generate_strategy_button": "🧠 Generate Financial Strategy",
        "edit_details_button": "✏️ Edit Specifics", "analyzing_spinner": "🤖 Analyzing your project and crafting a detailed financial plan...",
        "strategy_header": "💡 Your Personalized Financial Strategy", "follow_up_expander": "💬 Ask a Follow-up Question",
        "follow_up_placeholder": "e.g., What happens if the interest rate increases by 0.5%?", "ask_advisor_button": "✉️ Ask Advisor",
        "enter_question_warning": "Please enter a question.", "thinking_spinner": "🤔 Thinking...", "mixed_investment_header": "Co-Ownership & Investment Details",
        "is_joint_investment_checkbox": "Is this a joint investment with a co-owner?", "co_owner_name_label": "Co-owner's Full Name",
        "co_owner_relationship_label": "Relationship to Co-owner", "investment_share_p1_label": "Your Share (%)", "investment_share_p2_label": "Co-owner's Share (%)",
        "relationship_spouse": "Spouse", "relationship_parent": "Parent/Child", "relationship_sibling": "Sibling", "relationship_business": "Business Partner", "relationship_other": "Other",
        "fsi_label": "Floor Space Index (FSI)", "fsi_help": "The ratio of a building's total floor area to the size of the piece of land upon which it is built. Check local regulations for the correct value.",
        "max_construction_area_label": "Max. Permissible Construction Area", "print_report_button": "🖨️ Print Report",
        "advanced_tools_header": "🛠️ Advanced Analysis Tools", "back_to_analysis_button": "⬅️ Back to Main Analysis", "back_button_text": "⬅️ Back",
        "api_error_message": "⚠️ An error occurred with the AI service: {err}",
        "analysis_projections_header": "Analysis & Projections", "cost_construction_header": "Cost & Construction", "financial_green_header": "Financial & Green",

        # --- Tool: Build vs. Buy ---
        "tool_build_vs_buy_button": "Build vs. Buy", "tool_build_vs_buy_title": "Build vs. Buy: Unit Economics", "tool_build_vs_buy_info": "This tool compares the total project cost of building a multi-unit property versus the cost of buying a single ready-made flat, breaking it down to a per-unit cost.", "build_cost_header": "Total Project Cost (to Build)", "buy_cost_header": "Cost to Buy (Single Flat)", "land_cost": "Land Cost", "construction_cost": "Total Construction Cost", "other_costs": "Other Costs (10%)", "total_build_cost": "Total Project Cost", "property_price": "Ready-Made Flat Price", "breakeven_analysis_header": "Per-Unit Breakeven Analysis", "num_flats_to_build_label": "Number of Flats to Build", "cost_per_flat_build_label": "Cost Per Flat (If You Build)", "price_ready_flat_label": "Price of Ready-Made Flat", "build_vs_buy_conclusion": "Your total project cost of **₹{total_build_cost:,.0f}** is high due to land value. However, by building **{num_flats} units**, your effective cost per flat is **₹{cost_per_flat:,.0f}**, which is **{comparison}** than buying a single ready-made flat for **₹{buy_price:,.0f}**.",
        "tool_locality_compare_button": "Hyper-Local Prices", "tool_locality_compare_title": "Hyper-Local Price Analyzer", "tool_locality_compare_info": "This tool shows how property prices can vary within the same locality based on proximity to the main road.", "locality_price_table_header": "Price Variation in {locality}",
        "tool_sqft_breakdown_button": "Detailed Costs", "tool_sqft_breakdown_title": "Detailed Construction Cost Breakdown", "tool_sqft_breakdown_info": "This provides a detailed breakdown of construction costs, showing each item's price based on your budget and its percentage of the total.", "house_construction_tab": "House Construction Costs", "flat_interiors_tab": "Flat Finishing Costs", "cost_item_label": "Item", "cost_sqft_label": "Cost per sq.ft. (₹)", "cost_as_percent_label": "% of Total", "cost_price_label": "Price (₹)",
        "tool_contract_diff_button": "Material Prices", "tool_contract_diff_title": "Material Price Analyzer", "tool_contract_diff_info": "This tool shows estimated prices for key construction materials across different commercial zones in your city.", "material_prices_header": "Estimated Material Prices in {city}",

        # --- NEW & ENHANCED TOOLS ---
        "tool_resale_predictor_button": "Resale Predictor", "tool_resale_predictor_title": "Resale Value Predictor", "tool_resale_predictor_info": "This tool projects the future resale value of your property based on a simulated annual growth rate.", "resale_projection_header": "{years}-Year Resale Projection for a {size} sq.ft. Property", "current_value_label": "Current Estimated Value", "projected_value_label": "Projected Value", "annual_growth_rate_label": "Simulated Annual Growth Rate", "property_size_label": "Property Size (sq.ft)",
        "tool_rent_forecaster_button": "Rent Forecaster", "tool_rent_forecaster_title": "Hyper-Local Rental Income Forecaster", "tool_rent_forecaster_info": "Estimate potential monthly rent based on both rental type (Residential, Retail, Office) and the property's specific location within the neighborhood.", "forecast_monthly_rent_label": "Forecasted Monthly Rent (₹)", "location_label": "Location",
        "tool_payback_calculator_button": "Payback Calculator", "tool_payback_calculator_title": "Hyper-Local Investment Payback Calculator", "tool_payback_calculator_info": "Calculates the payback period (in years) based on rental type and location, factoring in different maintenance & expense ratios for each.", "payback_period_label": "Payback Period (Years)",
        "rent_type_residential": "Residential", "rent_type_commercial_retail": "Commercial (Retail)", "rent_type_commercial_office": "Commercial (Office)",

        # --- GREEN & ECO TOOLS ---
        "green_eco_costing_header": "♻️ Green + Eco Costing",
        "tool_green_cost_estimator_button": "Green Cost Estimator", "tool_green_cost_estimator_title": "Green Feature Cost Estimator", "tool_green_cost_estimator_info": "Estimate the initial installation cost for popular eco-friendly features like solar panels, rainwater harvesting, and insulation.",
        "green_feature_label": "Green Feature", "estimated_cost_label": "Estimated Cost (₹)", "notes_label": "Notes / Assumptions",
        "solar_panels_label": "Solar Panels", "rainwater_harvesting_label": "Rainwater Harvesting", "heat_insulation_label": "Heat Insulation (Roof)",
        "solar_note": "Based on a 5kW system for a standard house.", "rainwater_note": "For a 10,000-liter underground tank.", "insulation_note": "Based on roof area (approx. 60% of built-up area).",
        "tool_green_savings_predictor_button": "Green Savings Predictor", "tool_green_savings_predictor_title": "Eco-Savings & Payback Predictor", "tool_green_savings_predictor_info": "This tool forecasts your long-term financial savings on utility bills (electricity, water) from green investments and calculates the simple payback period.",
        "annual_savings_label": "Est. Annual Savings (₹)", "payback_period_years_label": "Payback Period (Years)",

        # --- LOCATION INTELLIGENCE TOOLS (NEW) ---
        "location_intelligence_header": "📍 Location & Market Intelligence",
        "tool_location_quality_button": "Location Quality Score", "tool_location_quality_title": "Location Quality Score Analyzer", "tool_location_quality_info": "Calculates a quality score for your target location based on your preferences for connectivity, amenities, and your concerns about pollution and crime.",
        "your_location_score_label": "Your Location's Quality Score", "score_breakdown_header": "Score Breakdown", "factor_label": "Factor", "your_preference_label": "Your Preference", "score_impact_label": "Score Impact",
        "tool_compare_localities_button": "Compare Nearby Options", "tool_compare_localities_title": "Comparative Locality Analysis", "tool_compare_localities_info": "Discover alternative localities in the same city that might offer better value or a better location score for your budget.",
        "your_target_locality_label": "Your Target Locality", "for_your_budget_label": "For your budget of", "you_can_get_label": "you can get approx.", "sq_ft_label": "sq. ft.",
        "alternative_localities_header": "Alternative Localities in {city}", "locality_label": "Locality", "avg_price_psf_label": "Avg. Price (psf)", "location_score_label": "Location Score", "property_size_for_budget_label": "Area for your Budget", "vibe_label": "Vibe / Character",

        # --- NEW FEATURES (Flood, Vendor, Loan) ---
        "tool_env_risk_button": "Environmental Risk", "tool_env_risk_title": "Flood & Eco-Zone Risk Analysis", "tool_env_risk_info": "Assesses potential flood and ecological sensitivity risks for your chosen locality. *Note: This is a simulation based on general data and not a legal certification.*",
        "risk_assessment_for_label": "Risk Assessment For:", "flood_risk_label": "Flood Zone Risk", "eco_risk_label": "Ecological Sensitivity",
        "risk_level_low": "Low", "risk_level_medium": "Medium", "risk_level_high": "High",
        "risk_advice_low": "Standard precautions recommended.", "risk_advice_medium": "Further due diligence recommended. Check local municipal records and consider professional assessment.", "risk_advice_high": "High risk indicated. Essential to consult local authorities and perform a detailed environmental impact assessment before proceeding.",
        "tool_vendor_suggestion_button": "Find Vendors", "tool_vendor_suggestion_title": "Top-Rated Vendor Suggestions", "tool_vendor_suggestion_info": "Find simulated top-rated builders and vendors in your city for various project needs. *Ratings and reviews are for demonstration purposes.*",
        "vendor_type_label": "Select Vendor Type", "vendor_name_label": "Vendor Name", "vendor_specialty_label": "Specialty", "vendor_rating_label": "Rating", "vendor_review_label": "Summary",
        "tool_loan_guide_button": "Loan & Subsidy Guide", "tool_loan_guide_title": "Loan & Subsidy Eligibility Guide", "tool_loan_guide_info": "Get information on home loans, potential government subsidies like PMAY, and tax benefits.",
        "loan_tips_header": "Home Loan Tips", "pmay_guide_header": "PMAY Subsidy Guide", "tax_benefits_header": "Tax Saving Tips", "pmay_eligibility_header": "Your PMAY Eligibility (Simulation)",
    },
    'hi': { # Hindi Translations
        "language_name": "Hindi (हिन्दी)", "app_title": "एआई रियल एस्टेट सलाहकार",
    },
    'mr': { # Marathi Translations
        "language_name": "Marathi (मराठी)", "app_title": "एआय रिअल इस्टेट सल्लागार",
    }
}
# Add fallbacks for other languages to English
for lang in ['hi', 'mr']:
    for key, value in TRANSLATIONS['en'].items():
        if key not in TRANSLATIONS[lang]:
            TRANSLATIONS[lang][key] = value

def t(key):
    """Translation helper function."""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# --- Constants ---
CSV_COLUMNS = [
    'project_name','name','contact','dob','income','intent_type','intent_purpose','loc_city','loc_locality',
    'loc_pincode','fin_budget','fin_loan','fin_subsidy','mixed_components','plan_flat_size','plan_plot_area',
    'plan_built_up','plan_floors','extra_floors_rent','const_contract','const_vendors','const_green',
    'const_timeline','qual_connectivity','qual_amenities','risk_pollution','risk_crime',
    'fin_target_rent','fin_target_resale',
    'is_joint_investment', 'co_owner_name', 'co_owner_relationship', 'investment_share_p1', 'investment_share_p2',
    'fsi_value'
]

# ─────────────────────────────────────────────────────────────────────────────
# Core & Mock Data Functions
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600)
def ask_gemini(prompt: str, temperature: float = 0.4) -> str:
    try:
        response = MODEL.generate_content(prompt, generation_config={"temperature": temperature})
        return response.text
    except Exception as err:
        st.error(t('api_error_message').format(err=err), icon="🤖")
        return "Sorry, I couldn't process your request. The API may be busy. Please try again."

def get_saved_projects():
    return sorted([f.replace(".csv", "").replace("_", " ") for f in os.listdir(PROJECTS_DIR) if f.endswith(".csv")])

def get_project_filepath(project_name):
    return os.path.join(PROJECTS_DIR, f"{project_name.replace(' ', '_')}.csv")

def save_project():
    project_name = st.session_state.selected_project
    if not project_name: return False
    data_to_save = {key: st.session_state.get(key) for key in CSV_COLUMNS}
    for key in ['mixed_components', 'const_vendors', 'const_green']:
        if key in data_to_save and isinstance(data_to_save[key], list):
            data_to_save[key] = '|'.join(map(str, data_to_save[key]))
    if 'dob' in data_to_save and isinstance(data_to_save.get('dob'), date):
        data_to_save['dob'] = data_to_save['dob'].isoformat()
    try:
        df = pd.DataFrame([data_to_save])[CSV_COLUMNS]
        df.to_csv(get_project_filepath(project_name), index=False)
        return True
    except Exception as e:
        st.error(f"Error saving project '{project_name}': {e}")
        return False

def load_project(project_name):
    filepath = get_project_filepath(project_name)
    try:
        df = pd.read_csv(filepath).fillna('')
        for key, value in df.to_dict('records')[0].items(): st.session_state[key] = value
        for key in ['mixed_components', 'const_vendors', 'const_green']:
            if isinstance(st.session_state.get(key), str) and st.session_state[key]: st.session_state[key] = st.session_state[key].split('|')
            else: st.session_state[key] = []
        if 'dob' in st.session_state and st.session_state['dob']: st.session_state['dob'] = date.fromisoformat(str(st.session_state['dob']))
        else: st.session_state['dob'] = date(2000, 1, 1)
        for key in ['investment_share_p1', 'investment_share_p2', 'fsi_value', 'plan_plot_area', 'plan_built_up', 'plan_floors', 'const_timeline']:
            try:
                if st.session_state.get(key) not in [None, '']: st.session_state[key] = float(st.session_state[key])
            except (ValueError, TypeError): st.session_state[key] = 0.0
        st.session_state.step = 4
        st.session_state.ai_response, st.session_state.follow_up_response, st.session_state.active_tool = None, None, None
        st.success(t('project_loaded_success').format(project_name=project_name))
    except Exception as e:
        st.error(t('load_project_error').format(project_name=project_name, e=e))

def delete_project(project_name):
    try:
        filepath = get_project_filepath(project_name)
        if os.path.exists(filepath):
            os.remove(filepath)
            st.success(t('project_deleted_success').format(project_name=project_name))
            return True
        else:
            st.warning(t('project_file_not_found_warning').format(project_name=project_name))
            return False
    except Exception as e:
        st.error(t('delete_project_error').format(e=e))
        return False

@st.cache_data
def get_price_data(city_name: str) -> pd.DataFrame:
    if not city_name or pd.isna(city_name): city_name = "Default City"
    city_hash = hash(city_name.lower()); seed = city_hash % (2**32 - 1)
    np.random.seed(seed)
    base_prices = {
        "1 BHK Apartment": 4500 + (city_hash % 1500), "2 BHK Apartment": 5500 + (city_hash % 2000),
        "3 BHK Apartment": 6500 + (city_hash % 2500), "Plot / Land": 3000 + (city_hash % 3000),
        "Commercial Space": 8000 + (city_hash % 4000)
    }
    data = []
    for prop_type, base_price in base_prices.items():
        avg_price = base_price * np.random.uniform(0.98, 1.02)
        lower_bound = avg_price * 0.85; upper_bound = avg_price * 1.15
        price_range = f"₹{lower_bound:,.0f} - ₹{upper_bound:,.0f}"
        data.append({
            "Property Type": prop_type, "Average Price (per sq.ft)": f"₹{avg_price:,.0f}",
            "Typical Price Range (per sq.ft)": price_range
        })
    return pd.DataFrame(data)

# --- MOCK DATA FUNCTIONS (Including NEW & UPDATED) ---

@st.cache_data
def get_mock_build_vs_buy_data(loc_city, plan_plot_area, plan_built_up):
    city_hash = hash(loc_city.lower())
    SINGLE_FLAT_SIZE_FOR_COMPARISON = 900
    base_land_rate = 5000 + (city_hash % 2000)
    base_construction_sqft = 1800 + (city_hash % 500)
    plot_area = float(plan_plot_area or 1200)
    built_up_area = float(plan_built_up or 1800)
    land_cost = plot_area * base_land_rate
    construction_cost = built_up_area * base_construction_sqft
    other_costs = (land_cost + construction_cost) * 0.10
    total_build_cost = land_cost + construction_cost + other_costs
    buy_cost_single_flat = (4500 + (city_hash % 2500)) * SINGLE_FLAT_SIZE_FOR_COMPARISON
    num_flats_possible = max(1, math.floor(built_up_area / SINGLE_FLAT_SIZE_FOR_COMPARISON))
    cost_per_built_flat = total_build_cost / num_flats_possible
    return {
        "build": {"land": land_cost, "construction": construction_cost, "other": other_costs, "total": total_build_cost, "num_flats": num_flats_possible, "cost_per_flat": cost_per_built_flat},
        "buy": {"total_single_flat": buy_cost_single_flat}
    }

@st.cache_data
def get_mock_hyperlocal_price_data(loc_city, loc_locality):
    locality = loc_locality or 'your locality'
    locality_hash = hash(loc_city.lower() + locality.lower())
    np.random.seed(locality_hash % (2**32 - 1))
    base_rate = 6000 + (locality_hash % 3000)
    data = [
        {"Location": t('location_on_main_road'), "Price per sq.ft (₹)": base_rate, "Modifier": 1.0},
        {"Location": t('location_slightly_interior'), "Price per sq.ft (₹)": int(base_rate * 0.90), "Modifier": 0.90},
        {"Location": t('location_interior'), "Price per sq.ft (₹)": int(base_rate * 0.82), "Modifier": 0.82},
        {"Location": t('location_deep_interior'), "Price per sq.ft (₹)": int(base_rate * 0.70), "Modifier": 0.70},
    ]
    return pd.DataFrame([{"Location": d["Location"], "Modifier": d["Modifier"]} for d in data])


@st.cache_data
def get_mock_resale_projection_data(loc_city, loc_locality, property_size_sqft):
    locality_hash = hash(loc_city.lower() + (loc_locality or '').lower())
    np.random.seed(locality_hash % (2**32 - 1))
    current_price_psf = 6000 + (locality_hash % 3000)
    annual_growth_rate = np.random.uniform(0.04, 0.08) # 4% to 8% annual growth
    projections = {"Year": [], "Projected Price per sq.ft (₹)": [], "Projected Total Value (₹)": []}
    for i in range(0, 11, 2):
        projected_psf = current_price_psf * ((1 + annual_growth_rate) ** i)
        projected_total = projected_psf * property_size_sqft
        year_label = "Current" if i == 0 else f"+{i} Years"
        projections["Year"].append(year_label)
        projections["Projected Price per sq.ft (₹)"].append(f"₹{projected_psf:,.0f}")
        projections["Projected Total Value (₹)"].append(f"₹{projected_total:,.0f}")
    return {
        "current_value": current_price_psf * property_size_sqft, "projected_value_10y": (current_price_psf * ((1 + annual_growth_rate) ** 10)) * property_size_sqft,
        "growth_rate": annual_growth_rate, "table": pd.DataFrame(projections)
    }

@st.cache_data
def get_mock_detailed_sqft_costs(loc_city):
    city_hash = hash(loc_city.lower())
    np.random.seed(city_hash % (2**32 - 1))
    flat_costs = { "Flooring (Vitrified Tiles)": 150 + (city_hash % 40), "Painting (Emulsion)": 40 + (city_hash % 15), "Electrical (Wiring & Fixtures)": 130 + (city_hash % 30), "Plumbing (Pipes & Fixtures)": 160 + (city_hash % 35), "Doors & Windows": 200 + (city_hash % 50), "Kitchen Platform & Sink": 90 + (city_hash % 20), "Bathroom Tiling & Fixtures": 180 + (city_hash % 40), }
    house_costs = { "Foundation & Plinth": 250 + (city_hash % 50), "Structure (Steel, Cement, Aggregate)": 600 + (city_hash % 150), "Brickwork & Plastering": 220 + (city_hash % 40), **flat_costs }
    return { "house": pd.DataFrame(list(house_costs.items()), columns=[t("cost_item_label"), t("cost_sqft_label")]), "flat": pd.DataFrame(list(flat_costs.items()), columns=[t("cost_item_label"), t("cost_sqft_label")]) }

@st.cache_data
def get_mock_material_prices_by_area(loc_city):
    city = loc_city or 'Nagpur'; city_hash = hash(city.lower()); np.random.seed(city_hash % (2**32 - 1))
    zones = {"Nagpur": ["Butibori (Industrial)", "Kalamna (Market)", "Hingna (Industrial)"], "Pune": ["Chakan (Industrial)", "Market Yard", "Pimpri-Chinchwad"], "Mumbai": ["Bhiwandi (Logistics)", "Crawford Market", "Navi Mumbai"],}.get(city, ["Main Industrial Zone", "Central Market", "Suburban Supplier"])
    base_prices = {"Cement (per 50kg bag)": 380, "Steel (per kg)": 65, "Bricks (per 1000)": 7000, "Sand (per cft)": 50, "Aggregate (per cft)": 40}
    data = {"Material": list(base_prices.keys())}
    for zone in zones:
        zone_hash = hash(zone.lower()); prices = [f"₹{(price * (1 + (zone_hash % 10 - 5) / 100)):,.2f}" for price in base_prices.values()]; data[zone] = prices
    return pd.DataFrame(data)

@st.cache_data
def get_mock_hyperlocal_rent_forecast(loc_city, loc_locality, area_sqft):
    city_hash = hash(loc_city.lower()); np.random.seed(city_hash % (2**32 - 1)); base_rent_psf = 15 + (city_hash % 10)
    rent_multipliers = { t("rent_type_residential"): 1.0, t("rent_type_commercial_retail"): 2.5, t("rent_type_commercial_office"): 1.8, }
    locations_df = get_mock_hyperlocal_price_data(loc_city, loc_locality); forecast_data = []
    for index, row in locations_df.iterrows():
        location_name = row["Location"]; location_modifier = row["Modifier"]; row_data = {t("location_label"): location_name}
        for rent_type, type_multiplier in rent_multipliers.items():
            monthly_rent = (base_rent_psf * type_multiplier * location_modifier) * area_sqft; row_data[rent_type] = monthly_rent
        forecast_data.append(row_data)
    return pd.DataFrame(forecast_data)

@st.cache_data
def get_mock_green_cost_data(loc_city, built_up_area):
    city_hash = hash(loc_city.lower()); np.random.seed(city_hash % (2**32 - 1))
    solar_cost = 250000 * np.random.uniform(0.9, 1.1); rainwater_cost = 80000 * np.random.uniform(0.9, 1.1); insulation_cost_psf = 150 * np.random.uniform(0.9, 1.1)
    roof_area = built_up_area * 0.6; total_insulation_cost = roof_area * insulation_cost_psf
    data = [ {t("green_feature_label"): t("solar_panels_label"), t("estimated_cost_label"): solar_cost, t("notes_label"): t("solar_note")}, {t("green_feature_label"): t("rainwater_harvesting_label"), t("estimated_cost_label"): rainwater_cost, t("notes_label"): t("rainwater_note")}, {t("green_feature_label"): t("heat_insulation_label"), t("estimated_cost_label"): total_insulation_cost, t("notes_label"): t("insulation_note")}, ]
    return pd.DataFrame(data)

@st.cache_data
def get_mock_green_savings_data(cost_df):
    savings_data = cost_df.copy(); annual_savings, payback_periods = [], []
    np.random.seed(hash(cost_df.to_string()) % (2**32 - 1))
    for index, row in savings_data.iterrows():
        cost, feature = row[t("estimated_cost_label")], row[t("green_feature_label")]
        if feature == t("solar_panels_label"): savings = (5 * 4 * 365 * 8) * np.random.uniform(0.95, 1.05)
        elif feature == t("rainwater_harvesting_label"): savings = (10 * 2000) * np.random.uniform(0.9, 1.1)
        elif feature == t("heat_insulation_label"): savings = (40000 * 0.15) * np.random.uniform(0.9, 1.1)
        else: savings = 0
        annual_savings.append(savings); payback = cost / savings if savings > 0 else 0; payback_periods.append(payback)
    savings_data[t("annual_savings_label")] = annual_savings; savings_data[t("payback_period_years_label")] = payback_periods
    return savings_data

def calculate_location_quality_score(amenities, connectivity, pollution, crime):
    score_mapping = { 'Low': 1, 'Medium': 2, 'High': 3, 'Not Important': 1, 'Somewhat': 2, 'Very Important': 3 }
    amenities_score = score_mapping.get(amenities, 1) * 1.2 # Slightly more weight
    connectivity_score = score_mapping.get(connectivity, 1) * 1.2
    pollution_score = (4 - score_mapping.get(pollution, 3)) # Inverted
    crime_score = (4 - score_mapping.get(crime, 3))
    total_score = amenities_score + connectivity_score + pollution_score + crime_score
    max_score = (3 * 1.2) + (3 * 1.2) + 3 + 3
    final_percentage = (total_score / max_score) * 100
    breakdown = {
        t("amenities_label"): {"pref": amenities, "impact": f"+{amenities_score/max_score*100:.0f}"},
        t("connectivity_label"): {"pref": connectivity, "impact": f"+{connectivity_score/max_score*100:.0f}"},
        t("pollution_label"): {"pref": pollution, "impact": f"+{pollution_score/max_score*100:.0f}"},
        t("crime_label"): {"pref": crime, "impact": f"+{crime_score/max_score*100:.0f}"},
    }
    return final_percentage, breakdown

@st.cache_data
def get_mock_comparative_localities_data(city, budget):
    np.random.seed(hash(city.lower()) % (2**32 - 1))
    mock_db = {
        "Nagpur": [
            {"name": "Dharampeth", "price": 9500, "amen": "High", "conn": "High", "poll": "Medium", "crime": "Low", "vibe": "Posh, Commercial Hub"},
            {"name": "Manish Nagar", "price": 6000, "amen": "Medium", "conn": "High", "poll": "Low", "crime": "Low", "vibe": "Modern, Family-Friendly"},
            {"name": "Besa", "price": 4500, "amen": "Medium", "conn": "Medium", "poll": "Low", "crime": "Medium", "vibe": "Developing, Affordable"},
            {"name": "Civil Lines", "price": 11000, "amen": "High", "conn": "High", "poll": "Low", "crime": "Low", "vibe": "Historic, Green, Elite"},
        ],
        "Pune": [
            {"name": "Koregaon Park", "price": 15000, "amen": "High", "conn": "High", "poll": "Medium", "crime": "Low", "vibe": "Elite, Nightlife, Green"},
            {"name": "Hinjawadi", "price": 7500, "amen": "Medium", "conn": "Medium", "poll": "High", "crime": "Medium", "vibe": "IT Hub, Bustling"},
            {"name": "Wakad", "price": 8500, "amen": "High", "conn": "High", "poll": "Medium", "crime": "Low", "vibe": "Well-planned, Family-Oriented"},
            {"name": "Viman Nagar", "price": 11000, "amen": "High", "conn": "High", "poll": "High", "crime": "Low", "vibe": "Near Airport, Upscale"},
        ]
    }
    localities = mock_db.get(city, mock_db["Nagpur"])
    results = []
    for loc in localities:
        score, _ = calculate_location_quality_score(loc["amen"], loc["conn"], loc["poll"], loc["crime"])
        affordable_area = budget / loc["price"] if loc["price"] > 0 else 0
        results.append({
            t("locality_label"): loc["name"],
            t("avg_price_psf_label"): loc["price"],
            t("location_score_label"): int(score),
            t("property_size_for_budget_label"): affordable_area,
            t("vibe_label"): loc["vibe"]
        })
    return pd.DataFrame(results)

# --- NEW MOCK DATA & CONTENT FUNCTIONS ---

@st.cache_data
def get_mock_environmental_risk_data(city, locality):
    seed = hash(city.lower() + locality.lower()) % (2**32 - 1)
    np.random.seed(seed)
    flood_risk = np.random.choice(['Low', 'Medium', 'High'], p=[0.6, 0.3, 0.1])
    eco_risk = np.random.choice(['Low', 'Medium', 'High'], p=[0.7, 0.2, 0.1])
    if any(k in locality.lower() for k in ['river', 'wadi', 'nadi', 'lake', 'talab', 'nullah']):
        flood_risk = np.random.choice(['Medium', 'High'], p=[0.4, 0.6])
    if any(k in locality.lower() for k in ['forest', 'hills', 'park', 'reserve', 'sanctuary']):
        eco_risk = np.random.choice(['Medium', 'High'], p=[0.5, 0.5])
    return {"flood": flood_risk, "eco": eco_risk}

@st.cache_data
def get_mock_vendor_suggestions(city, vendor_type):
    seed = hash(city.lower() + vendor_type.lower()) % (2**32 - 1)
    np.random.seed(seed)
    suggestions = []
    names = {
        'Construction': ["{city} Builders", "Pinnacle Constructions", "Solid Rock Infra", "Dream Homes Pvt. Ltd.", "Vision Associates"],
        'Interiors': ["Creative Corners", "Design Aesthetics", "{city} Interiors", "The Style Studio", "Perfect Finish Designers"],
        'Solar': ["Surya Green Energy", "{city} Solar Solutions", "PowerGrid Solar", "EcoFirst Power", "Sunbeam Installers"],
        'Plumbing': ["Flow-Well Plumbers", "AquaFit Solutions", "The Plumbing Co.", "{city} Piping Experts", "Leak-Proof Systems"],
        'Electrical': ["Sparkline Electricals", "Secure-Volt Co.", "Power-Right Electric", "{city} Wiring Pros", "Ampere Solutions"]
    }
    specialties = {
        'Construction': ["Residential & Commercial", "Luxury Villas", "Affordable Housing", "Turnkey Projects", "Multi-storey Apartments"],
        'Interiors': ["Modern & Minimalist", "Classic & Luxury", "Modular Kitchens", "Commercial Spaces", "Full Home Interiors"],
        'Solar': ["Rooftop Solar", "Industrial Solar", "Solar Water Heaters", "Off-grid Systems", "Govt. Subsidy Advisor"],
        'Plumbing': ["New Installations", "Maintenance & Repair", "Large-scale Projects", "Sanitary Fittings", "Waterproofing"],
        'Electrical': ["Complete House Wiring", "Commercial Installations", "Smart Home Automation", "Safety Audits", "Fixture Installation"]
    }
    vendor_names = names.get(vendor_type, ["Generic Vendor A", "Generic Vendor B", "Generic Vendor C"])
    vendor_specialties = specialties.get(vendor_type, ["General Services"])
    for _ in range(np.random.randint(3, 5)):
        suggestions.append({
            "name": np.random.choice(vendor_names).format(city=city), "specialty": np.random.choice(vendor_specialties),
            "rating": round(np.random.uniform(3.8, 4.9), 1),
            "review": np.random.choice([ "Highly professional and timely delivery.", "Good quality work, slightly over budget.", "Excellent communication and support.", "Recommended for their expertise in the field.", "Satisfactory results, great value for money." ])
        })
    return pd.DataFrame(suggestions).drop_duplicates(subset=['name']).to_dict('records')

def get_loan_subsidy_info(income):
    info = {}
    if income <= 600000: pmay_status = f"With an annual income of ₹{income:,.0f}, you may be eligible for PMAY under the **EWS/LIG** category, offering the highest interest subsidy."
    elif 600001 <= income <= 1200000: pmay_status = f"With an annual income of ₹{income:,.0f}, you may be eligible for PMAY under the **MIG-I** category."
    elif 1200001 <= income <= 1800000: pmay_status = f"With an annual income of ₹{income:,.0f}, you may be eligible for PMAY under the **MIG-II** category."
    else: pmay_status = f"With an income above ₹18,00,000, you are likely not eligible for the PMAY Credit-Linked Subsidy Scheme (CLSS)."
    info['pmay'] = pmay_status + " **Please verify the current scheme status and exact eligibility criteria with your lending bank, as scheme details can change.**"
    info['tax'] = "*   **Section 24(b):** Claim a deduction of up to **₹2,00,000** on the interest paid on your home loan for a self-occupied property.\n*   **Section 80C:** The principal amount repaid is eligible for a deduction of up to **₹1,50,000** (within the overall 80C limit).\n*   **Joint Loan:** If co-owned and the loan is joint, each co-owner can claim these deductions individually, potentially doubling the tax benefit."
    info['tips'] = "*   **Credit Score:** A score above 750 is ideal for the best interest rates. Check your score before applying.\n*   **Compare Lenders:** Don't just go with your salary account bank. Compare rates, processing fees, and prepayment charges across multiple banks and NBFCs.\n*   **Required Documents:** You will typically need Identity/Address Proof (PAN, Aadhaar), Income Proof (Salary Slips, Form 16, ITR), and Property Documents (Sale Agreement, Title Deed)."
    return info


# ─────────────────────────────────────────────────────────────────────────────
# UI Rendering Functions
# ─────────────────────────────────────────────────────────────────────────────
def render_flat_specifics():
    st.markdown(f"##### {t('flat_details_header')}")
    st.selectbox(t('flat_size_label'), ['1BHK', '2BHK', '3BHK', '4BHK+', 'Penthouse', 'Studio', 'Custom'], key='plan_flat_size')

def render_plot_and_fsi_details():
    st.markdown(f"#### {t('plot_construction_potential_header')}")
    c1, c2 = st.columns(2)
    with c1:
        st.number_input(t('plot_area_label'), min_value=300.0, value=float(st.session_state.get('plan_plot_area', 1200.0)), step=100.0, key='plan_plot_area', format="%.2f")
        st.number_input(t('fsi_label'), min_value=0.5, max_value=5.0, value=float(st.session_state.get('fsi_value', 1.5)), step=0.1, key='fsi_value', help=t('fsi_help'), format="%.2f")
    with c2:
        plot_area = st.session_state.get('plan_plot_area', 0.0); fsi = st.session_state.get('fsi_value', 0.0)
        max_area = plot_area * fsi if plot_area > 0 and fsi > 0 else 0
        st.metric(label=t('max_construction_area_label'), value=f"{max_area:,.0f} sq. ft")
    st.divider()

def render_build_specifics():
    st.markdown(f"##### {t('construction_details_header')}")
    st.number_input(t('built_up_area_label'), min_value=200.0, value=float(st.session_state.get('plan_built_up', 1800.0)), step=100.0, key='plan_built_up', format="%.2f")
    st.number_input(t('floors_label'), min_value=1, value=int(st.session_state.get('plan_floors', 2)), key='plan_floors')
    st.checkbox(t('extra_floors_rent_checkbox'), key='extra_floors_rent')
    st.selectbox(t('contract_type_label'), ['With Material (Turnkey)', 'Without Material (Labor Only)'], key='const_contract')
    st.multiselect(t('vendors_label'), ['Plumbing', 'Electrical', 'Tiles', 'Paint', 'Solar', 'Interiors', 'CCTV', 'Automation', 'Landscaping'], key='const_vendors')
    st.multiselect(t('green_features_label'), ['Solar Panels', 'Rainwater Harvesting', 'Heat Insulation', 'EV Charging Point', 'Greywater Recycling'], key='const_green')
    st.slider(t('timeline_label'), 3, 36, value=int(st.session_state.get('const_timeline', 12)), key='const_timeline')

def render_investment_specifics(purpose):
    if "Rental" in purpose or t('rental_income') in purpose: st.number_input(t('target_rent_label'), min_value=0, step=1000, key='fin_target_rent')
    if "Resale" in purpose or t('resale_investment') in purpose: st.number_input(t('target_resale_label'), min_value=0, step=100000, key='fin_target_resale')

def sync_investment_shares(source):
    if source == 'p1': st.session_state.investment_share_p2 = 100.0 - st.session_state.investment_share_p1
    else: st.session_state.investment_share_p1 = 100.0 - st.session_state.investment_share_p2

def render_mixed_investment_specifics():
    st.markdown(f"#### {t('mixed_investment_header')}")
    st.checkbox(t('is_joint_investment_checkbox'), key='is_joint_investment')
    if st.session_state.get('is_joint_investment'):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input(t('co_owner_name_label'), key='co_owner_name'); st.slider(t('investment_share_p1_label'), 0.0, 100.0, key='investment_share_p1', on_change=sync_investment_shares, args=('p1',))
        with c2:
            rel_options_keys = ['relationship_spouse', 'relationship_parent', 'relationship_sibling', 'relationship_business', 'relationship_other']
            rel_options_display = [t(k) for k in rel_options_keys]
            st.selectbox(t('co_owner_relationship_label'), options=rel_options_display, key='co_owner_relationship'); st.slider(t('investment_share_p2_label'), 0.0, 100.0, key='investment_share_p2', on_change=sync_investment_shares, args=('p2',))
    st.divider()

# --- Advanced Tool Renderers ---
def render_build_vs_buy_tool():
    st.subheader(f"🆚 {t('tool_build_vs_buy_title')}"); st.info(t('tool_build_vs_buy_info'))
    data = get_mock_build_vs_buy_data(st.session_state.get('loc_city'), st.session_state.get('plan_plot_area'), st.session_state.get('plan_built_up'))
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader(t('build_cost_header')); st.metric(t('land_cost'), f"₹{data['build']['land']:,.0f}"); st.metric(t('construction_cost'), f"₹{data['build']['construction']:,.0f}"); st.metric(t('other_costs'), f"₹{data['build']['other']:,.0f}")
            st.metric(t('total_build_cost'), f"₹{data['build']['total']:,.0f}", delta_color="off")
    with col2:
        with st.container(border=True):
            st.subheader(t('buy_cost_header')); st.metric(t('property_price'), f"₹{data['buy']['total_single_flat']:,.0f}"); st.empty(); st.empty(); st.empty()
    st.divider(); st.subheader(t('breakeven_analysis_header'))
    with st.container(border=True):
        c1, c2, c3 = st.columns(3); c1.metric(t('num_flats_to_build_label'), f"{data['build']['num_flats']} units", help="Calculated based on your target built-up area and a standard flat size of 900 sq.ft.")
        cost_per_built = data['build']['cost_per_flat']; cost_to_buy = data['buy']['total_single_flat']
        delta = cost_per_built - cost_to_buy; delta_percent = (delta / cost_to_buy) * 100 if cost_to_buy > 0 else 0
        c2.metric(t('cost_per_flat_build_label'), f"₹{cost_per_built:,.0f}"); c3.metric(t('price_ready_flat_label'), f"₹{cost_to_buy:,.0f}", f"{delta_percent:.1f}% vs Buying", delta_color="inverse")
        comparison_text = f"{abs(delta_percent):.1f}% cheaper" if delta < 0 else f"{delta_percent:.1f}% more expensive"
        conclusion = t('build_vs_buy_conclusion').format(total_build_cost=data['build']['total'], num_flats=data['build']['num_flats'], cost_per_flat=cost_per_built, comparison=comparison_text, buy_price=cost_to_buy); st.info(conclusion)

def render_locality_compare_tool():
    st.subheader(f"🏘️ {t('tool_locality_compare_title')}"); st.info(t('tool_locality_compare_info'))
    locality = st.session_state.get('loc_locality') or 'your area'; base_rate = 6000 + (hash(st.session_state.get('loc_city').lower() + locality.lower()) % 3000)
    price_data = [ {"Location": t('location_on_main_road'), "Price per sq.ft (₹)": f"₹{base_rate:,.0f}"}, {"Location": t('location_slightly_interior'), "Price per sq.ft (₹)": f"₹{int(base_rate * 0.90):,.0f}"}, {"Location": t('location_interior'), "Price per sq.ft (₹)": f"₹{int(base_rate * 0.82):,.0f}"}, {"Location": t('location_deep_interior'), "Price per sq.ft (₹)": f"₹{int(base_rate * 0.70):,.0f}"}, ]
    with st.container(border=True): st.subheader(t('locality_price_table_header').format(locality=locality.title())); st.dataframe(pd.DataFrame(price_data), use_container_width=True, hide_index=True)

def render_resale_predictor_tool():
    st.subheader(f"📈 {t('tool_resale_predictor_title')}"); st.info(t('tool_resale_predictor_info'))
    with st.container(border=True):
        size = st.number_input(t('property_size_label'), min_value=300.0, value=float(st.session_state.get('plan_built_up') or st.session_state.get('plan_plot_area') or 1200.0), step=50.0)
        data = get_mock_resale_projection_data(st.session_state.get('loc_city'), st.session_state.get('loc_locality'), size)
        st.subheader(t('resale_projection_header').format(years=10, size=f"{size:,.0f}")); c1, c2, c3 = st.columns(3)
        c1.metric(t('current_value_label'), f"₹{data['current_value']:,.0f}"); c2.metric(t('projected_value_label'), f"₹{data['projected_value_10y']:,.0f}"); c3.metric(t('annual_growth_rate_label'), f"{data['growth_rate']:.2%}")
        st.dataframe(data['table'], use_container_width=True, hide_index=True)

def render_sqft_breakdown_tool():
    st.subheader(f"🧱 {t('tool_sqft_breakdown_title')}"); st.info(t('tool_sqft_breakdown_info'))
    data = get_mock_detailed_sqft_costs(st.session_state.get('loc_city')); total_budget = st.session_state.get('fin_budget', 0)
    def process_df(df, budget):
        cost_col, percent_col, price_col = t("cost_sqft_label"), t("cost_as_percent_label"), t("cost_price_label"); total_cost_psf = df[cost_col].sum(); df[percent_col] = (df[cost_col] / total_cost_psf) * 100
        if budget > 0: df[price_col] = (df[percent_col] / 100) * (budget * 0.6)
        else: df[price_col] = 0
        return df
    with st.container(border=True):
        tab1, tab2 = st.tabs([t('house_construction_tab'), t('flat_interiors_tab')]); column_order = [t("cost_item_label"), t("cost_sqft_label"), t("cost_as_percent_label"), t("cost_price_label")]
        column_config = {t("cost_sqft_label"): st.column_config.NumberColumn(format="₹%d"), t("cost_as_percent_label"): st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100), t("cost_price_label"): st.column_config.NumberColumn(format="₹%,.0f")}
        with tab1: st.dataframe(process_df(data['house'], total_budget)[column_order], use_container_width=True, hide_index=True, column_config=column_config)
        with tab2: st.dataframe(process_df(data['flat'], total_budget)[column_order], use_container_width=True, hide_index=True, column_config=column_config)

def render_contract_diff_tool():
    st.subheader(f"⚖️ {t('tool_contract_diff_title')}"); st.info(t('tool_contract_diff_info'))
    city = st.session_state.get('loc_city') or 'your city'; data = get_mock_material_prices_by_area(st.session_state.get('loc_city'))
    with st.container(border=True): st.subheader(t('material_prices_header').format(city=city.title())); st.dataframe(data, use_container_width=True, hide_index=True)

def render_rent_forecaster_tool():
    st.subheader(f"💰 {t('tool_rent_forecaster_title')}"); st.info(t('tool_rent_forecaster_info'))
    with st.container(border=True):
        size = st.number_input(t('property_size_label'), min_value=300.0, value=float(st.session_state.get('plan_built_up') or 1000.0), step=50.0)
        rent_df = get_mock_hyperlocal_rent_forecast(st.session_state.get('loc_city'), st.session_state.get('loc_locality'), size)
        st.subheader(t('forecast_monthly_rent_label'))
        st.dataframe(rent_df, use_container_width=True, hide_index=True, column_config={t("rent_type_residential"): st.column_config.NumberColumn(format="₹%,.0f"), t("rent_type_commercial_retail"): st.column_config.NumberColumn(format="₹%,.0f"), t("rent_type_commercial_office"): st.column_config.NumberColumn(format="₹%,.0f")})

def render_payback_calculator_tool():
    st.subheader(f"⏳ {t('tool_payback_calculator_title')}"); st.info(t('tool_payback_calculator_info'))
    with st.container(border=True):
        total_cost = st.session_state.get('fin_budget', 5000000); built_up_area = st.session_state.get('plan_built_up', 1000.0)
        rent_df = get_mock_hyperlocal_rent_forecast(st.session_state.get('loc_city'), st.session_state.get('loc_locality'), built_up_area); payback_df = rent_df.copy()
        net_income_multipliers = { t("rent_type_residential"): (1 - 0.25), t("rent_type_commercial_retail"): (1 - 0.20), t("rent_type_commercial_office"): (1 - 0.15)}
        for rent_type, multiplier in net_income_multipliers.items():
            if rent_type in payback_df.columns:
                net_annual_rent = (payback_df[rent_type] * 12 * multiplier); payback_df[rent_type] = total_cost / net_annual_rent.where(net_annual_rent > 0, np.nan)
        st.subheader(t('payback_period_label'))
        st.dataframe(payback_df, use_container_width=True, hide_index=True, column_config={t("rent_type_residential"): st.column_config.NumberColumn(format="%.1f Yrs"), t("rent_type_commercial_retail"): st.column_config.NumberColumn(format="%.1f Yrs"), t("rent_type_commercial_office"): st.column_config.NumberColumn(format="%.1f Yrs")})

def render_green_cost_estimator_tool():
    st.subheader(f"🌱 {t('tool_green_cost_estimator_title')}"); st.info(t('tool_green_cost_estimator_info'))
    with st.container(border=True):
        built_up_area = st.session_state.get('plan_built_up', 1800.0); cost_df = get_mock_green_cost_data(st.session_state.get('loc_city'), built_up_area)
        st.dataframe(cost_df, use_container_width=True, hide_index=True, column_config={ t("estimated_cost_label"): st.column_config.NumberColumn(format="₹%,.0f") })

def render_green_savings_predictor_tool():
    st.subheader(f"💸 {t('tool_green_savings_predictor_title')}"); st.info(t('tool_green_savings_predictor_info'))
    with st.container(border=True):
        built_up_area = st.session_state.get('plan_built_up', 1800.0); cost_df = get_mock_green_cost_data(st.session_state.get('loc_city'), built_up_area); savings_df = get_mock_green_savings_data(cost_df)
        st.dataframe(savings_df, use_container_width=True, hide_index=True, column_config={ t("estimated_cost_label"): st.column_config.NumberColumn(format="₹%,.0f", help="The initial one-time cost for installation."), t("annual_savings_label"): st.column_config.NumberColumn(format="₹%,.0f", help="Estimated money saved per year on utility bills."), t("payback_period_years_label"): st.column_config.NumberColumn(format="%.1f Yrs", help="The time it takes for savings to cover the initial cost.") })

def render_location_quality_tool():
    st.subheader(f"⭐ {t('tool_location_quality_title')}"); st.info(t('tool_location_quality_info'))
    with st.container(border=True):
        score, breakdown = calculate_location_quality_score( st.session_state.qual_amenities, st.session_state.qual_connectivity, st.session_state.risk_pollution, st.session_state.risk_crime)
        st.subheader(t('your_location_score_label')); st.progress(int(score), text=f"{score:.0f}/100")
        st.subheader(t('score_breakdown_header')); c1, c2, c3, c4 = st.columns(4)
        cols = [c1, c2, c3, c4]
        for i, (factor, values) in enumerate(breakdown.items()):
            with cols[i]: st.metric(label=factor, value=values["pref"], delta=values["impact"], delta_color="off")

def render_compare_localities_tool():
    st.subheader(f"🔭 {t('tool_compare_localities_title')}"); st.info(t('tool_compare_localities_info'))
    city = st.session_state.get('loc_city', 'Nagpur'); budget = st.session_state.get('fin_budget', 5000000)
    with st.container(border=True):
        st.markdown(f"{t('your_target_locality_label')}: **{st.session_state.get('loc_locality', 'N/A')}**")
        st.markdown(f"{t('for_your_budget_label')} **₹{budget:,.0f}**, {t('you_can_get_label')} **`size`** {t('sq_ft_label')}")
        st.divider()
        st.subheader(t('alternative_localities_header').format(city=city))
        df = get_mock_comparative_localities_data(city, budget)
        st.dataframe(df, use_container_width=True, hide_index=True, column_config={
            t("avg_price_psf_label"): st.column_config.NumberColumn(format="₹%,.0f"),
            t("location_score_label"): st.column_config.ProgressColumn(format="%d/100", min_value=0, max_value=100),
            t("property_size_for_budget_label"): st.column_config.NumberColumn(format="%,.0f sq.ft.")
        })

# --- NEW TOOL RENDERERS ---

def render_environmental_risk_tool():
    st.subheader(f"🏞️ {t('tool_env_risk_title')}"); st.info(t('tool_env_risk_info'))
    risk_data = get_mock_environmental_risk_data(st.session_state.get('loc_city', ''), st.session_state.get('loc_locality', ''))
    with st.container(border=True):
        st.subheader(f"{t('risk_assessment_for_label')} {st.session_state.get('loc_locality', 'N/A').title()}, {st.session_state.get('loc_city', 'N/A').title()}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{t('flood_risk_label')}**")
            risk_level = risk_data['flood']
            if risk_level == 'High': st.error(f"**{t('risk_level_high')}** 💧", icon="🚨"); st.warning(t('risk_advice_high'))
            elif risk_level == 'Medium': st.warning(f"**{t('risk_level_medium')}** 💧", icon="⚠️"); st.info(t('risk_advice_medium'))
            else: st.success(f"**{t('risk_level_low')}** 💧", icon="✅"); st.markdown(t('risk_advice_low'))
        with c2:
            st.markdown(f"**{t('eco_risk_label')}**")
            risk_level = risk_data['eco']
            if risk_level == 'High': st.error(f"**{t('risk_level_high')}** 🌳", icon="🚨"); st.warning(t('risk_advice_high'))
            elif risk_level == 'Medium': st.warning(f"**{t('risk_level_medium')}** 🌳", icon="⚠️"); st.info(t('risk_advice_medium'))
            else: st.success(f"**{t('risk_level_low')}** 🌳", icon="✅"); st.markdown(t('risk_advice_low'))

def render_vendor_suggestion_tool():
    st.subheader(f"👷 {t('tool_vendor_suggestion_title')}"); st.info(t('tool_vendor_suggestion_info'))
    vendor_map = { 'Plumbing': 'Plumbing', 'Electrical': 'Electrical', 'Solar': 'Solar', 'Interiors': 'Interiors' }
    user_needs = [vendor_map[v] for v in st.session_state.get('const_vendors', []) if v in vendor_map]
    all_vendor_types = ['Construction', 'Interiors', 'Solar', 'Plumbing', 'Electrical']
    sorted_vendor_types = sorted(list(set(user_needs + all_vendor_types)), key=lambda x: (x not in user_needs))
    selected_type = st.selectbox(t('vendor_type_label'), options=sorted_vendor_types)
    if selected_type:
        with st.spinner(f"Searching for {selected_type} vendors in {st.session_state.get('loc_city', 'your city')}..."):
            suggestions = get_mock_vendor_suggestions(st.session_state.get('loc_city', ''), selected_type)
            if not suggestions: st.warning("No suggestions found for this category.")
            else:
                for vendor in suggestions:
                    with st.container(border=True):
                        c1, c2 = st.columns([3, 1])
                        with c1: st.subheader(vendor['name']); st.caption(f"{t('vendor_specialty_label')}: {vendor['specialty']}"); st.markdown(f"*{vendor['review']}*")
                        with c2: st.metric(label=t('vendor_rating_label'), value=f"{vendor['rating']} ⭐")

def render_loan_guide_tool():
    st.subheader(f"🏦 {t('tool_loan_guide_title')}"); st.info(t('tool_loan_guide_info'))
    info = get_loan_subsidy_info(st.session_state.get('income', 0))
    if not st.session_state.get('fin_loan'): st.info("You indicated you do not need a loan. This guide is for general information.")
    with st.expander(f"**{t('pmay_guide_header')}**", expanded=True):
        st.subheader(t('pmay_eligibility_header')); st.markdown(info['pmay'])
    with st.expander(f"**{t('tax_benefits_header')}**"): st.markdown(info['tax'])
    with st.expander(f"**{t('loan_tips_header')}**"): st.markdown(info['tips'])


# ─────────────────────────────────────────────────────────────────────────────
# Main UI Display Functions
# ─────────────────────────────────────────────────────────────────────────────
def display_sidebar():
    with st.sidebar:
        language_map = {lang_code: details['language_name'] for lang_code, details in TRANSLATIONS.items()}
        TRANSLATIONS['en']['location_on_main_road'] = "On Main Road"; TRANSLATIONS['en']['location_slightly_interior'] = "Slightly Interior"; TRANSLATIONS['en']['location_interior'] = "Interior"; TRANSLATIONS['en']['location_deep_interior'] = "Deep Interior"
        for lang in ['hi', 'mr']:
            for key, value in TRANSLATIONS['en'].items():
                if key not in TRANSLATIONS[lang]: TRANSLATIONS[lang][key] = value
        selected_language_name = st.selectbox("Language / भाषा", options=language_map.values(), index=list(language_map.keys()).index(st.session_state.language))
        new_lang_code = next(code for code, name in language_map.items() if name == selected_language_name)
        if new_lang_code != st.session_state.language:
            st.session_state.language = new_lang_code; st.rerun()
        st.title(f"🗂️ {t('project_manager_title')}")
        if st.session_state.selected_project:
            with st.container(border=True):
                st.caption(t('active_project_caption')); st.subheader(st.session_state.selected_project)
                if st.button(t('switch_project_button'), use_container_width=True):
                    lang = st.session_state.language; st.session_state.clear(); st.session_state.language, st.session_state.step = lang, 0; st.rerun()
                with st.expander(t('danger_zone_header')):
                    if st.checkbox(t('delete_confirm_checkbox'), key="delete_confirm"):
                        if st.button(t('delete_project_button'), type="primary", use_container_width=True):
                            if delete_project(st.session_state.selected_project):
                                lang = st.session_state.language; st.session_state.clear(); st.session_state.language, st.session_state.step = lang, 0; st.rerun()
            st.divider()
        with st.container(border=True):
            st.subheader(t('create_new_project_header'))
            with st.form("new_project_form"):
                new_project_name = st.text_input(t('new_project_name_label'), key="new_proj_name").strip()
                if st.form_submit_button(t('start_new_project_button'), use_container_width=True):
                    if new_project_name:
                        if new_project_name in get_saved_projects(): st.error(t('project_name_exists_error'))
                        else:
                            lang = st.session_state.language; st.session_state.clear(); st.session_state.language, st.session_state.step = lang, 1
                            st.session_state.selected_project = new_project_name; st.rerun()
                    else: st.warning(t('enter_project_name_warning'))
        saved_projects = get_saved_projects()
        if saved_projects:
            with st.container(border=True):
                st.subheader(t('load_existing_project_header'))
                selected_to_load = st.selectbox(t('select_project_placeholder'), options=saved_projects, index=None, placeholder=t('select_project_placeholder'))
                if st.button(t('load_project_button'), use_container_width=True, disabled=not selected_to_load):
                    load_project(selected_to_load); st.rerun()
        st.info(t('disclaimer_info'), icon="📢")

def display_step1_user_details():
    st.subheader(t('step1_header'))
    with st.form("user_details_form"):
        c1, c2 = st.columns(2)
        with c1: st.text_input(t('full_name_label'), key='name'); st.date_input(t('dob_label'), min_value=date(1940, 1, 1), max_value=date.today(), key='dob')
        with c2: st.text_input(t('contact_label'), key='contact'); st.number_input(t('income_label'), min_value=100000, step=50000, key='income', format="%d")
        if st.form_submit_button(t('next_goal_button'), use_container_width=True, type="primary"):
            if all([st.session_state.name, st.session_state.contact, st.session_state.dob, st.session_state.income]):
                st.session_state.step = 2; st.rerun()
            else: st.error(t('fill_all_details_error'))

def display_step2_intent():
    st.subheader(t('step2_header'))
    with st.form("intent_form"):
        intent_options = { 'buy_flat': t('buy_flat'), 'build_house': t('build_house'), 'buy_plot': t('buy_plot'), 'mixed_investment': t('mixed_investment') }
        current_intent_val = t(st.session_state.get('intent_type', 'buy_flat')); current_index = list(intent_options.values()).index(current_intent_val) if current_intent_val in list(intent_options.values()) else 0
        st.session_state.intent_type_display = st.selectbox(t('select_goal_label'), options=list(intent_options.values()), index=current_index)
        
        c1, c2 = st.columns([1, 4])
        with c1:
            back_clicked = st.form_submit_button(t('back_button_text'))
        with c2:
            next_clicked = st.form_submit_button(t('next_specifics_button'), type="primary")

        if next_clicked:
            st.session_state.intent_type = next(key for key, value in intent_options.items() if value == st.session_state.intent_type_display)
            st.session_state.step = 3
            st.rerun()
        if back_clicked:
            st.session_state.step = 1
            st.rerun()

def display_step3_details():
    intent_type_key, intent_type_display = st.session_state.get('intent_type', 'buy_flat'), t(st.session_state.get('intent_type', 'buy_flat'))
    st.subheader(t('step3_header').format(intent_type=intent_type_display))
    with st.form("details_form"):
        st.markdown(f"#### {t('location_budget_header')}"); c1, c2 = st.columns(2)
        with c1: st.text_input(t('target_city_label'), key='loc_city'); st.text_input(t('localities_label'), key='loc_locality')
        with c2: st.text_input(t('pincode_label'), max_chars=6, key='loc_pincode'); st.number_input(t('budget_label'), min_value=100000, step=100000, key='fin_budget')
        c3, c4 = st.columns(2)
        with c3: st.checkbox(t('need_loan_checkbox'), key='fin_loan');
        with c4: st.checkbox(t('subsidy_checkbox'), key='fin_subsidy')
        purpose_options = {'self_use': t('self_use'), 'rental_income': t('rental_income'), 'resale_investment': t('resale_investment')}
        current_purpose_val = t(st.session_state.get('intent_purpose', 'self_use')); current_purpose_idx = list(purpose_options.values()).index(current_purpose_val) if current_purpose_val in list(purpose_options.values()) else 0
        st.session_state.intent_purpose_display = st.selectbox(t('main_purpose_label'), options=list(purpose_options.values()), index=current_purpose_idx)
        st.divider()
        if intent_type_key == 'mixed_investment': render_mixed_investment_specifics()
        components_to_render = []
        if intent_type_key == 'mixed_investment':
            mixed_options = {'buy_flat': t('buy_flat'), 'build_house': t('build_house'), 'buy_plot': t('buy_plot')}
            default_mixed = [t(c) for c in st.session_state.get('mixed_components',[])]
            st.session_state.mixed_components_display = st.multiselect(t('mixed_components_label'), options=list(mixed_options.values()), default=default_mixed)
            components_to_render = [key for key, value in mixed_options.items() if value in st.session_state.mixed_components_display]
        else: components_to_render = [intent_type_key]
        if 'buy_flat' in components_to_render: render_flat_specifics()
        if any(c in components_to_render for c in ['build_house', 'buy_plot']): render_plot_and_fsi_details()
        if 'build_house' in components_to_render: render_build_specifics()
        st.divider()
        st.markdown(f"#### {t('preferences_concerns_header')}"); c5, c6 = st.columns(2)
        with c5: st.select_slider(t('connectivity_label'), ['Low', 'Medium', 'High'], key='qual_connectivity'); st.select_slider(t('amenities_label'), ['Not Important', 'Somewhat', 'Very Important'], key='qual_amenities')
        with c6: st.select_slider(t('pollution_label'), ['Low', 'Medium', 'High'], key='risk_pollution'); st.select_slider(t('crime_label'), ['Low', 'Medium', 'High'], key='risk_crime')
        if st.session_state.intent_purpose_display in [t('rental_income'), t('resale_investment')]:
            st.markdown(f"##### {t('investment_goals_header')}"); render_investment_specifics(st.session_state.intent_purpose_display)
        
        
        c1_nav, c2_nav = st.columns([1, 4])
        with c1_nav:
             back_clicked = st.form_submit_button(t('back_button_text'))
        with c2_nav:
            save_clicked = st.form_submit_button(t('save_proceed_button'), type="primary")

        if save_clicked:
            st.session_state.intent_purpose = next(key for key, value in purpose_options.items() if value == st.session_state.intent_purpose_display)
            if 'mixed_components_display' in st.session_state: st.session_state.mixed_components = components_to_render
            if save_project(): st.session_state.step = 4; st.rerun()
        if back_clicked:
            st.session_state.step = 2
            st.rerun()


def display_step4_analysis():
    st.subheader(t('step4_header')); st.success(t('project_saved_success'))
    project_details = {key: st.session_state.get(key) for key in CSV_COLUMNS if st.session_state.get(key) not in [None, '']}
    with st.expander(t('view_details_expander')):
        display_details = {key.replace('_', ' ').title(): val for key, val in project_details.items() if val and key != 'project_name'}
        st.json(display_details)
    st.divider()
    city = project_details.get('loc_city', "Your City"); st.subheader(t('market_snapshot_header').format(city=city.title())); st.dataframe(get_price_data(city), use_container_width=True, hide_index=True); st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(t('generate_strategy_button'), type="primary", use_container_width=True):
            prompt = build_initial_prompt(project_details, st.session_state.language)
            with st.spinner(t('analyzing_spinner')): st.session_state.ai_response = ask_gemini(prompt)
            st.session_state.follow_up_response = None
    with col2:
        if st.button(t('edit_details_button'), use_container_width=True): 
            st.session_state.step = 3
            st.rerun()

    if st.session_state.get('ai_response'):
        st.markdown("---"); col1, col2 = st.columns([3,1])
        with col1: st.subheader(t('strategy_header'))
        with col2:
            if st.button(t('print_report_button'), use_container_width=True): st.components.v1.html("<script>window.print()</script>", height=0)
        st.markdown(st.session_state.ai_response, unsafe_allow_html=True); st.markdown("---")
        with st.expander(t('follow_up_expander')):
            question = st.text_area(t('follow_up_expander'), placeholder=t('follow_up_placeholder'))
            if st.button(t('ask_advisor_button')):
                if question:
                    prompt = build_follow_up_prompt(project_details, st.session_state.ai_response, question, st.session_state.language)
                    with st.spinner(t('thinking_spinner')): st.session_state.follow_up_response = ask_gemini(prompt, temperature=0.5)
                else: st.warning(t('enter_question_warning'))
        if st.session_state.get('follow_up_response'): st.info(st.session_state.follow_up_response)
        st.divider()
        st.subheader(t('advanced_tools_header'))

        st.markdown(f"##### 📈 {t('analysis_projections_header')}")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button(f"🆚 {t('tool_build_vs_buy_button')}", use_container_width=True): st.session_state.active_tool = 'build_vs_buy'; st.rerun()
        if c2.button(f"📈 {t('tool_resale_predictor_button')}", use_container_width=True): st.session_state.active_tool = 'resale_predictor'; st.rerun()
        if c3.button(f"💰 {t('tool_rent_forecaster_button')}", use_container_width=True): st.session_state.active_tool = 'rent_forecaster'; st.rerun()
        if c4.button(f"⏳ {t('tool_payback_calculator_button')}", use_container_width=True): st.session_state.active_tool = 'payback_calculator'; st.rerun()

        st.markdown(f"##### {t('location_intelligence_header')}")
        c5, c6, c7, c8 = st.columns(4)
        if c5.button(f"🏘️ {t('tool_locality_compare_button')}", use_container_width=True): st.session_state.active_tool = 'locality_compare'; st.rerun()
        if c6.button(f"⭐ {t('tool_location_quality_button')}", use_container_width=True): st.session_state.active_tool = 'location_quality'; st.rerun()
        if c7.button(f"🔭 {t('tool_compare_localities_button')}", use_container_width=True): st.session_state.active_tool = 'compare_localities'; st.rerun()
        if c8.button(f"🏞️ {t('tool_env_risk_button')}", use_container_width=True): st.session_state.active_tool = 'environmental_risk'; st.rerun()

        st.markdown(f"##### 🧱 {t('cost_construction_header')}")
        c9, c10, c11, _ = st.columns(4)
        if c9.button(f"🧱 {t('tool_sqft_breakdown_button')}", use_container_width=True): st.session_state.active_tool = 'sqft_breakdown'; st.rerun()
        if c10.button(f"⚖️ {t('tool_contract_diff_button')}", use_container_width=True): st.session_state.active_tool = 'contract_diff'; st.rerun()
        if c11.button(f"👷 {t('tool_vendor_suggestion_button')}", use_container_width=True): st.session_state.active_tool = 'vendor_suggestion'; st.rerun()

        st.markdown(f"##### 💸 {t('financial_green_header')}")
        c12, c13, c14, _ = st.columns(4)
        if c12.button(f"🏦 {t('tool_loan_guide_button')}", use_container_width=True): st.session_state.active_tool = 'loan_guide'; st.rerun()
        if c13.button(f"🌱 {t('tool_green_cost_estimator_button')}", use_container_width=True): st.session_state.active_tool = 'green_cost_estimator'; st.rerun()
        if c14.button(f"💸 {t('tool_green_savings_predictor_button')}", use_container_width=True): st.session_state.active_tool = 'green_savings_predictor'; st.rerun()

def display_advanced_tool_ui():
    if st.button(t('back_to_analysis_button')):
        st.session_state.active_tool = None; st.rerun()
    st.divider()
    tool = st.session_state.active_tool
    if tool == 'build_vs_buy': render_build_vs_buy_tool()
    elif tool == 'locality_compare': render_locality_compare_tool()
    elif tool == 'resale_predictor': render_resale_predictor_tool()
    elif tool == 'sqft_breakdown': render_sqft_breakdown_tool()
    elif tool == 'contract_diff': render_contract_diff_tool()
    elif tool == 'rent_forecaster': render_rent_forecaster_tool()
    elif tool == 'payback_calculator': render_payback_calculator_tool()
    elif tool == 'green_cost_estimator': render_green_cost_estimator_tool()
    elif tool == 'green_savings_predictor': render_green_savings_predictor_tool()
    elif tool == 'location_quality': render_location_quality_tool()
    elif tool == 'compare_localities': render_compare_localities_tool()
    elif tool == 'environmental_risk': render_environmental_risk_tool()
    elif tool == 'vendor_suggestion': render_vendor_suggestion_tool()
    elif tool == 'loan_guide': render_loan_guide_tool()

def calculate_age(born):
    if not isinstance(born, date): return "N/A"
    today = date.today(); return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

# ─────────────────────────────────────────────────────────────────────────────
# AI Prompt Engineering Functions
# ─────────────────────────────────────────────────────────────────────────────
def build_initial_prompt(details, lang_code):
    language_name = TRANSLATIONS[lang_code]['language_name']
    client_profile = f"**CLIENT'S BASE PROFILE:**\n- Name: {details.get('name', 'User')}\n- Age: {calculate_age(st.session_state.get('dob'))} years\n- Annual Income: ₹{int(details.get('income', 0)):,}\n- Primary Goal: {t(details.get('intent_type', 'N/A'))}\n- Main Purpose: {t(details.get('intent_purpose', 'N/A'))}\n- Target City: {details.get('loc_city', 'N/A')}\n- Total Budget: ₹{int(details.get('fin_budget', 0)):,}\n- Needs Loan: {'Yes' if details.get('fin_loan') else 'No'}\n"
    if details.get('is_joint_investment') and details.get('co_owner_name'): client_profile += f"\n**JOINT INVESTMENT DETAILS:**\n- Co-Owner: {details.get('co_owner_name')} ({details.get('co_owner_relationship')})\n- Investment Share: {details.get('name')} ({details.get('investment_share_p1')}%) / {details.get('co_owner_name')} ({details.get('investment_share_p2')}%)\n"
    intent_type, plot_area, fsi = details.get('intent_type'), float(details.get('plan_plot_area', 0)), float(details.get('fsi_value', 0))
    if intent_type in ['build_house', 'buy_plot'] or (intent_type == 'mixed_investment' and any(c in details.get('mixed_components', []) for c in ['build_house', 'buy_plot'])):
        if plot_area > 0 and fsi > 0: client_profile += f"\n**CONSTRUCTION CONSTRAINTS:**\n- Plot Area: {plot_area:,.0f} sq. ft\n- Floor Space Index (FSI): {fsi}\n- Maximum Permissible Construction Area: {plot_area * fsi:,.0f} sq. ft\n"
    return textwrap.dedent(f"""Act as a meticulous financial real estate analyst in India. Your goal is to provide a report that is 85% quantitative data, in clear Markdown tables. IMPORTANT: Your entire response, including all headers, table content, and text, MUST be in the {language_name} language.
        {client_profile}
        **MARKET DATA for {details.get('loc_city', 'your city')}:**\n{get_price_data(details.get('loc_city', '')).to_markdown(index=False)}
        ---
        **YOUR TASK: Generate a detailed, number-focused financial report. If the investment is joint, acknowledge this. If building a house or analyzing a plot, you MUST respect the 'Maximum Permissible Construction Area' constraint in your recommendations.**
        ### 1. Financial Snapshot\n- **Total Estimated Project Cost:** (Use client's budget)\n- **Down Payment (20%):**\n- **Loan Amount (80%):**\n- **Estimated EMI:** (Assume 20-year loan at 8.7% interest)\n- **EMI as % of Monthly Income:**
        ### 2. Detailed Cost Breakdown (Table)\n| Item | Amount (₹) | Notes |\n|---|---|---|\n| Base Property Cost | | Budget minus other fees |\n| Stamp Duty & Registration (est. 7%) | | |\n| Brokerage (if applicable, est. 1%) | | |\n| Interiors/Furnishing (est. 10%) | | |\n| Contingency Fund (5%) | | For unexpected expenses |\n| **Total Estimated Project Cost** | **₹{int(details.get('fin_budget', 0)):,}** | **Matches client budget** |
        ### 3. Loan Amortization Schedule (Table)\nShow the schedule for a 20-year term. Show years 1, 2, 3, 4, 5, 10, 15, and 20.\n| Year | Principal Paid (₹) | Interest Paid (₹) | Annual Payment (₹) | Remaining Balance (₹) |\n|---|---|---|---|---|\n| 1 | | | | |; 2 | | | | |; 3 | | | | |; 4 | | | | |; 5 | | | | |; 10 | | | | |; 15 | | | | |; 20 | | | | |
        ### 4. Future Value & Equity Projections (Table)\n| Year | Projected Value (₹) | Total Equity (Value - Loan Balance) |\n|---|---|---|\n| 2 | | |; 5 | | |; 10 | | |; 15 | | |; 20 | | |
        ### 5. Rental Income Analysis (if purpose is Rental)\n**Only include this section if purpose is 'Rental Income'.**\n- **Target Monthly Rent:** ₹{int(details.get('fin_target_rent', 0)):,}\n- **Gross Annual Rent:**\n- **Less Expenses (30%):** (Property Tax, Maintenance, Insurance)\n- **Net Operating Income (NOI):**\n- **Capitalization (Cap) Rate:** (NOI / Total Project Cost)\n- **Recommendation:** Briefly state if the rental yield seems viable.
        ### 6. Summary & Next Steps\nProvide a friendly closing summary and a short, actionable checklist of next steps.
    """)

def build_follow_up_prompt(details, initial_report, question, lang_code):
    language_name = TRANSLATIONS[lang_code]['language_name']
    return textwrap.dedent(f"""You are a real estate financial analyst continuing a conversation. You already provided a detailed financial report. Now, answer a follow-up question. IMPORTANT: Your entire answer MUST be in the {language_name} language.
        **CONTEXT: YOUR PREVIOUS REPORT (which was in {language_name})**\n---\n{initial_report}\n---
        **CLIENT'S FOLLOW-UP QUESTION:**\n"{question}"
        **YOUR TASK:**\nAnswer the question concisely in {language_name}. Base your answer on the report's data. If it requires a new calculation (e.g., "what if interest is 9%?"), perform it and show the result. Do not repeat large parts of the report.
    """)

# ─────────────────────────────────────────────────────────────────────────────
# Main App Controller
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="AI Real Estate Advisor", page_icon="🏠", layout="wide")
    defaults = {
        'language': 'en', 'step': 0, 'selected_project': None, 'ai_response': None, 'follow_up_response': None, 'active_tool': None, 'name': '', 'contact': '',
        'dob': date(2000, 1, 1), 'income': 1000000, 'intent_type': 'buy_flat', 'intent_purpose': 'self_use', 'loc_city': 'Nagpur', 'loc_locality': '',
        'loc_pincode': '', 'fin_budget': 5000000, 'fin_loan': True, 'fin_subsidy': False, 'mixed_components': [], 'plan_flat_size': '2BHK',
        'plan_plot_area': 1200.0, 'plan_built_up': 1800.0, 'plan_floors': 2.0, 'extra_floors_rent': False, 'const_contract': 'With Material (Turnkey)',
        'const_vendors': [], 'const_green': [], 'const_timeline': 12.0, 'qual_connectivity': 'Medium', 'qual_amenities': 'Somewhat', 'risk_pollution': 'Low',
        'risk_crime': 'Low', 'fin_target_rent': 0, 'fin_target_resale': 0, 'is_joint_investment': False, 'co_owner_name': '', 'co_owner_relationship': 'Spouse',
        'investment_share_p1': 50.0, 'investment_share_p2': 50.0, 'fsi_value': 1.5
    }
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value

    display_sidebar()
    st.title(f"🏠 {t('app_title')}")
    if not st.session_state.selected_project: st.info(t('welcome_message'))
    else:
        st.markdown(t('current_project_header').format(project_name=st.session_state.selected_project)); st.divider()
        if st.session_state.step == 1: display_step1_user_details()
        elif st.session_state.step == 2: display_step2_intent()
        elif st.session_state.step == 3: display_step3_details()
        elif st.session_state.step == 4:
            if st.session_state.active_tool is None: display_step4_analysis()
            else: display_advanced_tool_ui()

if __name__ == "__main__":
    main()
