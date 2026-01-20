import logging
import gradio as gr
from qusai_core.pipeline.middleware import QusaiMiddleware

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize Middleware
# We use lazy_load=True to allow the UI to start fast, 
# but effectively we'll load on the first request or we can trigger load in a separate thread.
# For simplicity in this demo, we load immediately.
middleware = QusaiMiddleware(model_id="Qwen/Qwen2.5-3B-Instruct", lazy_load=False)

def chat_interface(message, history):
    return middleware.process_query(message)

# Gradio UI
with gr.Blocks(title="QUSAI v2 (Modular)") as demo:
    gr.Markdown("# 🕌 QUSAI v2 - Quranic Ontological Alignment")
    gr.Markdown(f"**Status:** Core v3 Ontology Loaded | Model: Qwen 2.5 3B")
    
    chatbot = gr.ChatInterface(
        fn=chat_interface,
        type="messages"
    )

if __name__ == "__main__":
    print("Starting QUSAI v2...")
    demo.launch()
