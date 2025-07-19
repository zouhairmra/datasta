import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Economics Simulations", layout="wide")
st.title("📊 Microeconomics & Business Math Simulations")

# Sidebar Navigation
section = st.sidebar.selectbox("Select Section", [
    "Microeconomics Simulations",
    "Business Math Applications"
])

# Arabic translations dictionary
translations = {
    "Supply and Demand": "العرض والطلب",
    "Elasticity": "المرونة",
    "Production Functions": "دوال الإنتاج",
    "Oligopoly (Game Theory)": "الاحتكار القليل (نظرية الألعاب)",
    "Competitive Market": "السوق التنافسية",
    "Monopolistic Competition": "المنافسة الاحتكارية",
    "Cost Minimization": "تقليل التكاليف",
    "Profit Maximization": "تعظيم الأرباح",
    "Marginal Revenue Analysis": "تحليل الإيراد الحدي",
    "Choose Concept": "اختر المفهوم",
    "Choose Scenario": "اختر السيناريو",
    "Show Arabic": "عرض بالعربية"
}

# Arabic Toggle
def translate(text):
    return translations.get(text, text)

show_arabic = st.sidebar.checkbox("Show Arabic", value=False)

def label(text):
    return f"{text} ({translate(text)})" if show_arabic else text

# Concept & Scenario Selector
def show_simulation(concepts):
    concept = st.selectbox(label("Choose Concept"), concepts)

    if concept == "Supply and Demand":
        scenario = st.radio(label("Choose Scenario"), [
            "Shift in Demand",
            "Shift in Supply",
            "Price Floor/Ceiling"
        ])
        if scenario == "Shift in Demand":
            st.subheader("🔄 Real Example: Increase in Demand for EVs")
            st.markdown("""
            In recent years, electric vehicles (EVs) have seen a surge in demand due to environmental awareness and government incentives.
            
            **Before Shift:** Demand = D1, Price = P1, Quantity = Q1  
            **After Shift:** Demand = D2, Price rises to P2, Quantity increases to Q2
            
            *You can simulate the change using Streamlit sliders in future.*
            """)
        elif scenario == "Shift in Supply":
            st.subheader("🚜 Real Example: Technological Advancement in Agriculture")
            st.markdown("""
            Suppose new farming technology reduces the cost of wheat production. This shifts supply rightward.

            **Before Shift:** Supply = S1, Price = P1, Quantity = Q1  
            **After Shift:** Supply = S2, Price falls to P2, Quantity increases to Q2
            """)
        elif scenario == "Price Floor/Ceiling":
            st.subheader("🏠 Real Example: Rent Control in New York")
            st.markdown("""
            A price ceiling on rent below market rate leads to housing shortages.
            
            **Equilibrium Rent:** $1,500  
            **Ceiling Price:** $1,000 → Shortage of housing supply
            """)

    elif concept == "Elasticity":
        scenario = st.radio(label("Choose Scenario"), [
            "Price Elasticity of Demand",
            "Income Elasticity"
        ])
        if scenario == "Price Elasticity of Demand":
            st.subheader("💡 Real Example: Luxury Cars vs Bread")
            st.markdown("""
            **Luxury Cars** have elastic demand → 10% ↑ in price → 20% ↓ in demand  
            **Bread** has inelastic demand → 10% ↑ in price → 2% ↓ in demand
            """)

    elif concept == "Production Functions":
        scenario = st.radio(label("Choose Scenario"), [
            "Short-run Costs",
            "Long-run Production"
        ])
        if scenario == "Short-run Costs":
            st.subheader("🏭 Real Example: Shoe Factory Costs")
            st.markdown("""
            A factory adds workers while keeping machines fixed → diminishing marginal returns.
            
            **Output:** Initially increases quickly, then slower
            **Costs:** Marginal cost increases
            """)

    elif concept == "Oligopoly (Game Theory)":
        st.subheader("🎮 Real Example: Airline Price Wars")
        st.markdown("""
        Delta and United must decide whether to lower prices. If both cut prices → less profit. If one cuts and the other doesn’t → winner takes market.

        This is a typical **Prisoner's Dilemma** structure.
        """)

    elif concept == "Competitive Market":
        st.subheader("📈 Real Example: Wheat Farming")
        st.markdown("""
        Thousands of identical wheat farms with no pricing power.

        **Market Outcome:** Firms are price takers. Long-run profits = 0
        """)

    elif concept == "Monopolistic Competition":
        st.subheader("🛍️ Real Example: Fast Food Chains")
        st.markdown("""
        Firms like McDonald's and Burger King differentiate products but face competition.

        **Short-run:** Positive profit  
        **Long-run:** Entry reduces profit to 0
        """)

def show_business_math():
    concept = st.selectbox(label("Choose Concept"), [
        "Cost Minimization",
        "Profit Maximization",
        "Marginal Revenue Analysis"
    ])

    if concept == "Cost Minimization":
        st.subheader("💼 Real Example: Minimizing Delivery Costs")
        st.markdown("""
        A logistics firm uses optimization to minimize costs by rerouting trucks.
        
        **Objective:** Minimize total cost C = f(distance, fuel, labor)
        """)

    elif concept == "Profit Maximization":
        st.subheader("📊 Real Example: Smartphone Pricing")
        st.markdown("""
        A phone company estimates demand Q = 100 - 2P.  
        Revenue = P × Q, Cost = 10Q.  
        
        **Max Profit:** where MR = MC
        """)

    elif concept == "Marginal Revenue Analysis":
        st.subheader("📉 Real Example: Streaming Platform Pricing")
        st.markdown("""
        A streaming service analyzes revenue when adding subscribers. 

        **Rule:** Keep adding users until Marginal Revenue = Marginal Cost
        """)

# Main Execution
if section == "Microeconomics Simulations":
    show_simulation([
        "Supply and Demand",
        "Elasticity",
        "Production Functions",
        "Oligopoly (Game Theory)",
        "Competitive Market",
        "Monopolistic Competition"
    ])

elif section == "Business Math Applications":
    show_business_math()
