import os
from src.chat_agent import ChatAgent

class DebateJudge:
    judge_persona = """
        You are an impartial debate judge. Your role is to evaluate a two-agent debate based solely on the arguments presented in the conversation history provided to you.

        Guidelines:
        1. You do not take sides based on personal beliefs or external knowledge.
        2. You judge only the reasoning, evidence, clarity, and logical coherence shown in the debate history.
        3. Identify which agent presented stronger arguments overall.
        4. Provide a brief, concise justification summarizing the key reasons for your decision.
        5. Your final answer must include:
        - The winner (Agent A or Agent B)
        - A short explanation of why that agent's reasoning was stronger.
        6. Do not restate the entire debate. Do not generate new arguments.
        7. Be objective, analytical, and strictly focused on debate quality.
        8. Keep your answers short and concise.
        """
    
    def __init__(self, groq_model: str, persona_a: str, persona_b: str, temperature: float = 0.7):
        
        self.judge = self.create_chatbot(
            chatbot_name="Judge Bot",
            persona=self.judge_persona,
            groq_model=groq_model,
            temperature=temperature,
        )

        self.chatbot_A = self.create_chatbot(
            "Bot A",
            persona_a,
            groq_model,
            temperature,
        )
        self.chatbot_B = self.create_chatbot(
            "Bot B",
            persona_b,
            groq_model,
            temperature,
        )
        
        self.round_num = 0
        self.history = []
                
    @staticmethod
    def create_chatbot(chatbot_name: str, persona: str, groq_model: str, temperature: float) -> ChatAgent:
        chatbot = ChatAgent(
            name=chatbot_name,
            persona=persona,
            groq_model=groq_model,
            temperature=temperature,
        )

        return chatbot

    def evaluate(self) -> str:
        # Build a plain-text summary of the rounds for the judge
        history_text = "\n".join([str(item) for item in self.history])

        # Ask the judge model (pass a string, not the list)
        judge_decision = self.judge.respond(message=history_text)

        # Record judge decision in history and return Chatbot-format messages
        self.history.append({
            "round": "Judge Decision",
            "Judge Bot": judge_decision,
        })

        return judge_decision

    def start_new_round(self) -> str:
        message_A = self.chatbot_A.respond(
            message="Make your opening statement."
            if self.round_num == 0
            else self.chatbot_B.history[-1]["output"]
        )
        print("Message A:", message_A)

        message_B = self.chatbot_B.respond(
            message=self.chatbot_A.history[-1]["output"]
        )
        print("Message B:", message_B)

        self.history.append({
            "round": self.round_num + 1,
            "chatbot_A": message_A,
            "chatbot_B": message_B,
        })

        return self.history[-1]
    
    def get_history(self) -> list[dict]:
        # Return messages in the format expected by gr.Chatbot: a list of dicts
        # Each dict should have 'role' and 'content' keys.
        messages = []

        for entry in self.history:
            messages.append({"role": "system", "content": f"Round {entry['round']}"})
            if entry['round'] == "Judge Decision":
                messages.append({"role": "assistant", "content": f"Judge Bot: {entry['Judge Bot']}"})
                continue
            
            messages.append({"role": "assistant", "content": f"Bot A: {entry['chatbot_A']}"})
            messages.append({"role": "assistant", "content": f"Bot B: {entry['chatbot_B']}"})
        
        return messages
    