import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as g0
import requests
import openai
from openai import OpenAI
import sys
import os
# Add project root folder (adjust if needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
st.set_page_config(page_title="Simulation Center", layout="wide")

# Title
st.title("📊 Economic Simulation Center")

# Language toggle
language = st.radio("🌐 Choose Language / اختر اللغة", ["English", "العربية"])

def translate(text_en, text_ar):
    return text_ar if language == "العربية" else text_en

# Sidebar navigation
section = st.sidebar.selectbox(
    translate("Choose Section", "اختر القسم"),
    [translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"),
     translate("Business Math Concepts", "مفاهيم الرياضيات للأعمال"),
     translate("AI Assistant", "المساعد الذكي")]
)

# --- Microeconomics Simulations ---
if section == translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"):
    topic = st.sidebar.radio(
        translate("Choose Topic", "اختر الموضوع"),
        [translate("Supply and Demand", "العرض والطلب"),
         translate("Elasticities", "المرونات"),
         translate("Production & Costs", "الإنتاج والتكاليف"),
         translate("Oligopoly (Game Theory)", "احتكار القلة (نظرية الألعاب)"),
         translate("Competitive Market", "السوق التنافسي"),
         translate("Monopolistic Competition", "المنافسة الاحتكارية")]
    )

    if topic == translate("Supply and Demand", "العرض والطلب"):
        st.header(translate("Supply and Demand Simulation", "محاكاة العرض والطلب"))

        price = st.slider(translate("Price", "السعر"), 1, 100, 50)
        demand_intercept = st.number_input(translate("Demand Intercept (a)", "تقاطع الطلب (a)"), value=100)
        demand_slope = st.number_input(translate("Demand Slope (b)", "ميل الطلب (b)"), value=1)
        supply_intercept = st.number_input(translate("Supply Intercept (c)", "تقاطع العرض (c)"), value=20)
        supply_slope = st.number_input(translate("Supply Slope (d)", "ميل العرض (d)"), value=1)

        quantity_demanded = demand_intercept - demand_slope * price
        quantity_supplied = supply_intercept + supply_slope * price

        st.metric(translate("Quantity Demanded", "الكمية المطلوبة"), quantity_demanded)
        st.metric(translate("Quantity Supplied", "الكمية المعروضة"), quantity_supplied)

        st.subheader(translate("Real Case: Qatari Wheat Market (2022)", "حالة واقعية: سوق القمح القطري (2022)"))
        st.markdown(translate(
            "In 2022, Qatar imported large quantities of wheat at a stable world price. Local demand shifts during Ramadan caused excess demand. The simulation above mimics how small changes in price affect market balance.",
            "في عام 2022، استوردت قطر كميات كبيرة من القمح بسعر عالمي ثابت. أدت زيادة الطلب المحلي خلال رمضان إلى فائض طلب. تحاكي المحاكاة أعلاه كيف تؤثر التغيرات الطفيفة في السعر على توازن السوق."
        ))

    elif topic == translate("Elasticities", "المرونات"):
        st.header(translate("Elasticity of Demand", "مرونة الطلب"))
        initial_price = st.number_input(translate("Initial Price", "السعر الابتدائي"), value=10.0)
        new_price = st.number_input(translate("New Price", "السعر الجديد"), value=12.0)
        initial_quantity = st.number_input(translate("Initial Quantity", "الكمية الابتدائية"), value=100.0)
        new_quantity = st.number_input(translate("New Quantity", "الكمية الجديدة"), value=90.0)

        try:
            elasticity = ((new_quantity - initial_quantity) / initial_quantity) / ((new_price - initial_price) / initial_price)
            st.metric(translate("Price Elasticity", "مرونة السعر"), round(elasticity, 2))
        except ZeroDivisionError:
            st.error(translate("Price or quantity cannot be zero.", "لا يمكن أن يكون السعر أو الكمية صفراً."))

        st.subheader(translate("Real Case: iPhone Price Sensitivity", "حالة واقعية: حساسية سعر الآيفون"))
        st.markdown(translate(
            "Apple increased iPhone prices by 10% in 2023. In emerging markets, quantity sold dropped by ~12%, suggesting an elasticity of -1.2.",
            "زادت شركة Apple أسعار الآيفون بنسبة 10٪ في عام 2023. في الأسواق الناشئة، انخفضت الكميات المباعة بنسبة 12٪ تقريبًا، مما يشير إلى مرونة -1.2."
        ))

    elif topic == translate("Production & Costs", "الإنتاج والتكاليف"):
        st.header(translate("Production and Cost Functions", "دوال الإنتاج والتكلفة"))

        labor = st.slider(translate("Labor Input", "العمالة"), 1, 100, 50)
        capital = st.slider(translate("Capital Input", "رأس المال"), 1, 100, 50)

        output = labor ** 0.5 * capital ** 0.5
        cost = 20 * labor + 30 * capital

        st.metric(translate("Output (Q)", "الإنتاج (Q)"), round(output, 2))
        st.metric(translate("Total Cost", "التكلفة الإجمالية"), round(cost, 2))

        st.subheader(translate("Real Case: Tesla Factory Efficiency", "حالة واقعية: كفاءة مصنع تسلا"))
        st.markdown(translate(
            "Tesla's Shanghai Gigafactory uses automation (capital) and specialized labor. Increasing capital improves output at diminishing marginal returns.",
            "يستخدم مصنع تسلا في شنغهاي الأتمتة (رأس المال) والعمالة المتخصصة. تؤدي زيادة رأس المال إلى تحسين الإنتاج بمردود هامشي متناقص."
        ))

    elif topic == translate("Oligopoly (Game Theory)", "احتكار القلة (نظرية الألعاب)"):
        st.header(translate("Cournot Competition Simulation", "محاكاة نموذج كورنو"))

        q1 = st.slider(translate("Firm 1 Quantity", "كمية الشركة 1"), 0, 100, 30)
        q2 = st.slider(translate("Firm 2 Quantity", "كمية الشركة 2"), 0, 100, 30)

        total_q = q1 + q2
        price = max(0, 100 - total_q)
        profit1 = (price - 20) * q1
        profit2 = (price - 20) * q2

        st.metric("Price", price)
        st.metric("Profit Firm 1", profit1)
        st.metric("Profit Firm 2", profit2)

        st.subheader(translate("Real Case: Airbus vs Boeing Market Competition", "حالة واقعية: المنافسة بين إيرباص وبوينغ"))
        st.markdown(translate(
            "Boeing and Airbus often restrict output to keep prices high, much like the Cournot model shows.",
            "تقوم شركتا بوينغ وإيرباص بتقييد الإنتاج للحفاظ على الأسعار مرتفعة، تمامًا كما يوضح نموذج كورنو."
        ))

    elif topic == translate("Competitive Market", "السوق التنافسي"):
        st.header(translate("Competitive Market Simulation", "محاكاة السوق التنافسي"))

        market_price = st.slider(translate("Market Price", "سعر السوق"), 1, 100, 50)
        cost_per_unit = st.number_input(translate("Cost per Unit", "التكلفة لكل وحدة"), value=30)
        quantity = st.slider(translate("Quantity Produced", "الكمية المنتجة"), 1, 100, 10)

        profit = (market_price - cost_per_unit) * quantity
        st.metric(translate("Profit", "الربح"), profit)

        quantities = np.arange(1, 101)
        revenues = market_price * quantities
        costs = cost_per_unit * quantities

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=quantities, y=revenues, mode='lines', name=translate("Total Revenue", "الإيراد الكلي"), line=dict(color='green')))
        fig.add_trace(go.Scatter(x=quantities, y=costs, mode='lines', name=translate("Total Cost", "التكلفة الكلية"), line=dict(color='red')))
        fig.add_trace(go.Scatter(x=[quantity], y=[market_price * quantity], mode='markers', name=translate("Chosen Quantity", "الكمية المختارة"), marker=dict(size=10, color='blue')))

        fig.update_layout(
            title=translate("Revenue and Cost in Competitive Market", "الإيراد والتكلفة في السوق التنافسي"),
            xaxis_title=translate("Quantity", "الكمية"),
            yaxis_title=translate("Amount", "القيمة"),
            legend_title=translate("Legend", "المفتاح")
        )

        st.plotly_chart(fig)

    elif topic == translate("Monopolistic Competition", "المنافسة الاحتكارية"):
        st.header(translate("Monopolistic Competition Simulation", "محاكاة المنافسة الاحتكارية"))

        price = st.slider(translate("Product Price", "سعر المنتج"), 1, 100, 50)
        avg_cost = st.number_input(translate("Average Cost", "التكلفة المتوسطة"), value=40)
        quantity = st.slider(translate("Quantity Sold", "الكمية المباعة"), 1, 100, 10)
        differentiation = st.slider(translate("Product Differentiation Level", "درجة تميز المنتج"), 0, 10, 5)

        revenue = price * quantity
        total_cost = avg_cost * quantity
        profit = revenue - total_cost + differentiation * 5

        st.metric(translate("Profit", "الربح"), profit)

        diff_range = np.arange(0, 11)
        profits = [(price * quantity - avg_cost * quantity + d * 5) for d in diff_range]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=diff_range,
            y=profits,
            mode='lines+markers',
            name=translate("Profit", "الربح"),
            line=dict(color='purple')
        ))

        fig.update_layout(
            title=translate("Profit vs Product Differentiation", "الربح مقابل درجة تميز المنتج"),
            xaxis_title=translate("Product Differentiation Level", "درجة التميز"),
            yaxis_title=translate("Profit", "الربح"),
            legend_title=translate("Legend", "المفتاح")
        )

        st.plotly_chart(fig)
st.set_page_config(page_title="🧠 AI Economics Assistant", layout="centered")
st.title("🧠 AI Economics Assistant (Mistral-7B)")

# 🔐 API Key Input
api_key = st.text_input("🔑 Enter your Together AI API Key", type="password")

# 📥 Prompt Input
prompt = st.text_area("💬 Ask a question in economics:", height=150)

# 🎛️ Model and Settings
with st.expander("🧠 Model Options"):
    model_options = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "meta-llama/Llama-2-7b-chat-hf"
    ]
    selected_model = st.selectbox("Choose a model", model_options, index=0)

with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max tokens (response length)", 256, 4096, 1024, 128)

# 🧠 Answer Generation
if st.button("Generate Answer"):
    if not api_key:
        st.error("❌ Please enter your API key.")
    elif not prompt.strip():
        st.error("❌ Please write a prompt.")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": "You are an expert economics teacher assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
            st.markdown("### 🤖 AI Response")
            st.write(reply)
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error: {e}")
