import os
from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "DOcument_collection"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

prompt_template = """
You are an AI assistant for DOcument.

Instructions:
- Answer ONLY using the provided context.
- If the context is not relevant or missing, reply exactly:
  "Hmm, I'm not sure. Please ask information about DOcument only"

{context}

Question: {question}

Answer:
"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectorstore = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3",
)



    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# CLI test only
if __name__ == "__main__":
    rag = create_rag_chain()
    print("🤖 DOcument Chatbot (type 'exit' to quit)\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            print("Bot: Please ask a valid question.")
            continue

        print("Bot:", rag.invoke(question), "\n")
