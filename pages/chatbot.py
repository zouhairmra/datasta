import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.service_context import ServiceContext
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondenseQuestionChatEngine

# --- Sidebar ---
st.sidebar.title("📚 Datasta TutorBot")
st.sidebar.markdown("Ask me anything about Microeconomics or Business Math in Arabic!")

# --- Initialize only once ---
@st.cache_resource
def initialize_chat_engine():
    # Use Arabic-friendly embedding
    embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-base")

    # Local LLM from Ollama
    llm = Ollama(model="llama3")

    # Mini knowledge base
    content = """
    الاقتصاد الجزئي هو فرع من فروع الاقتصاد يركز على سلوك الأفراد والشركات في اتخاذ القرارات بشأن تخصيص الموارد. من مفاهيمه: العرض والطلب، توازن السوق، مرونة الأسعار، وتكاليف الإنتاج.

    في الرياضيات للأعمال، نستخدم مفاهيم مثل الدوال، المعادلات الخطية، التفاضل، ونسب النمو لفهم وتحليل مسائل اقتصادية مثل تعظيم الربح أو تقليل التكاليف.
    """

    documents = [Document(text=content)]
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model
    )

    index = VectorStoreIndex(nodes, service_context=service_context)
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

    return CondenseQuestionChatEngine.from_defaults(
        index=index,
        service_context=service_context,
        memory=memory,
        verbose=True,
    )

# --- Load engine ---
chat_engine = initialize_chat_engine()

# --- Chat UI ---
st.title("🤖 Microeconomics & Business Math Chatbot")
st.markdown("اسألني عن مفاهيم الاقتصاد الجزئي أو رياضيات الأعمال باللغة العربية:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("اكتب سؤالك هنا...")

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process user question
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("أفكر في الإجابة..."):
            response = chat_engine.chat(user_input)
            st.markdown(response.response)
            st.session_state.chat_history.append({"role": "assistant", "content": response.response})
