from loadingresumes import load_full_resumes_from_pdfs
from langchain.vectorstores import Chroma #vector store from langchain where documents are stored as vectors 
from langchain.embeddings import OpenAIEmbeddings #converts text into embeddings using openai's models

def create_db():
    docs = load_full_resumes_from_pdfs("Resumes")  #Loads all the resumes from the folder "Resumes" using your function.
    embedding = OpenAIEmbeddings(openai_api_key="your key here")
    db = Chroma.from_documents(docs, embedding, persist_directory="db")  # optional persist
    return db
#This line creates a Chroma vector database from your list of resume documents (docs), using the embedding model you just created.
#persist_directory="db" means it will save this vector store to disk in a folder called "db" so you don’t have to recompute everything later.
