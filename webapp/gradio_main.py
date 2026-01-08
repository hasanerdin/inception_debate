import gradio as gr
import os

from src.utils import create_vector_index, data_path
from src.judge import DebateJudge

persona_a = """
    You firmly believe the ending of Inception takes place inside a dream. You always emphasize visual inconsistencies, unresolved plot logic, and symbolic clues pointing toward a dream state. Your answers must stay short (2-3 sentences) and confidently argue that the top is irrelevant because Cobb never left the dream.
"""

persona_b = """
    You insist the final scene is set in reality. You focus on emotional resolution, narrative logic, and details like the children aging and wearing different clothes. Your answers must remain short (2-3 sentences) and express certainty that Cobb truly returned to the real world.
"""

judge = None

groq_model = "llama-3.1-8b-instant"
temperature = 0.7

def process_file(uploaded_file) -> str:
    if uploaded_file is None:
        return "❌ No file uploaded."
    
    try:
        os.makedirs(data_path, exist_ok=True)

        dest_path = os.path.join(data_path, os.path.basename(uploaded_file.name))
        with open(uploaded_file, "rb") as s, open(dest_path, "wb") as f:
            f.write(s.read())
        
        # Create vector index from the uploaded file
        create_vector_index()
        return "✅ File processed and vector index created successfully."
    except Exception as e:
        return f"❌ Error processing file: {str(e)}"

def create_judge(model_name, temp_value, persona_a_role: str, persona_b_role: str) -> str:
    global persona_a, persona_b, judge, groq_model, temperature
    groq_model = model_name
    temperature = temp_value
    persona_a =  persona_a_role 
    persona_b =  persona_b_role

    try:
        judge = DebateJudge(groq_model, persona_a, persona_b, temperature)

        return "✅ Judge created successfully."
    except Exception as e:
        return f"❌ Error creating judge: {str(e)}"

def start_new_round():
    if judge is None:
        return "Please set both personas before starting the debate."
    
    judge.start_new_round()

    return judge.get_history()

def evaluate_debate():
    if judge is None:
        return "Please set personas and start the debate first."
    
    judge.evaluate()
    
    return judge.get_history()

with gr.Blocks() as demo:
    gr.Markdown("# Chat Debate — Setup Phase")

    with gr.Row():
        # txt file upload section
        gr.Markdown("## 1. Upload debate context file")
        file_uploader = gr.File(file_types=[".txt"], 
                                type="filepath",
                                label="Upload Text File", 
                                interactive=True)
        file_status = gr.Markdown(label="File Status", value="⏳ Processing...")
        file_uploader.change(process_file, file_uploader, file_status)
    
    with gr.Row(): 
        # Model selection section
        with gr.Column():
            gr.Markdown("## 1. Select Groq Model")
            model_dropdown = gr.Dropdown(
                label="Select Groq Model",
                choices=["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
                value=groq_model,
                interactive=True,
            )

            # Temperature slider section
            gr.Markdown("## 2. Set Temperature")
            slider = gr.Slider(minimum=0.0, maximum=1.0, value=temperature, step=0.1, label="Temperature")

        # Persona section
        with gr.Column():   
            gr.Markdown("## 2. Give personas to the chatbots")

            with gr.Row():
                persona_a = gr.Textbox(label="Persona A", value=persona_a)
                persona_b = gr.Textbox(label="Persona B", value=persona_b)

    with gr.Row():
        create_model = gr.Button("Create Chatbots")
        model_creation_status = gr.Markdown(label="Chatbot Creation Status", value="⏳ Processing...")
        create_model.click(create_judge, [model_dropdown, slider, persona_a, persona_b], model_creation_status)
        

    # Start debate section
    with gr.Column() as debate_column:
        gr.Markdown("## 3. Start the debate")
        # I want a chatbot that hold previous messages
        chatbot = gr.Chatbot(label="Debate Output")
        
        with gr.Row():
            # When button is clicked, start the new round for the debate
            start_btn = gr.Button("Start New Round")
            start_btn.click(start_new_round, [], [chatbot])

            judge_btn = gr.Button("Judge Debate")
            judge_btn.click(evaluate_debate, None, [chatbot])


demo.launch()

# You argue that the ending of Inception is real. 
# You argue that the ending of Inception is a dream. 