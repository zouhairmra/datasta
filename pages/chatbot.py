import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core import VectorStoreIndex, SimpleNodeParser, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.service_context import ServiceContext
from llama_index.core.memory import ChatMemoryBuffer

# Streamlit page config
st.set_page_config(page_title="💬 AI Tutor", layout="wide")
st.title("📘🤖 Tutor IA en économie & mathématiques (arabe)")

# Load the model from Ollama (must be running locally)
llm = Ollama(model="llama3")

# Example knowledge base (you can customize this later)
documents = [
    Document(text="""
        الاقتصاد الجزئي يدرس سلوك الأفراد والمؤسسات في اتخاذ القرارات حول تخصيص الموارد المحدودة. 
        مفاهيم أساسية تشمل: العرض والطلب، التوازن في السوق، مرونة الأسعار، التكلفة الحدية، والإيراد الحدي.
        
        الرياضيات للأعمال تشمل: النسب المئوية، الفائدة البسيطة والمركبة، تحليل التكلفة والعائد، المعادلات الخطية، والمصفوفات.
    """)
]

# Embedding + parser
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
parser = SimpleNodeParser()

# Vector index
nodes = parser.get_nodes_from_documents(documents)
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
index = VectorStoreIndex(nodes, service_context=service_context)

# Memory
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

# Chat engine
chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt="أنت مساعد ذكي لشرح مفاهيم الاقتصاد الجزئي والرياضيات التجارية باللغة العربية للطلاب.",
)

# Chat interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("📝 اسأل عن الاقتصاد الجزئي أو الرياضيات للأعمال")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    response = chat_engine.chat(user_input)
    st.session_state.chat_history.append(("ai", response.response))

# Show conversation
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("🧑‍🎓").markdown(msg)
    else:
        st.chat_message("🤖").markdown(msg)
