import gradio as gr
import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma, FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain.chains import create_history_aware_retriever, create_retrieval_chain, RetrievalQA
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
import arabic_reshaper
from bidi.algorithm import get_display

import warnings
warnings.filterwarnings("ignore")

# Ensure the PDF file is available in the environment where the script is run
pdf_path = "./اللائحة الداخلية لكلية الحاسبات والذكاء الاصطناعي أكتوبر 2019.pdf"
persist_directory = "./chroma_fcai_regulations_db"

# --- RAG Setup ---

# Load and clean the document
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Function to clean Arabic text
def clean_arabic_text(text):
    """Reshape and reorder Arabic text for proper display."""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

for page in docs:
    page.page_content = clean_arabic_text(page.page_content)

# Configure and split the text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " "]
)
chunks = splitter.split_documents(docs)

# Initialize multilingual embedding model
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model_kwargs = {'device': 'cpu'} # Or 'cuda'
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Create or load the Chroma vector store
if os.path.exists(persist_directory):
    print(f"Loading existing vector store from {persist_directory}")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=hf
    )
else:
    print(f"Creating new vector store at {persist_directory}")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=hf,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print("Chroma vector store created and saved successfully!")

# Initialize Google Generative AI (Gemini)
try:
    from google.colab import userdata
    google_api_key = userdata.get("GOOGLE_API_KEY")
except ModuleNotFoundError:
    google_api_key = os.environ.get("GOOGLE_API_KEY")

if google_api_key:
    google_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        convert_system_message_to_human=True,
        google_api_key=google_api_key
    )

    # Define the prompt template - FIXED to use {question} instead of {query}
    prompt_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
{context}
----------------
Question: {question}
Answer:"""
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Create retriever interface
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )

    # Create a RetrievalQA chain with input_key specified
    qa_chain = RetrievalQA.from_chain_type(
        llm=google_llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        chain_type="stuff",
        return_source_documents=True,
        input_key="question"  # Explicitly set the input key
    )

    # --- Gradio Interface ---

    def rag_chat(query):
        """
        Function to interact with the RAG chain and get an answer.
        """
        if not google_api_key:
             return "Google API key is not configured. Please set it up to use the chatbot."
        try:
            # FIXED: Use "question" as the key instead of "query"
            result = qa_chain.invoke({"question": query})
            answer = result['result']
            sources = "\n\n📚 المصادر:\n" + "\n".join([
                f"  • {doc.metadata.get('source', 'Unknown')} | صفحة {doc.metadata.get('page', 'N/A')}"
                for doc in result["source_documents"]
            ])
            return answer + sources
        except Exception as e:
            return f"An error occurred while processing your request: {e}"

    # Create enhanced Gradio interface with custom CSS
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .input-textbox textarea {
        min-height: 120px !important;
        font-size: 16px !important;
    }
    .output-textbox textarea {
        min-height: 400px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    """

    with gr.Blocks(css=custom_css, title="FCAI Regulations Chatbot", theme=gr.themes.Soft()) as iface:
        gr.Markdown(
            """
            # 🎓 FCAI Internal Regulations Chatbot
            ### Ask questions about the Faculty of Computer and Artificial Intelligence Internal Regulations (October 2019)
            
            **Instructions:** Type your question in Arabic or English and press Submit to get an answer based on the official regulations.
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                query_input = gr.Textbox(
                    label="📝 Your Question",
                    placeholder="مثال: ما هي شروط القبول؟\nExample: What are the admission requirements?",
                    lines=5,
                    elem_classes="input-textbox"
                )
                submit_btn = gr.Button("Submit 🔍", variant="primary", size="lg")
                clear_btn = gr.Button("Clear 🗑️", variant="secondary", size="sm")
        
        with gr.Row():
            with gr.Column(scale=1):
                output_text = gr.Textbox(
                    label="💬 Answer & Sources",
                    lines=15,
                    elem_classes="output-textbox",
                    show_copy_button=True
                )
        
        gr.Markdown(
            """
            ---
            💡 **Tip:** The chatbot retrieves information directly from the official PDF document and provides source references for transparency.
            """
        )
        
        # Event handlers
        submit_btn.click(fn=rag_chat, inputs=query_input, outputs=output_text)
        query_input.submit(fn=rag_chat, inputs=query_input, outputs=output_text)
        clear_btn.click(lambda: ("", ""), outputs=[query_input, output_text])

    # Launch the Gradio app
    iface.launch(debug=True, share=False)

else:
    print("Cannot launch Gradio app without a configured Google API key.")