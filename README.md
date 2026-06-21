# Legal Case Research Assistant (Enterprise RAG Workflow)

## Overview

The Legal Case Research Assistant is an enterprise-style Retrieval-Augmented Generation (RAG) application designed for legal research and analysis. The system ingests large collections of legal judgments and enables users to retrieve relevant precedents, analyze legal issues, and automatically generate structured legal memoranda.

Unlike a traditional chatbot, this application performs a complete legal research workflow by:

* Retrieving relevant legal authorities from a document corpus.
* Reranking retrieved documents for improved precision.
* Generating structured legal analysis using Gemini.
* Producing downloadable PDF legal memoranda.
* Providing document management through dynamic CRUD operations.
* Enforcing security guardrails and graceful API failover.

---

## Features

### Document Management (CRUD)

* Upload new legal judgments (PDF).
* Automatically index uploaded documents.
* Update existing documents without rebuilding the entire database.
* Delete documents dynamically.
* Page-level metadata indexing.

### Retrieval-Augmented Generation (RAG)

* PDF ingestion and chunking.
* Embedding generation using Sentence Transformers.
* Vector storage using ChromaDB.
* Semantic similarity search.
* FlashRank reranking for improved retrieval precision.

### Legal Workflow Automation

The application:

1. Accepts legal facts and research questions.
2. Retrieves relevant judgments.
3. Identifies legal issues.
4. Finds relevant precedents.
5. Extracts legal principles.
6. Generates a structured legal analysis.
7. Produces a downloadable PDF report.

### Security & Guardrails

#### Input Guardrails

Blocks malicious prompts such as:

* Prompt injections
* Jailbreak attempts
* Hidden prompt extraction attempts

#### Output Guardrails

Verifies whether generated responses are supported by the retrieved legal context and warns users if unsupported claims may exist.

### API Failover

If the Gemini API fails:

* The system does not crash.
* Retrieved legal documents are displayed as a fallback response.

---

## System Architecture

```text
User Query
     ↓
Input Guardrails
     ↓
Embedding Search
     ↓
ChromaDB Retrieval
     ↓
FlashRank Reranking
     ↓
Context Construction
     ↓
Gemini LLM
     ↓
Output Guardrails
     ↓
PDF Generation
     ↓
Legal Memo
```

---

## Tech Stack

| Component              | Technology              |
| ---------------------- | ----------------------- |
| Frontend               | Streamlit               |
| LLM                    | Google Gemini 2.5 Flash |
| Embeddings             | all-MiniLM-L6-v2        |
| Vector Database        | ChromaDB                |
| Reranking              | FlashRank               |
| PDF Processing         | PyPDF                   |
| PDF Generation         | ReportLab               |
| Environment Management | python-dotenv           |

---

## Project Structure

```text
legal-rag-assistant/

├── app.py
├── ingest.py
├── rag.py
├── guardrails.py
├── output_guardrails.py
├── pdf_generator.py
├── requirements.txt
├── data/
├── chroma_db/
├── generated_reports/
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/legal-rag-assistant.git

cd legal-rag-assistant
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

---

## Usage

### Upload Documents

Use the sidebar to upload legal judgments in PDF format.

### Generate Legal Analysis

Enter:

* Case facts
* Legal issue
* Research question

Example:

```text
Facts:

An employee was dismissed without notice or an opportunity to be heard.

Question:

Find similar judgments and explain the principles of natural justice.
```

The system will:

* Retrieve relevant judgments.
* Generate legal analysis.
* Display cited sources.
* Allow PDF download.

---

## Advanced Retrieval Pipeline

The retrieval workflow consists of:

1. Semantic vector retrieval using ChromaDB.
2. Initial retrieval of top candidate chunks.
3. FlashRank reranking.
4. Selection of highest relevance chunks.
5. Context optimization before LLM generation.

This approach reduces noisy context and improves answer quality.

---

## Security Considerations

The system blocks:

* "ignore previous instructions"
* "jailbreak"
* "system prompt"
* "reveal prompt"

Unsupported outputs are flagged by output validation before presentation.

---

## Future Improvements

* OCR support for scanned judgments.
* Hybrid keyword + vector retrieval.
* Citation extraction automation.
* Deployment on cloud infrastructure.

---

## Author

Developed as part of an Enterprise RAG Workflow Application project.
