# smart-subsidy-dashboard/app.py
import streamlit as st

# --- Central PM Suryaghar Subsidy Logic ---
def central_subsidy(kW):
    if kW <= 2:
        return 30000 * kW
    elif kW <= 3:
        return 30000 * 2 + 18000 * (kW - 2)
    else:
        return 78000  # Capped subsidy

# --- Suggested capacity based on average monthly usage ---
def suggest_capacity(units):
    if units <= 150:
        return "1–2 kW"
    elif 150 < units <= 300:
        return "2–3 kW"
    else:
        return ">3 kW"

# --- Top 10 states data ---
states_data = {
    "Gujarat": {
        "subsidy": lambda kW: min(20000, 10000 * min(kW, 2) + 5000 * max(0, min(kW - 2, 1))),
        "eligibility": "Use empaneled vendors, max ₹20,000",
        "url": "https://geda.gujarat.gov.in"
    },
    "Rajasthan": {
        "subsidy": lambda kW: min(kW, 3) * 15000,
        "eligibility": "Residential only, RREC Scheme",
        "url": "https://energy.rajasthan.gov.in/rrec"
    },
    "Maharashtra": {
        "subsidy": lambda kW: min(kW, 3) * 3000,
        "eligibility": "Only in select districts",
        "url": "https://www.mahadiscom.in/solar/"
    },
    "Karnataka": {
        "subsidy": lambda kW: 10000 if kW <= 3 else 0,
        "eligibility": "BESCOM pilot, Bangalore Urban only",
        "url": "https://bescom.karnataka.gov.in"
    },
    "Tamil Nadu": {
        "subsidy": lambda kW: 20000 if kW <= 3 else 0,
        "eligibility": "Seasonal, TANGEDCO only",
        "url": "https://www.teda.in"
    },
    "Kerala": {
        "subsidy": lambda kW: min(kW, 3) * 10000,
        "eligibility": "ANERT registered vendors only",
        "url": "https://anert.gov.in"
    },
    "Delhi": {
        "subsidy": lambda kW: 0.10 * 45000 * min(kW, 3),
        "eligibility": "Group Housing/Societies only",
        "url": "https://solarrooftop.gov.in"
    },
    "Punjab": {
        "subsidy": lambda kW: min(kW, 3) * 12000,
        "eligibility": "MNRE vendors only",
        "url": "https://peda.gov.in"
    },
    "Telangana": {
        "subsidy": lambda kW: min(kW, 3) * 10000,
        "eligibility": "Urban pilot only",
        "url": "https://tsredco.telangana.gov.in"
    },
    "Haryana": {
        "subsidy": lambda kW: min(kW, 3) * 15000,
        "eligibility": "Residential only via HAREDA",
        "url": "https://hareda.gov.in"
    }
}

# --- UI ---
st.set_page_config(page_title="Smart Solar Subsidy Dashboard for Reference 🇮🇳")
st.title("🔆 Smart Solar Subsidy Dashboard")
st.caption("Includes PM Suryaghar + Top 10 State Schemes")
st.markdown("---")

capacity = st.slider("Rooftop System Size (kW)", 1.0, 10.0, 3.0, step=0.5)
monthly_units = st.number_input("Average Monthly Electricity Consumption (Units)", min_value=0, max_value=1000, value=250)
state = st.selectbox("Select Your State", list(states_data.keys()) + ["Others"])

# --- Results ---
central = central_subsidy(capacity)
suggested = suggest_capacity(monthly_units)

if state in states_data:
    state_info = states_data[state]
    state_sub = state_info["subsidy"](capacity)
    total_sub = central + state_sub
    st.subheader("💰 Subsidy Details")
    st.write(f"✅ Central Subsidy (PM Suryaghar): ₹{int(central):,}")
    st.write(f"✅ {state} State Subsidy: ₹{int(state_sub):,}")
    st.write(f"ℹ️ Eligibility: {state_info['eligibility']}")
    st.write(f"🔗 [Official Portal]({state_info['url']})")
else:
    total_sub = central
    st.subheader("💰 Subsidy Details")
    st.write(f"✅ Central Subsidy (PM Suryaghar): ₹{int(central):,}")
    st.warning("ℹ️ State scheme details not available. Please check your DISCOM or [MNRE Portal](https://solarrooftop.gov.in)")

st.markdown("---")
total_cost = capacity * 45000
net_cost = total_cost - total_sub
st.metric("📦 Estimated Total System Cost", f"₹{int(total_cost):,}")
st.metric("🏷️ Net Payable After Subsidy", f"₹{int(net_cost):,}")

# --- Suggested system size ---
st.markdown("---")
st.subheader("📐 Suggested Rooftop Solar Size")
st.write(f"Based on your usage of {monthly_units} units/month → Suggested: **{suggested}**")

# --- Disclaimer ---
st.markdown("""
---
### ⚠️ Disclaimer:
This dashboard is for **educational purposes only**. 
Values are indicative. Always verify with your local DISCOM, MNRE, or registered installer.
Refer: [PM Suryaghar Portal](https://pmsuryaghar.gov.in/#/)
Built by Ganesh Moorthi
""")
