import os
import pymupdf
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def extract_text_from_pdf(pdf_path):
    """Extracts raw text from the PDF."""
    with pymupdf.open(pdf_path) as doc:
        text = " ".join([page.get_text("text") for page in doc])
    return " ".join(text.split())


def extract_carbon_value_with_rag(text):
    """Method 2: RAG (Fast, low token usage)"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embeddings)

    query = "Total product footprint kg CO2e"
    best_chunks = vector_store.similarity_search(query, k=4)
    context = "\n".join([doc.page_content for doc in best_chunks])

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    prompt = PromptTemplate.from_template("""
        You are a precise data extraction assistant. Look at the following text excerpt from an environmental report.
        Extract the total product carbon footprint (Net GHG emissions) in kg CO2e.

        If the text lists multiple footprint values for different product configurations (e.g., different processors or storage sizes), return ONLY the value for the lowest/baseline configuration.

        Text excerpt:
        {context}

        Return ONLY the numerical value as a float (e.g., 303.0). Do not include units or any other text.
        If the data is not in the text, return "None".
        """)

    chain = prompt | llm
    result = chain.invoke({"context": context})

    input_tokens = (
        result.usage_metadata.get("input_tokens", 0) if result.usage_metadata else 0
    )

    try:
        val = float(result.content.strip())
        return val, input_tokens
    except ValueError:
        return None, input_tokens


def extract_carbon_value_full_text(text):
    """Method 1: Full Text (Slower, high token usage)"""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    prompt = PromptTemplate.from_template("""
        You are a precise data extraction assistant. Look at the following full environmental report.
        Extract the total product carbon footprint (Net GHG emissions) in kg CO2e.

        If the text lists multiple footprint values for different product configurations (e.g., different processors or storage sizes), return ONLY the value for the lowest/baseline configuration.

        Full Document:
        {context}

        Return ONLY the numerical value as a float (e.g., 303.0). Do not include units or any other text.
        If the data is not in the text, return "None".
        """)

    chain = prompt | llm
    result = chain.invoke({"context": text})

    input_tokens = (
        result.usage_metadata.get("input_tokens", 0) if result.usage_metadata else 0
    )

    try:
        val = float(result.content.strip())
        return val, input_tokens
    except ValueError:
        return None, input_tokens


if __name__ == "__main__":
    demo_pdf = "apple/14-inch_MacBook_Pro_PER_Oct2023.pdf"

    print("1. Extracting text from PDF...")
    full_text = extract_text_from_pdf(demo_pdf)
    print(f"-> Extracted {len(full_text)} characters.\n")

    print("--------------------------------------------------")
    print("RUNNING METHOD 1: FULL TEXT (No RAG)")
    print("--------------------------------------------------")
    full_val, full_tokens = extract_carbon_value_full_text(full_text)
    print(f"Value Found: {full_val} kg CO2e")
    print(f"Tokens Used: {full_tokens}")

    print("\n--------------------------------------------------")
    print("RUNNING METHOD 2: RAG (Retrieval-Augmented Generation)")
    print("--------------------------------------------------")
    rag_val, rag_tokens = extract_carbon_value_with_rag(full_text)
    print(f"Value Found: {rag_val} kg CO2e")
    print(f"Tokens Used: {rag_tokens}")

    print("\n--------------------------------------------------")
    print("CONCLUSION")
    print("--------------------------------------------------")
    if full_tokens > 0:
        reduction = ((full_tokens - rag_tokens) / full_tokens) * 100
        print(f"✅ RAG saved {full_tokens - rag_tokens} tokens per document!")
        print(f"✅ That is a {reduction:.1f}% reduction in API costs.")