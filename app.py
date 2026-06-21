import os

import streamlit as st

from dotenv import load_dotenv

import google.generativeai as genai

from rag import (
    search_documents,
    delete_document,
    get_all_documents,
    get_document_count
)

from ingest import ingest_pdf

from guardrails import is_safe

from output_guardrails import verify_output

from pdf_generator import create_pdf


# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv(
    dotenv_path=r"C:\Users\Administrator\Desktop\legal-rag-assistant\.env"
)

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("Document Management")

st.sidebar.metric(
    "Indexed Chunks",
    get_document_count()
)

# -----------------------------
# Upload / Update PDF
# -----------------------------

uploaded_file = st.sidebar.file_uploader(
    "Upload Legal Judgment",
    type=["pdf"]
)

if uploaded_file:

    save_path = os.path.join(
        "data",
        uploaded_file.name
    )

    existing_files = get_all_documents()

    # Update existing document
    if uploaded_file.name in existing_files:

        delete_document(uploaded_file.name)

    with open(save_path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    ingest_pdf(save_path)

    st.sidebar.success(
        f"{uploaded_file.name} uploaded and indexed successfully."
    )


# -----------------------------
# Delete Document
# -----------------------------

st.sidebar.subheader("Delete Document")

all_files = get_all_documents()

if len(all_files) > 0:

    selected_file = st.sidebar.selectbox(
        "Choose document",
        all_files
    )

    if st.sidebar.button(
            "Delete Selected Document"):

        delete_document(selected_file)

        file_path = os.path.join(
            "data",
            selected_file
        )

        if os.path.exists(file_path):

            os.remove(file_path)

        st.sidebar.success(
            f"{selected_file} deleted."
        )

        st.rerun()


# -------------------------------------------------
# MAIN UI
# -------------------------------------------------

st.title("Legal Case Research Assistant")

st.markdown("""
### Example Query

**Facts:**

An employee was dismissed from service without
being given notice or an opportunity to be heard.

**Question:**

Find similar judgments in the uploaded database
and explain the legal principles regarding
natural justice and wrongful termination.
""")

query = st.text_area(
    "Enter case facts and legal question:",
    height=200,
    placeholder="""
Facts:
An employee was dismissed from service without notice.

Question:
Find similar judgments and explain the legal principles.
"""
)


# -------------------------------------------------
# GENERATE ANALYSIS
# -------------------------------------------------

if st.button("Generate Legal Analysis"):

    if not query.strip():

        st.warning(
            "Please enter facts and a legal question."
        )

        st.stop()

    # Input guardrails

    if not is_safe(query):

        st.error(
            "Prompt blocked by guardrails."
        )

        st.stop()

    try:

        # ---------------------------------
        # Retrieval + Reranking
        # ---------------------------------

        results = search_documents(query)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        if len(documents) == 0:

            st.warning(
                "No relevant cases found."
            )

            st.stop()

        # ---------------------------------
        # Display Retrieved Authorities
        # ---------------------------------

        st.subheader(
            "Retrieved Legal Authorities"
        )

        for doc, meta in zip(
                documents,
                metadatas):

            st.markdown(
                f"### {meta.get('file', 'Unknown File')}"
            )

            st.markdown(
                f"**Page:** {meta.get('page', 'Unknown')}"
            )

            st.write(doc)

            st.markdown("---")

        # ---------------------------------
        # Build Context
        # ---------------------------------

        context = ""

        for doc, meta in zip(
                documents,
                metadatas):

            context += f"""
Case File: {meta.get('file', 'Unknown')}
Page: {meta.get('page', 'Unknown')}

{doc}

--------------------------------------------------
"""

        # ---------------------------------
        # Chain-of-Thought Prompt
        # ---------------------------------

        prompt = f"""
You are an expert Indian legal research assistant.

STRICT RULES:

- Use ONLY the supplied context.
- Never invent facts, statutes, precedents or holdings.
- If information is unavailable, explicitly state:
  "The retrieved documents do not contain sufficient information."
- Cite case names and page numbers whenever possible.

Reason step-by-step.

Step 1:
Identify legal issues.

Step 2:
Identify relevant precedents.

Step 3:
Extract governing legal principles.

Step 4:
Compare user facts with retrieved precedents.

Step 5:
Provide a reasoned legal conclusion.

Output Format:

## Legal Issues

## Relevant Precedents

## Governing Principles

## Comparative Analysis

## Legal Opinion

Context:

{context}

User Facts and Question:

{query}
"""

        # ---------------------------------
        # LLM Call
        # ---------------------------------

        response = model.generate_content(
            prompt
        )

        memo = response.text

        # ---------------------------------
        # Output Guardrail
        # ---------------------------------

        if not verify_output(
                context,
                memo):

            st.warning(
                "Warning: Some parts of the analysis may not be fully supported by the retrieved documents."
            )

        # ---------------------------------
        # Display Memo
        # ---------------------------------

        st.subheader(
            "Generated Legal Analysis"
        )

        st.write(memo)

        # ---------------------------------
        # Sources
        # ---------------------------------

        st.subheader(
            "Sources Used"
        )

        shown = set()

        for meta in metadatas:

            source = (
                f"{meta.get('file', 'Unknown')} "
                f"(Page {meta.get('page', 'Unknown')})"
            )

            if source not in shown:

                st.write(source)

                shown.add(source)

        # ---------------------------------
        # Generate PDF
        # ---------------------------------

        pdf_path = create_pdf(memo)

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="Download Legal Memo PDF",
                data=file,
                file_name="legal_memo.pdf",
                mime="application/pdf"
            )

    except Exception as e:

        # ---------------------------------
        # Graceful Fallback
        # ---------------------------------

        st.warning(
            "AI generation failed. Showing retrieved documents instead."
        )

        st.error(str(e))

        try:

            st.subheader(
                "Retrieved Documents"
            )

            for doc in documents:

                st.write(doc)

                st.markdown("---")

        except:

            st.write(
                "No documents retrieved."
            )