# 🩺 Medical Chatbot using RAG | OpenAI + Pinecone + Flask

A smart **Medical Chatbot** built using a **Retrieval-Augmented Generation (RAG)** approach that answers medical-related queries using a custom medical knowledge base.  
The chatbot retrieves relevant medical context from stored documents and generates intelligent, context-aware responses using **OpenAI LLMs**.

This project is built with **Flask**, **LangChain**, **OpenAI Embeddings**, and **Pinecone Vector Database**, and is deployed on **Render**.

## 🚀 Live Demo
[Try the deployed Medical Chatbot on Render](https://medical-chatbot-zhk6.onrender.com)

---

## 📌 Features

- 💬 Ask medical-related questions in natural language
- 🧠 Uses **RAG (Retrieval-Augmented Generation)** for context-based responses
- 📚 Retrieves relevant information from a custom medical knowledge base (PDF documents)
- 🔎 Semantic search using **OpenAI Embeddings**
- 🗂️ Stores and retrieves embeddings with **Pinecone Vector Database**
- ⚡ Lightweight backend built with **Flask**
- ☁️ Deployed on **Render**
- 🔒 Secure configuration using environment variables

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### LLM & AI
- OpenAI GPT Model
- OpenAI Embeddings
- LangChain
- LangChain Community
- LangChain OpenAI
- LangChain Pinecone

### Vector Database
- Pinecone

### Document Processing
- PyPDF

### Deployment
- Render
- Gunicorn

---

## 🧩 How It Works

1. Medical documents are loaded from the knowledge base.
2. Documents are split into smaller chunks.
3. **OpenAI Embeddings** are generated for each chunk.
4. Embeddings are stored in **Pinecone**.
5. When a user asks a question:
   - The query is converted into embeddings
   - Relevant chunks are retrieved from Pinecone
   - Retrieved context is passed to the **OpenAI LLM**
   - The chatbot generates a relevant medical response based on the retrieved context

---

## 📂 Project Structure

```bash
Medical-chatbot/
│── app.py
│── store_index.py
│── requirements.txt
│── runtime.txt
│── setup.py
│── README.md
│── LICENSE
│── .gitignore
│── templates/
│   └── chat.html
│── static/
│   └── style.css
│── data/
│   └── Medical_book.pdf
│── src/
│   ├── __init__.py
│   ├── helper.py
│   └── prompt.py
```

## ⚙️ Installation & Setup

# 1. Clone the Repository

```bash
git clone https://github.com/anushkapolley/Medical-chatbot.git
cd Medical-chatbot
```
# 2. Create a Virtual Environment

```bash
python -m venv medibot
```
# 3. Activate the Environment

_ **Windows**
```bash
medibot\Scripts\activate
```
_ **Mac/Linux**

```bash
source medibot/bin/activate
```

# 4. Install Dependencies

```bash
pip install -r requirements.txt
```

# 🔐 Environment Variables

_ **Create a .env file in the root directory and add the following:**

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
OPENAI_API_KEY=your_openai_api_key

# ⚠️ Make sure your Pinecone index (for example: medical-chatbot) already exists and is accessible before running the app or deploying on Render.

# 🧠 Create and Store Embeddings in Pinecone

Before running the chatbot, you need to process your medical knowledge base and upload embeddings to Pinecone.

python store_index.py

_ **This script will:**

Load the medical PDF/document
Split the content into chunks
Generate embeddings using OpenAI
Store the vectors inside your Pinecone index

# ▶️ Run the Project Locally

```bash
python app.py
```

_ **Or with Flask:**

```bash
flask run
```

_ **Open in browser:**

```bash
http://127.0.0.1:5000
```

# ☁️ Deployment on Render

This project is deployed using Render.

_ **Render Deployment Steps**

Push your project to GitHub
Go to Render
Create a New Web Service
Connect your GitHub repository
Configure the service with the following:
Build Command
pip install -r requirements.txt
Start Command
gunicorn app:app
Environment Variables

_ **Add these in the Render Dashboard → Environment section:**

OPENAI_API_KEY
PINECONE_API_KEY
PINECONE_ENV
Click Deploy

# 📦 Requirements

Example requirements.txt:
langchain==0.3.27
langchain-community==0.3.27
langchain-openai==0.3.28
langchain-pinecone==0.2.11
openai==1.99.9
Flask==3.1.3
pypdf==6.1.1
python-dotenv==1.1.1
tiktoken
gunicorn
-e .

# ⚠️ Important Notes
Your Pinecone index must already exist before deployment.
If your app works locally but fails on Render, check:
API keys are correctly added in Render
Pinecone environment/region is correct
The index name matches exactly in your code
gunicorn app:app matches your Flask app filename and variable name


# 🔮 Future Improvements
Add conversation memory
Improve chatbot UI/UX
Add response source citations
Support multiple medical documents
Add authentication for user sessions
Add Docker support
Enable streaming responses for better user experience


# ⚠️ Disclaimer
This chatbot is built for educational and informational purposes only.
It is not a substitute for professional medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional for any medical concerns.


# 👩‍💻 Author
Anushka Polley
AI/ML Enthusiast | LLM & GenAI Projects


#⭐ Support
If you found this project useful, consider giving it a star ⭐ on GitHub!
