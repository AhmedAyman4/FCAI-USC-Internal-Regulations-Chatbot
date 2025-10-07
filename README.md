# 🎓 FCAI Regulations Chatbot

This is a simple chatbot that answers questions about the **Faculty of Computer and Artificial Intelligence (FCAI)** internal regulations (October 2019).
It uses **LangChain**, **Gradio**, and **Google Gemini** to search the official PDF and give answers in **Arabic or English**.

---

## ⚙️ Features

* Reads and understands Arabic and English questions
* Uses Google Gemini for smart answers
* Retrieves info from the official regulations PDF
* Runs locally with a Gradio web interface

---

## 📦 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```txt
gradio
langchain
langchain-community
langchain-google-genai
langchain-huggingface
chromadb
sentence-transformers
arabic-reshaper
python-bidi
```

### 2. Add your Google API key

```bash
export GOOGLE_API_KEY="your_key_here"
```

*(Use `setx` on Windows if needed.)*

### 3. Run the app

```bash
python app.py
```

Then open the Gradio link in your browser.

---

## 💬 Example Questions

* 🇸🇦 ما هي شروط القبول في الكلية؟
* 🇬🇧 What are the graduation requirements?

---

## 🗂️ Files

* `app.py` → main code
* `اللائحة الداخلية لكلية الحاسبات والذكاء الاصطناعي أكتوبر 2019.pdf` → regulation file
* `chroma_fcai_regulations_db/` → saved vector database

---

## 🧠 Tools Used

* LangChain
* HuggingFace Embeddings
* Google Gemini
* Gradio
