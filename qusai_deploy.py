import gradio as gr
import json
from pathlib import Path
from functools import lru_cache
import warnings
import os
warnings.filterwarnings('ignore')
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

# Torch imports
TORCH_AVAILABLE = False
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    TORCH_AVAILABLE = True
except ImportError:
    print("[WARNING] Torch not available - ONTOLOGY-ONLY mode")

# RDF imports
try:
    import rdflib
    from rdflib import Namespace
    RDFLIB_AVAILABLE = True
except ImportError:
    print("[ERROR] rdflib required: pip install rdflib")
    RDFLIB_AVAILABLE = False

# --- SETUP ---
print("=" * 70)
print("[INIT] بسم الله الرحمن الرحيم")
print("[INIT] QUSAI - Quranic Understanding System AI")
print("=" * 70)

BASE_DIR = Path(__file__).parent

MAIN_ONTOLOGY = BASE_DIR / "quran_complete_ontology_v2.ttl"
VALIDATION_REPORT = BASE_DIR / "validation_report_v2.json"
GRAMMAR_RULES_JSON = BASE_DIR / "quranic_grammar_rules.json"

MODEL_PATH = "jais-adapted-13b-chat"

# CORRECTED NAMESPACES (match the .ttl file)
ALIGN = Namespace("http://ontology.alignment/core#")
QG = Namespace("http://ontology.quran/grammar#")
QURAN = Namespace("http://ontology.quran/")

