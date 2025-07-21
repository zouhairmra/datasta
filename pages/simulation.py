import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Simulation Center", layout="wide")

# Title
st.title("📊 Economic Simulation Center")

# Translation toggle
language = st.radio("🌐 Choose Language / اختر اللغة", ["English", "العربية"])

def translate(text_en, text_ar):
    return text_ar if language == "العربية" else text_en

# Sidebar Section navigation
section = st.sidebar.selectbox(
    translate("Choose Section", "اختر القسم"),
    [translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"),
     translate("Business Math Concepts", "مفاهيم الرياضيات للأعمال"),
     translate("AI Assistant", "المساعد الذكي")]
)

# Microeconomics Simulations
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

        st.subheader(translate("Real Case: Competitive Agriculture", "حالة واقعية: الزراعة التنافسية"))
        st.markdown(translate(
            "In competitive markets like small-scale agriculture, firms are price takers and cannot influence the market price. Their goal is to minimize cost and maximize output.",
            "في الأسواق التنافسية مثل الزراعة الصغيرة، تكون الشركات متلقية للأسعار ولا يمكنها التأثير على سعر السوق. هدفها هو تقليل التكاليف وتعظيم الإنتاج."
        ))

    elif topic == translate("Monopolistic Competition", "المنافسة الاحتكارية"):
        st.header(translate("Monopolistic Competition Simulation", "محاكاة المنافسة الاحتكارية"))

        price = st.slider(translate("Product Price", "سعر المنتج"), 1, 100, 50)
        avg_cost = st.number_input(translate("Average Cost", "التكلفة المتوسطة"), value=40)
        quantity = st.slider(translate("Quantity Sold", "الكمية المباعة"), 1, 100, 10)
        differentiation = st.slider(translate("Product Differentiation Level", "درجة تميز المنتج"), 0, 10, 5)

        revenue = price * quantity
        total_cost = avg_cost * quantity
        profit = revenue - total_cost + differentiation * 5  # Bonus for uniqueness

        st.metric(translate("Profit", "الربح"), profit)

        st.subheader(translate("Real Case: Coffee Shops", "حالة واقعية: المقاهي"))
        st.markdown(translate(
            "Coffee shops operate in a monopolistic competition structure. Each tries to stand out (location, taste, atmosphere) while still competing on price.",
            "تعمل المقاهي في إطار من المنافسة الاحتكارية، حيث تحاول كل منها التميز (بالموقع أو الطعم أو الأجواء) بينما تنافس أيضًا على السعر."
        ))
# AI Assistant Section (without OpenAI)
elif section == translate("AI Assistant", "المساعد الذكي"):
    st.header(translate("Ask the AI Assistant", "اسأل المساعد الذكي"))

    user_question = st.text_area(translate("Ask any question related to microeconomics or business math.",
                                           "اطرح أي سؤال متعلق بالاقتصاد الجزئي أو الرياضيات للأعمال."))

    if user_question:
        with st.spinner(translate("Thinking...", "جارٍ التفكير...")):
            answer = ""
            question_lower = user_question.lower()

            if "elasticity" in question_lower or "مرونة" in user_question:
                answer = translate(
                    "Elasticity measures how much quantity demanded or supplied changes when the price changes. For example, if a 10% increase in price causes a 20% drop in demand, the price elasticity is -2.",
                    "تقيس المرونة مقدار تغير الكمية المطلوبة أو المعروضة عند تغير السعر. على سبيل المثال، إذا أدت زيادة بنسبة 10٪ في السعر إلى انخفاض بنسبة 20٪ في الطلب، فإن المرونة السعرية هي -2."
                )
            elif "supply" in question_lower or "demand" in question_lower or "العرض" in user_question or "الطلب" in user_question:
                answer = translate(
                    "Supply is the quantity producers are willing to sell at a given price, while demand is the quantity consumers are willing to buy. The intersection determines the market price.",
                    "العرض هو كمية السلع التي يرغب المنتجون في بيعها عند سعر معين، بينما الطلب هو كمية السلع التي يرغب المستهلكون في شرائها. يتحدد السعر في السوق عند تقاطع العرض والطلب."
                )
            elif "cost" in question_lower or "التكلفة" in user_question:
                answer = translate(
                    "Total cost is the sum of fixed and variable costs. Marginal cost is the change in total cost from producing one more unit.",
                    "التكلفة الإجمالية هي مجموع التكاليف الثابتة والمتغيرة. التكلفة الحدية هي التغير في التكلفة الإجمالية عند إنتاج وحدة إضافية."
                )
            else:
                answer = translate(
                    "Sorry, I currently only answer questions about elasticity, supply/demand, and cost. More features coming soon!",
                    "عذرًا، يمكنني حالياً الإجابة فقط على الأسئلة المتعلقة بالمرونة، العرض والطلب، والتكلفة. المزيد من الميزات قريباً!"
                )

            st.success(answer)
