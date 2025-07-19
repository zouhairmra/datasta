import streamlit as st

st.set_page_config(page_title="Microeconomics Simulation Center", layout="wide")
st.title("🧮 Microeconomics Simulation Center")

st.markdown("""
Welcome to the interactive simulation center. Select a topic below to explore different economic scenarios, available in **English** and **Arabic**.
""")

# Sidebar selection
section = st.sidebar.radio("Choose a simulation topic:", [
    "Supply & Demand",
    "Elasticities",
    "Production & Cost Functions",
    "Market Structures",
    "Game Theory",
    "Business Math Concepts"
])

# Scenario options per section
if section == "Supply & Demand":
    st.header("📈 Supply & Demand Simulation")
    scenario = st.selectbox("Choose a scenario:", [
        "Shift in Demand",
        "Shift in Supply",
        "Price Ceiling & Floor",
        "Equilibrium Dynamics"
    ])
    
    if scenario == "Shift in Demand":
        st.markdown("""
        **Example**: What happens if consumers' income increases?

        → Demand curve shifts right. Equilibrium price and quantity rise.
        """)
        # Here you can add sliders or charts

elif section == "Elasticities":
    st.header("📊 Elasticity Explorer")
    topic = st.selectbox("Choose an elasticity concept:", [
        "Price Elasticity of Demand",
        "Income Elasticity",
        "Cross-Price Elasticity"
    ])
    
    if topic == "Price Elasticity of Demand":
        st.markdown("""
        **Example**: If price rises by 10% and quantity demanded falls by 20% → Elasticity = -2
        → This is elastic demand.
        """)

elif section == "Production & Cost Functions":
    st.header("🏭 Production & Cost Simulation")
    scenario = st.selectbox("Choose a scenario:", [
        "Short Run Cost Curve",
        "Long Run Average Cost",
        "Profit Maximization"
    ])
    
    if scenario == "Profit Maximization":
        st.markdown("""
        **Example**: Given a cost and revenue function, find output where MR = MC.
        """)

elif section == "Market Structures":
    st.header("🏦 Market Structures")
    market_type = st.selectbox("Choose a market type:", [
        "Perfect Competition",
        "Monopoly",
        "Monopolistic Competition",
        "Oligopoly"
    ])

    if market_type == "Perfect Competition":
        st.markdown("""
        **Example**: Firm is price taker, P = MR. Profit maximization at P = MC.
        """)

elif section == "Game Theory":
    st.header("🎯 Oligopoly & Game Theory")
    model = st.selectbox("Choose a model:", [
        "Prisoner's Dilemma",
        "Nash Equilibrium",
        "Cournot Competition"
    ])
    
    if model == "Prisoner's Dilemma":
        st.markdown("""
        **Example**: Two firms choosing whether to collude or compete.
        → Best response leads to equilibrium (defect, defect).
        """)

elif section == "Business Math Concepts":
    st.header("📐 Business Math in Economics")
    concept = st.selectbox("Choose a concept:", [
        "Cost Minimization",
        "Profit Maximization",
        "Marginal Analysis",
        "Break-even Analysis"
    ])
    
    if concept == "Cost Minimization":
        st.markdown("""
        **Example**: Use Lagrange method to minimize cost given production target.
        """)

st.markdown("---")
st.markdown("**Note:** All simulations will be extended with charts and interactive components. Arabic translation coming soon.")
