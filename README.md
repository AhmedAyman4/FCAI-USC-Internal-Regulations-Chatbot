# FCAI Regulations Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about the **Faculty of Computer and Artificial Intelligence (FCAI)** internal regulations (October 2019). The system uses **LangChain**, **Google Gemini**, and **Gradio** to provide accurate, source-referenced answers in both Arabic and English.

---

## Live Demo

**Try the chatbot online:** [https://huggingface.co/spaces/ahmed-ayman/fcai-usc-internal-regulations-chatbot](https://huggingface.co/spaces/ahmed-ayman/fcai-usc-internal-regulations-chatbot)

---

## Features

* **Bilingual Support:** Handles questions in Arabic and English with proper Arabic text processing
* **Intelligent Retrieval:** Uses MMR (Maximal Marginal Relevance) search for diverse, relevant context
* **Source Attribution:** Provides page references from the original PDF document
* **Contextual Reasoning:** Infers answers logically when information is not explicitly stated
* **Persistent Vector Store:** Saves embeddings locally to avoid reprocessing the PDF
* **Modern Web Interface:** Clean, responsive Gradio interface with custom styling

---

## Prerequisites

* Python 3.8 or higher
* Google API key for Gemini access
* At least 2GB of available RAM for embeddings

---

## Installation

### 1. Clone or download the project

```bash
git clone <repository-url>
cd fcai-regulations-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```txt
gradio
langchain
langchain-community
langchain-google-genai
langchain-huggingface
chromadb
sentence-transformers
pypdf
arabic-reshaper
python-bidi
```

### 3. Set up your Google API key

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

To get a Google API key, visit: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

## Usage

### Run the application

```bash
python app.py
```

The first run will create a vector database, which may take a few minutes. Subsequent runs will load the existing database.

Once running, open the provided local URL (typically `http://127.0.0.1:7860`) in your browser.

### Ask questions

Type your question in the text box and click **Submit** or press Enter. Examples:

**Arabic:**
* ما هي شروط القبول في الكلية؟
* كم عدد الساعات المعتمدة المطلوبة للتخرج؟
* ما هي نسبة الحضور المطلوبة؟

**English:**
* What are the admission requirements?
* What is the percentage allocated for the final exam?
* How many credit hours are required for graduation?

---

## Project Structure

```
fcai-regulations-chatbot/
├── app.py                                    # Main application code
├── requirements.txt                          # Python dependencies
├── اللائحة الداخلية لكلية الحاسبات...pdf   # Regulations PDF document
└── chroma_fcai_regulations_db/               # Vector database (created on first run)
    ├── chroma.sqlite3
    └── [embedding files]
```

---

## Technical Details

### Components

* **Document Loader:** PyPDFLoader extracts text from the regulations PDF
* **Text Processing:** Arabic text is reshaped and reordered for proper display using arabic-reshaper and python-bidi
* **Text Splitting:** RecursiveCharacterTextSplitter creates 3000-character chunks with 1000-character overlap
* **Embeddings:** HuggingFace's multilingual-e5-base model generates vector representations
* **Vector Store:** ChromaDB stores and retrieves document embeddings
* **LLM:** Google Gemini 2.5 Flash generates contextual answers
* **Retrieval Strategy:** MMR with k=8 and lambda=0.7 for diverse, relevant results
* **Interface:** Gradio provides the web-based chat interface

### Configuration

Key parameters in `app.py`:

```python
chunk_size = 3000          # Text chunk size
chunk_overlap = 1000       # Overlap between chunks
search_k = 8               # Number of chunks to retrieve
fetch_k = 25               # Initial candidates for MMR
lambda_mult = 0.7          # Diversity factor (0-1)
temperature = 0.0          # LLM creativity (0=deterministic)
```

---

## Troubleshooting

**Issue:** "Google API key is not configured"
* **Solution:** Ensure the GOOGLE_API_KEY environment variable is set correctly

**Issue:** Vector database creation is slow
* **Solution:** This is normal on first run. The database is saved and reused on subsequent runs

**Issue:** Arabic text appears garbled
* **Solution:** Ensure arabic-reshaper and python-bidi are installed correctly

**Issue:** Out of memory errors
* **Solution:** Reduce chunk_size or search_k parameters, or use a machine with more RAM

---

## Technologies Used

* **LangChain:** Framework for building LLM applications
* **Google Gemini:** Large language model for answer generation
* **ChromaDB:** Vector database for semantic search
* **HuggingFace Transformers:** Multilingual embeddings model
* **Gradio:** Web interface framework
* **PyPDF:** PDF document processing
* **arabic-reshaper & python-bidi:** Arabic text rendering

---

## License

This project is for educational and informational purposes. Please refer to your institution's guidelines regarding the use and distribution of official documents.

---

## Contributing

Contributions are welcome. Please ensure any changes maintain compatibility with both Arabic and English text processing.
