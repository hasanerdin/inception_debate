import os

from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from api_keys import GROQ_API_KEY, HF_API_KEY


# groq_model = "llama-3.3-70b-versatile" 
groq_model = "llama-3.1-8b-instant"
# groq_model = "meta-llama/llama-guard-4-12b" 

embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
embedding_path = "./embedding_model/"
data_path = "./data"
vector_index_path = "./vector_index"

"""Add API keys to environment variables for library access."""
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["HF_API_KEY"] = HF_API_KEY
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def create_vector_index():
    """Create and store a vector index from the given file.
    
    Args:
        file_path (str): Path to the text file to index.
    """
    # Load documents from the specified file
    documents = SimpleDirectoryReader(data_path).load_data()

    # Initialize Text Splitter
    text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
    
    # Initialize HuggingFace Embeddings
    embeddings = get_embedding_model()

    # Create Vector Index
    vector_index = VectorStoreIndex.from_documents(
        documents=documents,
        transformations=[text_splitter],
        embed_model=embeddings,
    )

    # Persist the vector index to storage
    vector_index.storage_context.persist(persist_dir=vector_index_path)

def get_embedding_model() -> HuggingFaceEmbedding:
    """Initialize and return a HuggingFace embedding model.

    Args:
        embedding_model_path (str): Path to the embedding model.
    Returns:
        HuggingFaceEmbedding: Configured embedding model.
    """
    embeddings = HuggingFaceEmbedding(
        model_name=embedding_model,
        cache_folder=embedding_path,
    )
    return embeddings

def get_groq_llm(groq_model: str, temperature: float = 0.7) -> Groq:
    """Initialize and return a Groq LLM.

    Returns:
        Groq: Configured Groq LLM.
    """

    llm = Groq(model=groq_model, 
               temperature=temperature, 
               token=os.environ.get("GROQ_API_KEY"))
    return llm

def get_retriever(embeddings: HuggingFaceEmbedding, similarity_top_k: int = 5):
    """Load a vector index from storage.    
    Args:
        embeddings (HuggingFaceEmbedding): Embedding model to use.
    Returns:
        VectorIndex: Loaded vector index.
    """

    storage_context = StorageContext.from_defaults(persist_dir=vector_index_path)
    vector_index = load_index_from_storage(
        storage_context=storage_context,
        embed_model=embeddings,
    )
    retriever = vector_index.as_retriever(similarity_top_k=similarity_top_k)
    return retriever

def create_prefix_messages(persona_prompt: str) -> list[ChatMessage]:
    """Create prefix messages for the chat engine.
    Args:
        persona_prompt (str): Persona prompt for the chat engine.
    Returns:
        list[ChatMessage]: List of prefix chat messages.
    """

    prefix_messages = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=(
                "You are about to engage in a debate."
                f" Here is your persona and instructions:\n{persona_prompt}\n"
                "Provide concise and accurate answers based on the provided context."
            ),
        )
    ]
    return prefix_messages

def create_chat_engine(groq_model: str, persona_prompt: str, similarity_top_k: int = 5, temperature: float = 0.7) -> ContextChatEngine:
    """Create and return a Context Chat Engine.
    Args:
        persona_prompt (str): Persona prompt for the chat engine.
    Returns:
        ContextChatEngine: Configured chat engine.
    """

    # Initialize Groq LLM
    llm = get_groq_llm(groq_model, temperature=temperature)
    
    # Initialize HuggingFace Embeddings
    embeddings = get_embedding_model()
    
    # Load Vector Index from storage
    retriever = get_retriever(embeddings, similarity_top_k=similarity_top_k)
    
    # Create Prefix Messages
    prefix_messages = create_prefix_messages(persona_prompt=persona_prompt)

    # Create Chat Memory Buffer (use from_defaults and `token_limit` per library API)
    chat_memory = ChatMemoryBuffer.from_defaults()

    # Create Context Chat Engine
    chat_engine = ContextChatEngine.from_defaults(
        llm=llm,
        retriever=retriever,
        chat_memory=chat_memory,
        prefix_messages=prefix_messages,
        response_mode="compact",
    )

    return chat_engine
