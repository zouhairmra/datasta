import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Economic Simulations", layout="wide")
st.title("📊 Economics Simulation & Business Math")

section = st.sidebar.radio("Choose a section", ["📘 Microeconomics Simulations", "📐 Business Math Concepts"])

if section == "📘 Microeconomics Simulations":
    st.header("Microeconomics Simulations (English / العربية)")

    sim_topic = st.selectbox("Choose a topic:", [
        "Supply & Demand (العرض والطلب)",
        "Elasticities (المرونة)",
        "Production & Costs (الإنتاج والتكاليف)",
        "Profit Maximization (تعظيم الأرباح)",
        "Game Theory & Oligopoly (نظرية الألعاب)",
        "Competitive Market (السوق التنافسية)",
        "Monopolistic Competition (المنافسة الاحتكارية)"
    ])

    if sim_topic == "Supply & Demand (العرض والطلب)":
        st.subheader("Supply & Demand Simulation")
        a = st.slider("Demand Intercept (a)", 10, 100, 60)
        b = st.slider("Demand Slope (b)", 1, 10, 2)
        c = st.slider("Supply Intercept (c)", 0, 50, 10)
        d = st.slider("Supply Slope (d)", 1, 10, 3)

        Q = np.linspace(0, 50, 100)
        Pd = a - b * Q
        Ps = c + d * Q

        fig, ax = plt.subplots()
        ax.plot(Q, Pd, label="Demand")
        ax.plot(Q, Ps, label="Supply")
        ax.set_xlabel("Quantity")
        ax.set_ylabel("Price")
        ax.legend()
        st.pyplot(fig)

    elif sim_topic == "Elasticities (المرونة)":
        st.subheader("Elasticity Calculator")
        P1 = st.number_input("Initial Price", value=100.0)
        Q1 = st.number_input("Initial Quantity", value=500.0)
        P2 = st.number_input("New Price", value=120.0)
        Q2 = st.number_input("New Quantity", value=450.0)

        if P1 != P2:
            elasticity = ((Q2 - Q1) / ((Q2 + Q1)/2)) / ((P2 - P1) / ((P2 + P1)/2))
            st.metric("Price Elasticity of Demand", f"{elasticity:.2f}")
        else:
            st.warning("Price values must differ to calculate elasticity.")

elif section == "📐 Business Math Concepts":
    st.header("Business Math Concepts Applied to Economics")

    math_topic = st.selectbox("Select a concept:", [
        "Cost Minimization",
        "Profit Maximization",
        "Marginal Revenue & Marginal Cost",
        "Break-Even Analysis",
        "Optimization with Constraints",
        "Supply & Demand Equilibrium (Algebraic)",
        "Elasticity Calculation"
    ])

    if math_topic == "Break-Even Analysis":
        st.subheader("Break-Even Point")
        fixed_cost = st.number_input("Fixed Cost", value=1000.0)
        price_per_unit = st.number_input("Price per Unit", value=20.0)
        variable_cost_per_unit = st.number_input("Variable Cost per Unit", value=10.0)

        if price_per_unit > variable_cost_per_unit:
            break_even_qty = fixed_cost / (price_per_unit - variable_cost_per_unit)
            st.metric("Break-Even Quantity", f"{break_even_qty:.0f} units")
        else:
            st.error("Price must be greater than variable cost.")

    elif math_topic == "Supply & Demand Equilibrium (Algebraic)":
        st.subheader("Algebraic Equilibrium")
        a = st.number_input("Demand Intercept (a)", value=100.0)
        b = st.number_input("Demand Slope (b)", value=1.0)
        c = st.number_input("Supply Intercept (c)", value=10.0)
        d = st.number_input("Supply Slope (d)", value=1.0)

        Q_eq = (a - c) / (b + d)
        P_eq = a - b * Q_eq
        st.metric("Equilibrium Quantity", f"{Q_eq:.2f}")
        st.metric("Equilibrium Price", f"{P_eq:.2f}")
