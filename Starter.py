from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Ollama ChatBot
documents = SimpleDirectoryReader("data").load_data()

# bge-m3 embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

index = VectorStoreIndex.from_documents(
    documents,
)

query_engine = index.as_query_engine()
response = query_engine.query("Ask Your Question Here")
print(response)

