import streamlit as st
import numpy as np
import pandas as pd

# Arabic toggle
arabic = st.sidebar.checkbox("العربية؟")

def label(en, ar):
    return ar if arabic else en

st.title(label("Economics Simulations", "محاكاة مفاهيم الاقتصاد"))

section = st.selectbox(
    label("Choose a Section", "اختر قسمًا"),
    [
        label("Microeconomics", "الاقتصاد الجزئي"),
        label("Business Math Concepts", "مفاهيم الرياضيات الاقتصادية")
    ]
)

if section.startswith("Micro"):

    topic = st.selectbox(
        label("Select Micro Topic", "اختر موضوعًا"),
        [
            label("Demand and Supply", "العرض والطلب"),
            label("Elasticities", "المرونات"),
            label("Production & Cost Functions", "دوال الإنتاج والتكلفة"),
            label("Perfect Competition", "السوق التنافسية"),
            label("Monopolistic Competition", "المنافسة الاحتكارية"),
            label("Oligopoly (Game Theory)", "الاحتكار القلّي (نظرية الألعاب)"),
        ]
    )

    if topic.startswith("Demand"):
        st.subheader(label("Real-World Example: Gasoline Market", "مثال واقعي: سوق الوقود"))
        price = st.slider(label("Price (USD)", "السعر بالدولار"), 1.0, 10.0, 3.0)
        quantity_demanded = 1000 - 100 * price
        quantity_supplied = -200 + 150 * price

        st.write(label(f"Quantity Demanded: {quantity_demanded}", f"الكمية المطلوبة: {quantity_demanded}"))
        st.write(label(f"Quantity Supplied: {quantity_supplied}", f"الكمية المعروضة: {quantity_supplied}"))

        if quantity_demanded == quantity_supplied:
            st.success(label("Market is in equilibrium", "السوق في حالة توازن"))
        elif quantity_demanded > quantity_supplied:
            st.warning(label("Excess Demand", "زيادة في الطلب"))
        else:
            st.warning(label("Excess Supply", "زيادة في العرض"))

    elif topic.startswith("Elasticities"):
        st.subheader(label("Example: Elasticity of Coffee", "مثال: مرونة الطلب على القهوة"))
        base_price = st.number_input(label("Base Price (USD)", "السعر الأساسي بالدولار"), value=4.0)
        new_price = st.number_input(label("New Price (USD)", "السعر الجديد"), value=5.0)
        base_quantity = 800
        new_quantity = 600

        pe = ((new_quantity - base_quantity) / base_quantity) / ((new_price - base_price) / base_price)
        st.write(label(f"Price Elasticity of Demand = {pe:.2f}", f"مرونة السعر = {pe:.2f}"))

        if abs(pe) > 1:
            st.info(label("Elastic Demand", "الطلب مرن"))
        else:
            st.info(label("Inelastic Demand", "الطلب غير مرن"))

    elif topic.startswith("Production"):
        st.subheader(label("Example: Factory Production (Short Run)", "مثال: إنتاج مصنع"))
        labor = st.slider(label("Labor Units", "وحدات العمل"), 1, 10, 5)
        capital = st.slider(label("Capital Units", "وحدات رأس المال"), 1, 10, 3)

        output = labor**0.5 * capital**0.5
        cost = labor * 50 + capital * 100
        st.write(label(f"Output = {output:.2f}", f"الإنتاج = {output:.2f}"))
        st.write(label(f"Total Cost = ${cost}", f"التكلفة الكلية = ${cost}"))

    elif topic.startswith("Perfect"):
        st.subheader(label("Example: Wheat Market", "مثال: سوق القمح"))
        price = st.slider(label("Market Price", "السعر السوقي"), 1.0, 20.0, 10.0)
        cost = 7.0
        output = st.slider(label("Output", "الكمية المنتجة"), 1, 100, 50)
        profit = (price - cost) * output
        st.write(label(f"Profit = ${profit}", f"الربح = ${profit}"))

    elif topic.startswith("Monopolistic"):
        st.subheader(label("Example: Restaurant Pricing", "مثال: تسعير مطعم"))
        demand_price = st.slider(label("Demand-based Price", "السعر حسب الطلب"), 5.0, 50.0, 20.0)
        cost = 10
        q = 30
        revenue = demand_price * q
        profit = revenue - (q * cost)
        st.write(label(f"Profit = ${profit}", f"الربح = ${profit}"))

    elif topic.startswith("Oligopoly"):
        st.subheader(label("Cournot Duopoly", "احتكار ثنائي - نموذج كورنو"))
        q1 = st.slider(label("Firm 1 Quantity", "كمية الشركة 1"), 0, 100, 40)
        q2 = st.slider(label("Firm 2 Quantity", "كمية الشركة 2"), 0, 100, 40)
        price = 100 - (q1 + q2)
        profit1 = q1 * price - q1 * 20
        profit2 = q2 * price - q2 * 20

        st.write(label(f"Firm 1 Profit: ${profit1}", f"ربح الشركة 1: ${profit1}"))
        st.write(label(f"Firm 2 Profit: ${profit2}", f"ربح الشركة 2: ${profit2}"))

elif section.startswith("Business"):
    st.subheader(label("Business Math Concepts", "مفاهيم رياضية اقتصادية"))

    topic = st.selectbox(
        label("Choose a Concept", "اختر مفهوما"),
        [
            label("Cost Minimization", "تقليل التكلفة"),
            label("Profit Maximization", "تعظيم الربح"),
            label("Marginal Analysis", "التحليل الحدي"),
        ]
    )

    if topic.startswith("Cost"):
        st.subheader(label("Example: Bakery Cost", "مثال: تكلفة المخبز"))
        labor = st.slider(label("Labor (hrs)", "العمل بالساعات"), 1, 100, 50)
        capital = st.slider(label("Capital ($)", "رأس المال"), 100, 1000, 500)
        cost = labor * 20 + capital * 0.5
        st.write(label(f"Total Cost: ${cost}", f"التكلفة الإجمالية: ${cost}"))

    elif topic.startswith("Profit"):
        st.subheader(label("Example: Selling Bottled Water", "مثال: بيع زجاجات المياه"))
        price = st.slider(label("Price per Bottle", "سعر الزجاجة"), 0.5, 5.0, 2.0)
        cost = 0.5
        quantity = st.slider(label("Quantity Sold", "الكمية المباعة"), 0, 1000, 300)
        profit = (price - cost) * quantity
        st.write(label(f"Profit: ${profit}", f"الربح: ${profit}"))

    elif topic.startswith("Marginal"):
        st.subheader(label("Example: Marginal Revenue vs Cost", "مثال: الإيراد الحدي مقابل التكلفة الحدية"))
        q = st.slider(label("Quantity", "الكمية"), 1, 100, 10)
        MR = 100 - 2*q
        MC = 20 + q
        st.write(label(f"Marginal Revenue = {MR}", f"الإيراد الحدي = {MR}"))
        st.write(label(f"Marginal Cost = {MC}", f"التكلفة الحدية = {MC}"))

        if abs(MR - MC) < 5:
            st.success(label("Near Profit Maximization", "نحو تعظيم الربح"))

