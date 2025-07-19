import streamlit as st
import pandas as pd
import numpy as np

# Sidebar for language selection
st.sidebar.title("Language / اللغة")
use_arabic = st.sidebar.checkbox("عرض بالعربية", value=False)

# Section and sub-section structure
section = st.sidebar.selectbox(
    "Choose a section:" if not use_arabic else "اختر القسم:",
    [
        "Microeconomics Simulations" if not use_arabic else "محاكاة الاقتصاد الجزئي",
        "Business Math Applications" if not use_arabic else "تطبيقات الرياضيات الاقتصادية"
    ]
)

# ------------------------- MICROECONOMICS SIMULATIONS --------------------------
if section.startswith("Micro"):
    subsection = st.sidebar.selectbox(
        "Choose a topic:" if not use_arabic else "اختر الموضوع:",
        [
            "Supply and Demand",
            "Elasticity of Demand",
            "Production and Cost Functions",
            "Profit Maximization",
            "Oligopoly (Game Theory)",
            "Perfect Competition",
            "Monopolistic Competition"
        ]
    )

    st.title(subsection if not use_arabic else "")

    if subsection == "Supply and Demand":
        st.header("Supply and Demand Simulation" if not use_arabic else "محاكاة العرض والطلب")
        price = st.slider("Select price", 1, 100, 50)
        demand = 100 - price
        supply = price - 10
        st.write(f"At price {price}, demand is {demand} and supply is {supply}.")

    elif subsection == "Elasticity of Demand":
        st.header("Elasticity Simulation" if not use_arabic else "مرونة الطلب")
        q1 = st.number_input("Quantity before", value=100)
        q2 = st.number_input("Quantity after", value=90)
        p1 = st.number_input("Price before", value=10)
        p2 = st.number_input("Price after", value=12)
        e = ((q2 - q1) / q1) / ((p2 - p1) / p1)
        st.write(f"Price elasticity of demand: {e:.2f}")

    elif subsection == "Production and Cost Functions":
        st.header("Production and Cost" if not use_arabic else "الإنتاج والتكلفة")
        labor = st.slider("Labor input", 1, 100, 20)
        capital = st.slider("Capital input", 1, 100, 10)
        output = np.sqrt(labor * capital)
        cost = 10 * labor + 20 * capital
        st.write(f"Output: {output:.2f}, Total Cost: ${cost:.2f}")

    elif subsection == "Profit Maximization":
        st.header("Profit Maximization" if not use_arabic else "تعظيم الربح")
        price = st.number_input("Product price", value=20)
        quantity = st.slider("Quantity produced", 1, 100, 10)
        cost = 5 * quantity + 50
        revenue = price * quantity
        profit = revenue - cost
        st.write(f"Revenue: ${revenue}, Cost: ${cost}, Profit: ${profit}")

    elif subsection == "Oligopoly (Game Theory)":
        st.header("Game Theory (Cournot Duopoly)" if not use_arabic else "السلوك في السوق الثنائي")
        q1 = st.slider("Firm A output", 0, 100, 20)
        q2 = st.slider("Firm B output", 0, 100, 20)
        market_price = 100 - (q1 + q2)
        profit1 = q1 * market_price
        profit2 = q2 * market_price
        st.write(f"Firm A profit: ${profit1}, Firm B profit: ${profit2}, Market Price: ${market_price}")

    elif subsection == "Perfect Competition":
        st.header("Perfect Competition" if not use_arabic else "المنافسة الكاملة")
        price = 50
        quantity = st.slider("Your firm's output", 1, 100, 10)
        cost = 30 * quantity
        revenue = price * quantity
        profit = revenue - cost
        st.write(f"Revenue: ${revenue}, Cost: ${cost}, Profit: ${profit}")

    elif subsection == "Monopolistic Competition":
        st.header("Monopolistic Competition" if not use_arabic else "المنافسة الاحتكارية")
        price = st.slider("Set your price", 1, 100, 40)
        demand = 100 - price
        cost = 20 * demand
        revenue = price * demand
        profit = revenue - cost
        st.write(f"Revenue: ${revenue}, Cost: ${cost}, Profit: ${profit}")

# ------------------------ BUSINESS MATH APPLICATIONS ---------------------------
else:
    subsection = st.sidebar.selectbox(
        "Choose a topic:" if not use_arabic else "اختر الموضوع:",
        [
            "Cost Minimization",
            "Profit Maximization",
            "Marginal Revenue vs Cost"
        ]
    )

    st.title(subsection if not use_arabic else "")

    if subsection == "Cost Minimization":
        st.header("Cost Minimization" if not use_arabic else "تقليل التكاليف")
        labor_cost = st.slider("Labor cost per unit", 1, 100, 20)
        capital_cost = st.slider("Capital cost per unit", 1, 100, 30)
        output = st.slider("Required output", 10, 100, 50)
        min_cost = output * (labor_cost * 0.6 + capital_cost * 0.4)
        st.write(f"Minimum cost to produce {output} units: ${min_cost:.2f}")

    elif subsection == "Profit Maximization":
        st.header("Profit Maximization" if not use_arabic else "تعظيم الربح")
        price = st.number_input("Unit price", value=50)
        variable_cost = st.number_input("Variable cost per unit", value=30)
        fixed_cost = st.number_input("Fixed cost", value=100)
        quantity = st.slider("Quantity sold", 1, 100, 10)
        profit = quantity * (price - variable_cost) - fixed_cost
        st.write(f"Total profit: ${profit:.2f}")

    elif subsection == "Marginal Revenue vs Cost":
        st.header("MR = MC Analysis" if not use_arabic else "تحليل الإيراد الحدي والتكلفة الحدية")
        quantity = st.slider("Quantity", 1, 100, 10)
        price = 100 - quantity
        total_revenue = quantity * price
        marginal_revenue = 100 - 2 * quantity
        marginal_cost = st.slider("Marginal cost", 1, 100, 20)
        st.write(f"Marginal Revenue: {marginal_revenue}, Marginal Cost: {marginal_cost}")
        if marginal_revenue > marginal_cost:
            st.success("Increase production")
        elif marginal_revenue < marginal_cost:
            st.error("Reduce production")
        else:
            st.info("Profit is maximized at this output level")
