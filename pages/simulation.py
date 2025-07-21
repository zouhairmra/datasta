import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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

# --- AI Assistant ---
elif section == translate("AI Assistant", "المساعد الذكي"):
    import plotly.graph_objs as go

    st.header(translate("Ask the AI Assistant", "اسأل المساعد الذكي"))

    user_question = st.text_area(translate("Ask any question related to microeconomics or business math.",
                                           "اطرح أي سؤال متعلق بالاقتصاد الجزئي أو الرياضيات للأعمال."))

    # Define topic dictionary
    topics = {
        "elasticity": {
            "keywords": ["elasticity", "مرونة"],
            "en": "Elasticity measures how much quantity demanded or supplied changes when the price changes. For example, if a 10% increase in price causes a 20% drop in demand, the price elasticity is -2.",
            "ar": "تقيس المرونة مقدار تغير الكمية المطلوبة أو المعروضة عند تغير السعر. على سبيل المثال، إذا أدت زيادة بنسبة 10٪ في السعر إلى انخفاض بنسبة 20٪ في الطلب، فإن المرونة السعرية هي -2.",
            "show_chart": True
        },
        "supply_demand": {
            "keywords": ["supply", "demand", "العرض", "الطلب"],
            "en": "Supply is what producers offer at various prices; demand is what consumers want to buy. Their intersection determines equilibrium price.",
            "ar": "العرض هو ما يقدمه المنتجون عند أسعار مختلفة؛ الطلب هو ما يرغب المستهلكون في شرائه. يتحدد السعر التوازني عند تقاطع العرض والطلب.",
            "show_chart": False
        },
        "cost": {
            "keywords": ["cost", "التكلفة"],
            "en": "Total cost includes fixed and variable costs. Marginal cost is the cost of producing one more unit.",
            "ar": "تشمل التكلفة الإجمالية التكاليف الثابتة والمتغيرة. التكلفة الحدية هي تكلفة إنتاج وحدة إضافية.",
            "show_chart": False
        },
        "market_structure": {
            "keywords": ["monopoly", "oligopoly", "perfect competition", "structure", "احتكار", "سوق", "منافسة"],
            "en": "Market structures include perfect competition, monopolistic competition, oligopoly, and monopoly. Each differs in terms of number of firms, barriers to entry, and price control.",
            "ar": "تشمل هياكل السوق: المنافسة الكاملة، والمنافسة الاحتكارية، والاحتكار القلّي، والاحتكار. تختلف كل منها في عدد الشركات وحواجز الدخول والسيطرة على الأسعار.",
            "show_chart": False
        },
        "opportunity_cost": {
            "keywords": ["opportunity cost", "تكلفة الفرصة"],
            "en": "Opportunity cost is the value of the next best alternative you give up when making a choice.",
            "ar": "تكلفة الفرصة البديلة هي قيمة أفضل بديل تم التخلي عنه عند اتخاذ قرار.",
            "show_chart": False
        },
        "inflation": {
            "keywords": ["inflation", "تضخم"],
            "en": "Inflation is the general increase in prices over time. It reduces purchasing power.",
            "ar": "التضخم هو الارتفاع العام في الأسعار مع مرور الوقت، مما يقلل من القوة الشرائية.",
            "show_chart": False
        },
        "gdp": {
            "keywords": ["gdp", "gross domestic product", "الناتج المحلي", "الناتج الإجمالي"],
            "en": "GDP measures the total market value of all final goods and services produced in a country in a given period.",
            "ar": "يقيس الناتج المحلي الإجمالي القيمة السوقية لجميع السلع والخدمات النهائية المنتجة في بلد ما خلال فترة زمنية معينة.",
            "show_chart": False
        },
        "profit_max": {
            "keywords": ["profit", "maximize", "الربح", "تعظيم"],
            "en": "Firms maximize profit where marginal cost equals marginal revenue (MC = MR).",
            "ar": "تقوم الشركات بتعظيم الربح عندما تتساوى التكلفة الحدية مع الإيراد الحدي (MC = MR).",
            "show_chart": False
        },
        "game_theory": {
            "keywords": ["game theory", "نظريه الالعاب"],
            "en": "Game theory analyzes strategic interactions where outcomes depend on actions of multiple agents.",
            "ar": "تحلل نظرية الألعاب التفاعلات الاستراتيجية حيث تعتمد النتائج على تصرفات العديد من الأطراف.",
            "show_chart": False
        },
        "consumer_choice": {
            "keywords": ["utility", "consumer", "choice", "مستهلك", "المنفعة", "اختيار"],
            "en": "Consumer choice theory explains how individuals allocate income to maximize utility given prices and preferences.",
            "ar": "تشرح نظرية اختيار المستهلك كيف يوزع الأفراد دخلهم لتعظيم المنفعة في ظل الأسعار والتفضيلات.",
            "show_chart": False
        },
        "externalities": {
            "keywords": ["externality", "externalities", "الآثار الخارجية", "التلوث", "الضرر"],
            "en": "Externalities are side effects of economic activity. Negative ones like pollution harm third parties.",
            "ar": "الآثار الخارجية هي نتائج جانبية للنشاط الاقتصادي. مثلًا، التلوث هو أثر خارجي سلبي يضر بأطراف ثالثة.",
            "show_chart": False
        },
        "production_function": {
            "keywords": ["production", "function", "إنتاج", "دالة الإنتاج"],
            "en": "The production function shows the relationship between inputs (labor, capital) and output.",
            "ar": "توضح دالة الإنتاج العلاقة بين المدخلات (العمل، رأس المال) والمخرجات.",
            "show_chart": False
        },
        "price_control": {
            "keywords": ["price ceiling", "price floor", "سقف سعري", "حد أدنى للسعر"],
            "en": "Price ceilings are max legal prices (can cause shortages); price floors are minimum prices (can cause surpluses).",
            "ar": "السقوف السعرية هي أعلى أسعار قانونية (قد تؤدي إلى نقص)، والحد الأدنى للأسعار قد يؤدي إلى فائض.",
            "show_chart": False
        }
    }

    if user_question:
        with st.spinner(translate("Thinking...", "جارٍ التفكير...")):
            question_lower = user_question.lower()
            matched_topic = None

            for key, info in topics.items():
                if any(word in question_lower for word in info["keywords"]):
                    matched_topic = key
                    break

            if matched_topic:
                content = topics[matched_topic]
                answer = translate(content["en"], content["ar"])
                st.success(answer)

                # Optional chart for elasticity
                if content["show_chart"] and matched_topic == "elasticity":
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=[10, 11], y=[100, 80], mode="lines+markers", name="Demand Curve"))
                    fig.update_layout(
                        title=translate("Elasticity Example: Demand drops as Price increases",
                                        "مثال على المرونة: انخفاض الطلب مع ارتفاع السعر"),
                        xaxis_title=translate("Price", "السعر"),
                        yaxis_title=translate("Quantity Demanded", "الكمية المطلوبة"),
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(translate(
                    "Sorry, I currently only answer selected microeconomics topics. More features coming soon!",
                    "عذرًا، يمكنني حاليًا الإجابة فقط على مواضيع معينة في الاقتصاد الجزئي. المزيد من الميزات قريباً!"
                ))
