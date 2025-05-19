# HubSpot RAG Assistant

This project is a Retrieval-Augmented Generation (RAG) assistant for HubSpot documentation. It uses OpenAI to generate embeddings, Pinecone to store and search relevant document chunks, and FastAPI to serve a query endpoint.

---

## 🧩  Features

* Embeds HubSpot documentation from [`llms-full.txt`](https://developers.hubspot.com/docs/llms-full.txt)
* Generates OpenAI embeddings and stores them in Pinecone
* Provides a FastAPI endpoint to query the documents using semantic search
* Optional: Streamlit interface for easy testing

---

## 🗂️ Project Structure

```
hubspot-rag-app/
├── llms-full.txt              # Raw documentation source
├── embed.py                   # Script to chunk and embed data into Pinecone
├── main.py                    # FastAPI backend for querying and answering
├── streamlit_app.py           # Optional Streamlit UI for local testing
├── .env                       # API keys and config
├── requirements.txt           # Dependencies
```

---

## ⚙️ Environment Setup

1. Clone the repo

2. Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENV=your-pinecone-environment
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Populate Pinecone

To generate and store embeddings from the HubSpot documentation:

```bash
python embed.py
```

This script:

* Loads `llms-full.txt`
* Splits it into chunks
* Generates OpenAI embeddings
* Stores them in Pinecone with IDs

---

## 🚀 Run the API

```bash
uvicorn main:app --reload
```

Access the API at:
`http://localhost:8000/ask`

---

## 🧪 Test with Postman

### Endpoint

```
POST http://localhost:8000/ask
```

### Request Body

```json
{
  "question": "What are developer test accounts in HubSpot?"
}
```

### Response

```json
{
  "question": "What are developer test accounts in HubSpot?",
  "answer": "Developer test accounts are free HubSpot environments that allow you to test apps and integrations...",
  "sources": [
    "Developer test accounts will expire after 90 days if no API calls...",
    "You can create up to 10 test accounts per developer account..."
  ]
}
```

---

## 💡 Optional: Streamlit UI

To test locally with a simple web interface:

```bash
streamlit run streamlit_app.py
```

You'll get a local UI where you can enter questions and see answers and source snippets.

---

## 🧐 Technologies Used

* [OpenAI](https://platform.openai.com/docs)
* [Pinecone](https://www.pinecone.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Streamlit](https://streamlit.io/) *(optional)*

---

## 📌 Roadmap

* [ ] Add auth and usage limits
* [ ] Deploy to cloud (e.g., Render/Fly.io)
* [ ] Enable document updates/re-indexing

---

## 🙌 Credits

* HubSpot Developer Docs: [https://developers.hubspot.com/docs](https://developers.hubspot.com/docs)
* Built with OpenAI, Pinecone, FastAPI
