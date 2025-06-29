# smart-subsidy-dashboard/app.py
import streamlit as st

# --- Central PM Suryaghar Slab ---
def central_subsidy(kW):
    if kW <= 2:
        return 18000 * kW
    elif kW <= 3:
        return 18000 * 2 + 9000 * (kW - 2)
    return 0

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
        "url": "https://www.mahadiscom.in/solar/
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
st.set_page_config(page_title="Smart Solar Subsidy Dashboard 🇮🇳")
st.title("🔆 Smart Solar Subsidy Dashboard")
st.caption("Includes PM Suryaghar + Top 10 State Schemes")
st.markdown("---")

capacity = st.slider("Rooftop System Size (kW)", 1.0, 10.0, 3.0, step=0.5)
state = st.selectbox("Select Your State", list(states_data.keys()) + ["Others"])

# --- Results ---
central = central_subsidy(capacity)

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

# --- Disclaimer ---
st.markdown("""
---
### ⚠️ Disclaimer:
This dashboard is for **educational purposes only**. 
Values are indicative. Always verify with your local DISCOM, MNRE, or registered installer.
""")
