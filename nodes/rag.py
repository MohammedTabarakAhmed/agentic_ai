"""
txt file
   ↓ TextLoader
raw text
   ↓ RecursiveCharacterTextSplitter
   chunk_size=600, chunk_overlap=60
chunks of text
   ↓ HuggingFaceEmbeddings (all-MiniLM-L6-v2)
vectors (numbers)
   ↓ FAISS.from_documents
FAISS index
   ↓ save_local("faiss_index")
saved to disk

──── when user asks something ────

user_goal (from state notebook)
   ↓ same embeddings model
vector
   ↓ FAISS.similarity_search(k=3)
top 3 matching chunks (Document objects)
   ↓ [doc.page_content for doc in docs]
   (loop to extract just the text)
["chunk1 text", "chunk2 text", "chunk3 text"]
   ↓
state["retrieved_docs"] updated ✓
   ↓
notebook carried to next node via LangGraph
"""

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os
from state import AgentState

embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

if os.path.exists("faiss_index"):
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
else:
    loader = TextLoader("docs/coding_guide.txt")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
    chunks = splitter.split_documents(documents)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("faiss_index")


def rag_search(state:AgentState):
    docs=vector_store.similarity_search(query=state['user_goal'],k=3) #k=3 gove me 3 most relevent chunks
    return {"retrieved_docs": [doc.page_content for doc in docs]} #you loop thorugh and just load page_content not metadata