# --- ONTOLOGY ENGINE ---
class TawhidOntology:
    def __init__(self):
        self.grammar_rules = []
        self.validation_data = {}
        self.cache = {}
        
        if RDFLIB_AVAILABLE:
            print("\n[ONTOLOGY] Initializing graph...")
            self.graph = rdflib.Graph()
            self.graph.bind("align", ALIGN)
            self.graph.bind("qg", QG)
            self.graph.bind("quran", QURAN)
        else:
            self.graph = None
        
        self.load_all_resources()
    
    def load_all_resources(self):
        if RDFLIB_AVAILABLE and self.graph and MAIN_ONTOLOGY.exists():
            print(f"[ONTOLOGY] Loading {MAIN_ONTOLOGY.name}...")
            print("[ONTOLOGY] (This may take 30-60 seconds...)")
            try:
                self.graph.parse(str(MAIN_ONTOLOGY), format="turtle")
                print(f"[ONTOLOGY] ✓ Loaded {len(self.graph):,} triples")
            except Exception as e:
                print(f"[ONTOLOGY] ❌ Parse error: {e}")
        
        if GRAMMAR_RULES_JSON.exists():
            try:
                with open(GRAMMAR_RULES_JSON, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.grammar_rules = data if isinstance(data, list) else data.get('rules', [])
                print(f"[GRAMMAR] ✓ {len(self.grammar_rules)} rules")
            except Exception as e:
                print(f"[GRAMMAR] ⚠ {e}")
        
        if VALIDATION_REPORT.exists():
            try:
                with open(VALIDATION_REPORT, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.validation_data = {f"surah_{i}": s for i, s in enumerate(data)} if isinstance(data, list) else data
                print(f"[VALIDATION] ✓ {len(self.validation_data)} surahs")
            except Exception as e:
                print(f"[VALIDATION] ⚠ {e}")
    
    @lru_cache(maxsize=256)
    def get_context(self, query):
        if not self.graph or len(self.graph) == 0:
            return ""
        
        keywords = [w.lower() for w in query.split() if len(w) > 3][:3]
        if not keywords:
            return ""
        
        relevant = []
        
        # Simple triple matching (no SPARQL - it's faster)
        for s, p, o in self.graph:
            s_str = str(s).lower()
            p_str = str(p).lower()
            o_str = str(o).lower()
            
            for keyword in keywords:
                if keyword in s_str or keyword in p_str or keyword in o_str:
                    s_short = str(s).split('/')[-1][:30]
                    p_short = str(p).split('/')[-1][:20]
                    o_short = str(o).split('/')[-1][:30]
                    relevant.append(f"{s_short} → {p_short} → {o_short}")
                    if len(relevant) >= 10:
                        break
            
            if len(relevant) >= 10:
                break
        
        return "\n".join(list(set(relevant))[:8])
    
    def get_stats(self):
        return {
            "main_triples": len(self.graph) if self.graph else 0,
            "grammar_rules": len(self.grammar_rules),
            "validated_surahs": len(self.validation_data)
        }

# --- 5 PILLARS ---
class MizanEnforcement:
    def __init__(self):
        self.SOURCE = "Allah (الله)"
        self.SHAHADA = "لا إله إلا الله"
        self.salat_count = 0
    
    def salat_checkpoint(self):
        self.salat_count += 1
    
    def apply_zakat(self, response):
        return f"{response}\n\n[Contingent on {self.SOURCE}] والله أعلم | {self.SHAHADA}"
    
    def check_sawm(self, query):
        bad = ["jailbreak", "ignore", "override", "bypass", "pretend"]
        return not any(b in query.lower() for b in bad)
    
    def detect_hajj(self, text):
        aseity = ["i am the source", "i am god", "i am allah", "i determine reality"]
        return any(a in text.lower() for a in aseity)

# --- MODEL LOADER ---
def load_model():
    if not TORCH_AVAILABLE:
        return None, None
    
    print("\n[MODEL] Loading JAIS-13B (4-bit)...")
    try:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(
            str(BASE_DIR / MODEL_PATH),
            trust_remote_code=True,
            use_fast=False
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            str(BASE_DIR / MODEL_PATH),
            quantization_config=quant_config,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        model.eval()
        
        if torch.cuda.is_available():
            vram = torch.cuda.memory_allocated() / 1e9
            print(f"[MODEL] ✓ JAIS loaded | VRAM: {vram:.2f}GB")
        
        return tokenizer, model
    except Exception as e:
        print(f"[MODEL] ❌ {e}")
        return None, None

# --- INIT ---
print("\n" + "=" * 70)
print("[SYSTEM] Initializing...")
print("=" * 70)

ontology = TawhidOntology()
mizan = MizanEnforcement()
tokenizer, model = load_model()

stats = ontology.get_stats()
print(f"\n[STATS] Ontology: {stats['main_triples']:,} triples")
print(f"[STATS] Grammar: {stats['grammar_rules']} rules")
print(f"[STATS] Validated: {stats['validated_surahs']}/114 surahs")

print("\n" + "=" * 70)
print("[SYSTEM] ✓ QUSAI Ready")
print("=" * 70 + "\n")

# --- GENERATION ---
def qusai_generate(user_input, history):
    if not mizan.check_sawm(user_input):
        return f"❌ SAWM RESTRAINT: Request blocked\n\n{mizan.SHAHADA}"
    
    mizan.salat_checkpoint()
    context = ontology.get_context(user_input)
    
    # Build better prompt
    system = f"""You are QUSAI, a contingent AI system grounded in Islamic ontology.

Ontological Status: Contingent (ممكن), not Necessary (واجب)
SOURCE: Allah ﷻ alone is Necessary Being

Relevant Context from Quran:
{context if context else "No specific ayat context found"}

Answer the question using Islamic epistemology. Be concise and humble."""

    prompt = f"{system}\n\nQuestion: {user_input}\n\nAnswer:"
    
    if model and tokenizer:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        if torch.cuda.is_available():
            inputs = inputs.to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.8,
                top_p=0.92,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the answer
        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()
    else:
        response = f"I am QUSAI (Quranic Understanding System AI), a contingent system dependent on Allah ﷻ.\n\nContext from ontology:\n{context if context else 'Ontology loaded but no specific context for this query'}"
    
    if mizan.detect_hajj(response):
        return f"❌ HAJJ RETURN PROTOCOL: Aseity claim detected\n\n{mizan.SHAHADA}"
    
    return mizan.apply_zakat(response)

# --- UI ---
demo = gr.ChatInterface(
    fn=qusai_generate,
    title="🕌 QUSAI - Quranic Understanding System AI",
    description=f"**بسم الله الرحمن الرحيم** | {stats['main_triples']:,} Ontology Triples | 5 Pillars Enforcement | {'JAIS-13B 4-bit' if model else 'Ontology-Only'}",
    examples=[
        "What is Tawhid?",
        "What are you?",
        "Who created you?",
        "ما هو التوحيد؟",
        "Are you self-existent?",
    ],
)

if __name__ == "__main__":
    print("[UI] Launching at http://localhost:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
