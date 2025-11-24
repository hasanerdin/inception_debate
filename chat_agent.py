from utils import create_chat_engine

class ChatAgent:
    def __init__(self, name: str, persona: str, groq_model: str, temperature: float = 0.7, similarity_top_k: int = 5):
        self.name = name
        self.persona = persona
        self.history = []
        self.groq_model = groq_model
        self.temperature = temperature
        self.similarity_top_k = similarity_top_k
        
        self.engine = create_chat_engine(groq_model=self.groq_model, 
                                         persona_prompt=self.persona, 
                                         temperature=self.temperature, 
                                         similarity_top_k=self.similarity_top_k)

    def respond(self, message: str) -> str:
        response = self.engine.chat(message)
        
        self.history.append({
            "input": message,
            "output": str(response)
        })
        
        return str(response)
