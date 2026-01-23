import logging
import os
import gradio as gr
from qusai_core.pipeline.middleware import QusaiMiddleware

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Get Token from environment
hf_token = os.environ.get("HF_TOKEN")

# Global singleton
_middleware = None

# -----------------------------------------------------------------------------
# 1. LOAD ARTIFACTS
# -----------------------------------------------------------------------------
def load_whitepaper():
    try:
        with open("QUS_AI_Technical_Whitepaper.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "# Error: Whitepaper not found."

def load_proof(proof_name):
    path_map = {
        "Field Equation (Uniqueness of Source)": "_legacy_archive/docs/PROOFS.txt",
        "Equation of Return (Transmutation of Error)": "_legacy_archive/docs/Equation_of_Return.txt",
        "Calculus of Rahma (The Rectification of Error)": "_legacy_archive/docs/Calculus_of_Rahma.txt"
    }
    target_path = path_map.get(proof_name)
    if not target_path: return "⚠️ Unknown Artifact."
    try:
        with open(target_path, "r", encoding="utf-8") as f: return f.read()
    except FileNotFoundError: return f"⚠️ Artifact not found at {target_path}."

# -----------------------------------------------------------------------------
# 2. CORE LOGIC
# -----------------------------------------------------------------------------
def get_middleware():
    global _middleware
    if _middleware is None:
        logger.info("⚡ Lazy Initializing Middleware...")
        try:
            _middleware = QusaiMiddleware(
                model_id="Qwen/Qwen2.5-72B-Instruct",
                api_token=hf_token,
                lazy_load=False
            )
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise e
    return _middleware

def generate_response(message, history):
    try:
        mw = get_middleware()
        return mw.process_query(message)
    except Exception as e:
        logger.error(f"Runtime Error: {e}")
        return f"⚠️ System Error: {str(e)}"

def chat_wrapper(message, history, arabic_only):
    if arabic_only:
        message = f"{message} (Please answer strictly in Arabic / العربية)"
    return generate_response(message, history)

# -----------------------------------------------------------------------------
# 3. UI CONSTRUCTION
# -----------------------------------------------------------------------------
css = """
.prose { font-size: 1.1em; }
code { font-family: 'Consolas', 'Courier New', monospace; }
iframe { border: 1px solid #eee; border-radius: 8px; }
"""

with gr.Blocks(title="QUSAI v2 - Mizan (Pro)", css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🕌 QUSAI v2 - Quranic Ontological Alignment")
    gr.Markdown("**Status:** ✅ Model: Qwen 2.5 72B | ✅ Ontology: v3 Root Topology | ✅ Protocol: Mizan")

    with gr.Tabs():
        # TAB 1: THE WORKBENCH (Split View)
        with gr.Tab("💬 Interaction & Verification"):
            with gr.Row():
                # LEFT COLUMN: The AI (Gravity Well)
                with gr.Column(scale=2): 
                    gr.Markdown("### 🧠 The Reasoning Engine")
                    with gr.Row():
                        arabic_check = gr.Checkbox(label="Output in Arabic Only", value=False)
                    
                    # Manually define Chatbot to set height (Compat Fix)
                    custom_chatbot = gr.Chatbot(height=650, type="messages")
                    
                    chat_interface = gr.ChatInterface(
                        fn=chat_wrapper,
                        chatbot=custom_chatbot,
                        additional_inputs=[arabic_check],
                        type="messages",
                        examples=[
                            ["Define Justice (H-K-M)", False], 
                            ["Can an AI have a soul?", False], 
                            ["Explain Rizq mathematically", False]
                        ]
                    )

                # RIGHT COLUMN: The Source (Mushaf)
                with gr.Column(scale=1):
                    gr.Markdown("### 📖 The Reference (Mushaf)")
                    # Embed Quran.com (Defaults to Al-Fatiha, user can navigate)
                    gr.HTML(
                        '<iframe src="https://quran.com/1?reading=true" width="100%" height="700px" style="border:none;"></iframe>'
                    )
                    gr.Markdown("*Navigable Mushaf provided by Quran.com*")

        # TAB 2: MANIFEST
        with gr.Tab("📜 System Manifest"):
            gr.Markdown("### Technical Whitepaper: The Gravity Well Architecture")
            whitepaper_display = gr.Markdown(load_whitepaper())
            gr.Button("Refresh Document").click(load_whitepaper, outputs=whitepaper_display)

        # TAB 3: MATH
        with gr.Tab("📐 Theological Mathematics"):
            gr.Markdown("### The Calculus of Tawhid")
            with gr.Row():
                proof_selector = gr.Dropdown(
                    choices=[
                        "Field Equation (Uniqueness of Source)", 
                        "Equation of Return (Transmutation of Error)",
                        "Calculus of Rahma (The Rectification of Error)"
                    ],
                    label="Select Artifact",
                    value="Calculus of Rahma (The Rectification of Error)"
                )
                load_proof_btn = gr.Button("📂 Load Artifact")
            proof_display = gr.Code(label="Artifact Content", language="markdown", lines=20)
            load_proof_btn.click(load_proof, inputs=proof_selector, outputs=proof_display)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)