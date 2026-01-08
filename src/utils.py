from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.base.llms.types import ChatMessage, MessageRole

from src.config import (
    GROQ_API_KEY,
    HF_API_KEY,
    GROQ_MODEL,
    EMBEDDING_MODEL,
    DATA_PATH,
    VECTOR_INDEX_PATH,
    EMBEDDING_CACHE_PATH,
)

# ------------------------
# Embeddings
# ------------------------

def get_embedding_model() -> HuggingFaceEmbedding:
    return HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL,
        cache_folder=str(EMBEDDING_CACHE_PATH),
        api_key=HF_API_KEY,
    )

# ------------------------
# LLM
# ------------------------

def get_groq_llm(temperature: float = 0.7) -> Groq:
    return Groq(
        model=GROQ_MODEL,
        temperature=temperature,
        api_key=GROQ_API_KEY,
    )

# ------------------------
# Vector Index
# ------------------------

def create_vector_index() -> None:
    documents = SimpleDirectoryReader(str(DATA_PATH)).load_data()
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)

    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[splitter],
        embed_model=get_embedding_model(),
    )

    index.storage_context.persist(persist_dir=str(VECTOR_INDEX_PATH))

def load_retriever(similarity_top_k: int = 5):
    storage_context = StorageContext.from_defaults(
        persist_dir=str(VECTOR_INDEX_PATH)
    )

    index = load_index_from_storage(
        storage_context,
        embed_model=get_embedding_model(),
    )

    return index.as_retriever(similarity_top_k=similarity_top_k)

# ------------------------
# Chat Engine
# ------------------------

def create_prefix_messages(persona_prompt: str) -> list[ChatMessage]:
    return [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=(
                "You are about to engage in a debate.\n"
                f"Persona and instructions:\n{persona_prompt}\n"
                "Provide concise and accurate answers based on the context."
            ),
        )
    ]

def create_chat_engine(
    persona_prompt: str,
    similarity_top_k: int = 5,
    temperature: float = 0.7,
) -> ContextChatEngine:

    return ContextChatEngine.from_defaults(
        llm=get_groq_llm(temperature),
        retriever=load_retriever(similarity_top_k),
        chat_memory=ChatMemoryBuffer.from_defaults(),
        prefix_messages=create_prefix_messages(persona_prompt),
        response_mode="compact",
    )