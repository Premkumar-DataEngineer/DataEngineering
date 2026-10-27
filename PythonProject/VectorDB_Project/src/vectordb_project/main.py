from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector


load_dotenv()

pdf_loader=PyPDFLoader("/Users/navyadev/Documents/GitHub/DataEngineering/PythonProject/VectorDB_Project/reference_docs/ORIGIN_OF_CRICKET_IN_INDIA.pdf")
docs=pdf_loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
texts=text_splitter.split_documents(docs)

embeddings=OpenAIEmbeddings()
doc_vectors=embeddings.embed_documents([t.page_content for t in texts[:5]])
print(len(doc_vectors))

CONNECTION_STRING="postgresql+psycopg2://postgres:Dev2021@localhost:5430/vector_db"
COLLECTION_NAME="origin_of_cricket_in_india"

vectorDB=PGVector.from_documents(embedding=embeddings, documents=texts, connection_string=CONNECTION_STRING, collection_name=COLLECTION_NAME)

query="When Indian cricket player first century scored?"

similar=vectorDB.similarity_search_with_score(query, k=1)

for doc in similar:
    print(doc[0].page_content)


