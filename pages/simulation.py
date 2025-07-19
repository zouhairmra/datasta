import streamlit as st
import numpy as np
import pandas as pd
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Economic Simulation Center", layout="wide")

# Securely load your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]  # Make sure you set this in your secrets.toml

# Translation helper
language = st.radio("🌐 Choose Language / اختر اللغة", ["English", "العربية"])

def translate(en, ar):
    return ar if language == "العربية" else en

st.title(translate("📊 Economic Simulation Center", "📊 مركز محاكاة الاقتصاد"))

# Sidebar navigation
section = st.sidebar.selectbox(
    translate("Choose Section", "اختر القسم"),
    [
        translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"),
        translate("Business Math Concepts", "مفاهيم الرياضيات للأعمال"),
        translate("AI Assistant", "المساعد الذكي")
    ]
)

# --- Microeconomics simulations ---
if section == translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"):

    topic = st.sidebar.radio(
        translate("Choose Topic", "اختر الموضوع"),
        [
            translate("Supply and Demand", "العرض والطلب"),
            translate("Elasticities", "المرونات"),
            translate("Production & Costs", "الإنتاج والتكاليف"),
            translate("Oligopoly (Game Theory)", "احتكار القلة (نظرية الألعاب)"),
            translate("Competitive Market", "السوق التنافسي"),
            translate("Monopolistic Competition", "المنافسة الاحتكارية"),
        ]
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

# --- Business Math Concepts ---
elif section == translate("Business Math Concepts", "مفاهيم الرياضيات للأعمال"):

    topic = st.sidebar.radio(
        translate("Choose Concept", "اختر المفهوم"),
        [
            translate("Cost Minimization", "تقليل التكلفة"),
            translate("Profit Maximization", "تعظيم الربح"),
            translate("Marginal Analysis", "التحليل الحدي"),
        ]
    )

    if topic == translate("Cost Minimization", "تقليل التكلفة"):
        st.header(translate("Cost Minimization Example", "مثال تقليل التكلفة"))
        labor = st.slider(translate("Labor (hrs)", "العمل بالساعات"), 1, 100, 50)
        capital = st.slider(translate("Capital ($)", "رأس المال"), 100, 1000, 500)
        cost = labor * 20 + capital * 0.5
        st.metric(translate("Total Cost", "التكلفة الإجمالية"), cost)

    elif topic == translate("Profit Maximization", "تعظيم الربح"):
        st.header(translate("Profit Maximization Example", "مثال تعظيم الربح"))
        price = st.slider(translate("Price per Unit", "السعر للوحدة"), 0.5, 10.0, 2.0)
        cost = st.slider(translate("Cost per Unit", "التكلفة للوحدة"), 0.1, 5.0, 1.0)
        quantity = st.slider(translate("Quantity Sold", "الكمية المباعة"), 0, 1000, 300)
        profit = (price - cost) * quantity
        st.metric(translate("Profit", "الربح"), profit)

    elif topic == translate("Marginal Analysis", "التحليل الحدي"):
        st.header(translate("Marginal Revenue vs Marginal Cost", "الإيراد الحدي مقابل التكلفة الحدية"))
        q = st.slider(translate("Quantity", "الكمية"), 1, 100, 10)
        MR = 100 - 2 * q
        MC = 20 + q
        st.metric(translate("Marginal Revenue", "الإيراد الحدي"), MR)
        st.metric(translate("Marginal Cost", "التكلفة الحدية"), MC)

        if abs(MR - MC) < 5:
            st.success(translate("Near Profit Maximization", "نحو تعظيم الربح"))

# --- AI Assistant Section ---
elif section == translate("AI Assistant", "المساعد الذكي"):

    st.header(translate("Ask the AI Assistant", "اسأل المساعد الذكي"))

    user_question = st.text_area(translate(
        "Ask any question related to microeconomics or business math.",
        "اطرح أي سؤال متعلق بالاقتصاد الجزئي أو الرياضيات للأعمال."
    ))

    if user_question:
        with st.spinner(translate("Thinking...", "جارٍ التفكير...")):
            try:
              from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

chat_completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an expert assistant helping Arabic-speaking students understand microeconomics and business mathematics. Use simple examples and explain clearly."},
        {"role": "user", "content": user_question}
    ],
    temperature=0.7,
    max_tokens=1000
)

answer = chat_completion.choices[0].message.content
                st.success(answer)

            except Exception as e:
                st.error(f"Error communicating with OpenAI API: {e}")
