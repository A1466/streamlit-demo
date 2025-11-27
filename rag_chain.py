from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from agents.groq_llm import GroqLLM

def load_vectorstore(index_path="vectorstore/faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(index_path, embeddings)
    return vectorstore

def create_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()
    
    llm = GroqLLM()  # Use your Groq wrapper here
    
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

if __name__ == "__main__":
    chain = create_rag_chain()
    query = input("Ask me anything about the learning material: ")
    answer = chain.run(query)
    print(answer)
