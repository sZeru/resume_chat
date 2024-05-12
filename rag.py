import chromadb
import io
from llama_index.legacy import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.core.settings import Settings
from llama_index.legacy.embeddings import resolve_embed_model
from llama_index.legacy.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, PromptTemplate
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.ollama import Ollama
from pypdf import PdfReader


#Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

#Settings.llm = Ollama(model="mistral", request_timeout=30.0)

Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-en-v1.5")

Settings.llm = Ollama(model="mistral", request_timeout=30.0)

# load documents
reader = SimpleDirectoryReader("./data")
documents = reader.load_data()

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# get collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create your index
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

def query(string, pdf_data):
    Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

    Settings.llm = Ollama(model="mistral", request_timeout=30.0)

    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    # convert to readable format
    pdf = io.BytesIO(pdf_data)

    text = PdfReader(pdf)
    resume = text.pages[0].extract_text()
    prompt = "With this resume as context:\n" + resume + "\nPlease respond to the following query:\n" + string
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response
