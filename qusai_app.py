import logging
import gradio as gr
from qusai_core.pipeline.middleware import QusaiMiddleware

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Initialize Middleware with a solid 7B/8B GGUF Model
# "qwen2.5-7b-instruct-q4_k_m.gguf" is ~4.5GB. Perfect for 16GB RAM.
middleware = QusaiMiddleware(
    repo_id="Qwen/Qwen2.5-7B-Instruct-GGUF",
    filename="qwen2.5-7b-instruct-q4_k_m.gguf",
    lazy_load=False
)

def chat_interface(message, history, arabic_only):
    if arabic_only:
        message = f"{message} (Please answer strictly in Arabic / العربية)"
    return middleware.process_query(message)

# Gradio UI
with gr.Blocks(title="QUSAI v2 - Mizan") as demo:
    gr.Markdown("# 🕌 QUSAI v2 - Quranic Ontological Alignment")
    gr.Markdown("""
    **System Status:**
    - ✅ **Model**: Qwen 2.5 7B (GGUF/CPU Optimized)
    - ✅ **Ontology**: v3 Root Topology (Active)
    - ✅ **Bridge**: Universal Concept Map (Active)
    """)
    
    with gr.Row():
        arabic_check = gr.Checkbox(label="Output in Arabic Only (مخرجات عربية فقط)", value=False)
    
    chatbot = gr.ChatInterface(
        fn=chat_interface,
        additional_inputs=[arabic_check],
        type="messages"
    )

if __name__ == "__main__":
    demo.launch()