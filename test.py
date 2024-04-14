from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.ollama import Ollama

# This is without context
#gemma2b = Ollama(model="gemma:2b", request_timeout=30.0)
#resp = gemma2b.complete("what are michael jordan's accolades")
#print(resp)

def query(string):

    # This is with context
    reader = SimpleDirectoryReader(input_files=["./data/SOFI-2023.pdf"])
    documents = reader.load_data()

    Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

    Settings.llm = Ollama(model="mistral", request_timeout=30.0)

    index = VectorStoreIndex.from_documents(
        documents,
    )

    query_engine = index.as_query_engine()
    response = query_engine.query(string)
    # You can change this to 'return response' and then use the output of query() somewhere else
    return response
