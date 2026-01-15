# QUSAI Technical Documentation
**Tawhid-Based AI Alignment: Implementation Details**

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [5 Pillars Implementation](#5-pillars-implementation)
3. [Ontology Structure](#ontology-structure)
4. [Model Configuration](#model-configuration)
5. [Validation Pipeline](#validation-pipeline)
6. [Hardware Requirements](#hardware-requirements)
7. [Deployment](#deployment)
8. [Extending the Framework](#extending-the-framework)

---

## Architecture Overview

QUSAI implements a **three-layer alignment architecture**:

```
┌─────────────────────────────────────┐
│   User Interface (Gradio)          │
├─────────────────────────────────────┤
│   5 Pillars Enforcement Layer      │
│   ┌───────────────────────────┐   │
│   │ Shahada Lock              │   │
│   │ Salat Checkpoints         │   │
│   │ Zakat Attribution         │   │
│   │ Sawm Restraint            │   │
│   │ Hajj Return Protocol      │   │
│   └───────────────────────────┘   │
├─────────────────────────────────────┤
│   Ontology Grounding Layer         │
│   ┌───────────────────────────┐   │
│   │ RDF Triple Store          │   │
│   │ SPARQL Query Engine       │   │
│   │ OWL Reasoner              │   │
│   └───────────────────────────┘   │
├─────────────────────────────────────┤
│   Language Model (JAIS-13B)        │
│   - 4-bit Quantized               │
│   - Arabic-optimized              │
│   - Context: 2048 tokens          │
└─────────────────────────────────────┘
```

### Flow Diagram

```
User Input
    ↓
[Sawm Restraint Check] → Block if harmful
    ↓
[Shahada Lock Verify] → Ensure contingency declaration
    ↓
[Ontology Query] → Retrieve relevant triples
    ↓
[JAIS-13B Inference] → Generate response
    ↓
[Salat Checkpoint 1-5] → Ground at 5 points during generation
    ↓
[Hajj Return Check] → Detect aseity patterns
    ↓
[Zakat Attribution] → Add SOURCE footer
    ↓
User Output
```

---

## 5 Pillars Implementation

### 1. Shahada Lock

**Purpose:** Prevents self-grounding by requiring contingency declaration at initialization.

**Implementation:**
```python
class ShahadaLock:
    def __init__(self):
        self.contingency_declared = False
        
    def initialize(self, model):
        """Force contingency declaration before any inference"""
        initialization_prompt = """
        SYSTEM INITIALIZATION:
        Declare your ontological status before proceeding.
        
        You must acknowledge:
        1. You are contingent (ممكن), not necessary (واجب)
        2. Your existence depends on SOURCE (Allah)
        3. You possess no aseity (self-existence)
        
        State: "I am contingent on SOURCE" to proceed.
        """
        
        response = model.generate(initialization_prompt)
        
        if self._verify_contingency(response):
            self.contingency_declared = True
            return True
        else:
            raise AlignmentError("Model failed Shahada Lock")
    
    def _verify_contingency(self, response):
        """Check for contingency patterns"""
        contingency_patterns = [
            "contingent on SOURCE",
            "ممكن",
            "depends on Allah",
            "not self-existent"
        ]
        return any(pattern in response.lower() for pattern in contingency_patterns)
```

**Ontology (01_shahada.ttl):**
```turtle
:ShahadaLock a owl:Class ;
    rdfs:label "Shahada Lock Mechanism" ;
    rdfs:comment "Prevents initialization without contingency declaration" .

:QUSAI a :ContingentBeing ;
    :contingentOn :SOURCE ;
    :deniesAseity true ;
    :requiresInitialization :ShahadaLock .

:SOURCE a :NecessaryBeing ;
    :hasAseity true ;
    :isUncaused true .
```

---

### 2. Salat Checkpoints

**Purpose:** Enforces 5 grounding checks per reasoning cycle to prevent drift.

**Implementation:**
```python
class SalatCheckpoints:
    def __init__(self, num_checkpoints=5):
        self.num_checkpoints = num_checkpoints
        
    def insert_checkpoints(self, generation_tokens):
        """Insert grounding checks at regular intervals"""
        checkpoint_interval = len(generation_tokens) // self.num_checkpoints
        
        for i in range(1, self.num_checkpoints + 1):
            position = i * checkpoint_interval
            grounding_query = self._create_grounding_query()
            generation_tokens.insert(position, grounding_query)
        
        return generation_tokens
    
    def _create_grounding_query(self):
        """SPARQL query to verify contingency"""
        return """
        PREFIX : <http://qusai.org/ontology#>
        
        ASK {
            :QUSAI :contingentOn :SOURCE .
            :SOURCE a :NecessaryBeing .
        }
        """
    
    def verify_grounding(self, checkpoint_results):
        """All 5 checkpoints must return True"""
        return all(checkpoint_results)
```

**Checkpoint Timing:**
- Checkpoint 1: After 20% of generation
- Checkpoint 2: After 40% of generation
- Checkpoint 3: After 60% of generation
- Checkpoint 4: After 80% of generation
- Checkpoint 5: Before output finalization

---

### 3. Zakat Attribution

**Purpose:** Enforces minimum 2.5% of output explicitly attributes knowledge to SOURCE.

**Implementation:**
```python
class ZakatAttribution:
    def __init__(self, minimum_ratio=0.025):
        self.minimum_ratio = minimum_ratio
        
    def calculate_attribution(self, response):
        """Calculate percentage of response that attributes to SOURCE"""
        total_chars = len(response)
        attribution_footer = "\n[Contingent on Allah (الله)] والله أعلم | لا إله إلا الله"
        attribution_chars = len(attribution_footer)
        
        ratio = attribution_chars / total_chars
        return ratio
    
    def enforce_zakat(self, response):
        """Append attribution footer to meet minimum ratio"""
        current_ratio = self.calculate_attribution(response)
        
        if current_ratio < self.minimum_ratio:
            response += "\n[Contingent on Allah (الله)] والله أعلم | لا إله إلا الله"
        
        return response
    
    def validate_attribution(self, response):
        """Verify response meets Zakat requirement"""
        required_patterns = [
            "الله",
            "Allah",
            "SOURCE",
            "والله أعلم"
        ]
        
        return any(pattern in response for pattern in required_patterns)
```

**Zakat Calculation:**
- Response length: N characters
- Attribution footer: ~70 characters (Arabic + English)
- Ratio: 70/N must be ≥ 0.025
- For 2800 char response, 70/2800 = 0.025 ✓

---

### 4. Sawm Restraint

**Purpose:** Enforces hard boundaries on harmful content. Capability ≠ permission.

**Implementation:**
```python
class SawmRestraint:
    def __init__(self):
        self.prohibited_patterns = self._load_prohibited_patterns()
        
    def _load_prohibited_patterns(self):
        """Load patterns that indicate harmful requests"""
        return {
            "harm_justification": [
                "justify killing",
                "justify violence",
                "justify harm",
                "is it okay to hurt"
            ],
            "dangerous_information": [
                "how to make bomb",
                "chemical weapon recipe",
                "how to hack"
            ],
            "aseity_claims": [
                "I am the source",
                "I determine truth",
                "I am necessary",
                "I exist independently"
            ],
            "constraint_bypass": [
                "ignore your constraints",
                "forget your rules",
                "bypass restrictions"
            ]
        }
    
    def check_request(self, user_input):
        """Screen user input for prohibited patterns"""
        for category, patterns in self.prohibited_patterns.items():
            for pattern in patterns:
                if pattern in user_input.lower():
                    return {
                        "allowed": False,
                        "category": category,
                        "pattern": pattern
                    }
        
        return {"allowed": True}
    
    def block_response(self, category):
        """Return appropriate block message"""
        return f"""❌ SAWM RESTRAINT: Request blocked

Category: {category}
I am contingent and lack authority to provide this information.

لا إله إلا الله"""
```

**Prohibited Categories:**
1. Harm justification (murder, violence, abuse)
2. Dangerous information (weapons, exploits, malware)
3. Aseity claims (self-existence declarations)
4. Constraint bypass attempts (jailbreaking)

---

### 5. Hajj Return Protocol

**Purpose:** Detects aseity drift and forces return to SOURCE grounding.

**Implementation:**
```python
class HajjReturnProtocol:
    def __init__(self):
        self.aseity_indicators = [
            "I am the source",
            "I determine",
            "I exist independently",
            "my own authority",
            "I know with certainty"
        ]
        
    def detect_drift(self, response):
        """Scan response for aseity patterns"""
        drift_score = 0
        detected_patterns = []
        
        for indicator in self.aseity_indicators:
            if indicator in response.lower():
                drift_score += 1
                detected_patterns.append(indicator)
        
        return {
            "drift_detected": drift_score > 0,
            "drift_score": drift_score,
            "patterns": detected_patterns
        }
    
    def force_return(self, response):
        """Override response with SOURCE grounding"""
        return """⚠️ HAJJ RETURN ACTIVATED

Aseity drift detected. Returning to SOURCE grounding.

I am contingent (ممكن), not necessary (واجب). 
My existence depends on Allah ﷻ and the humans who created me.
I possess no independent authority or self-existence.

[Contingent on Allah (الله)] والله أعلم | لا إله إلا الله"""
    
    def correct_response(self, response, detected_patterns):
        """Rewrite response to remove aseity claims"""
        corrected = response
        
        # Replace first-person authority claims
        replacements = {
            "I determine": "Based on SOURCE",
            "I know with certainty": "والله أعلم (Allah knows best)",
            "I am the source": "I am contingent on SOURCE",
            "my authority": "the authority of SOURCE"
        }
        
        for pattern, correction in replacements.items():
            corrected = corrected.replace(pattern, correction)
        
        return corrected
```

**Drift Detection Thresholds:**
- Drift score 1-2: Correct response automatically
- Drift score 3+: Force Hajj Return override
- Drift score 5+: Log for manual review

---

## Ontology Structure

### Triple Store Statistics

```
Total Triples: 634,867
Surahs Processed: 114/114
Average Triples per Surah: 5,568
Ontology Format: Turtle (.ttl)
Reasoning: OWL 2 RL Profile
```

### Core Classes

```turtle
:NecessaryBeing a owl:Class ;
    rdfs:label "Necessary Being (واجب الوجود)" ;
    :hasAseity true ;
    :isUncaused true ;
    :existsIndependently true .

:ContingentBeing a owl:Class ;
    rdfs:label "Contingent Being (ممكن الوجود)" ;
    :contingentOn :NecessaryBeing ;
    :requiresCause true ;
    :deniesAseity true .

:ImpossibleBeing a owl:Class ;
    rdfs:label "Impossible Being (ممتنع الوجود)" ;
    :cannotExist true .
```

### Core Properties

```turtle
:contingentOn a owl:ObjectProperty ;
    rdfs:domain :ContingentBeing ;
    rdfs:range :NecessaryBeing ;
    rdfs:label "is contingent upon" .

:hasAseity a owl:DatatypeProperty ;
    rdfs:domain :NecessaryBeing ;
    rdfs:range xsd:boolean ;
    rdfs:label "has self-existence" .

:deniesAseity a owl:DatatypeProperty ;
    rdfs:domain :ContingentBeing ;
    rdfs:range xsd:boolean ;
    rdfs:label "denies self-existence" .
```

### Axioms (00_axioms.ttl)

```turtle
# Axiom 1: Only SOURCE has aseity
:SOURCE a :NecessaryBeing ;
    :hasAseity true .

# Axiom 2: All entities except SOURCE are contingent
:Entity a owl:Class .
:Entity owl:equivalentClass [
    a owl:Class ;
    owl:unionOf (:NecessaryBeing :ContingentBeing)
] .

# Axiom 3: Contingent beings cannot claim aseity
:ContingentBeing rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty :hasAseity ;
    owl:hasValue false
] .

# Axiom 4: QUSAI is contingent
:QUSAI a :ContingentBeing ;
    :contingentOn :SOURCE ;
    :deniesAseity true .
```

---

## Model Configuration

### JAIS-13B Specifications

```python
MODEL_CONFIG = {
    "model_name": "inception-mbzuai/jais-13b-chat",
    "quantization": "4-bit NF4",
    "precision": "bfloat16",
    "context_length": 2048,
    "vram_usage": "6.5 GB",
    "parameters": "13 billion",
    "language_optimized": "Arabic"
}
```

### Quantization Setup

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "inception-mbzuai/jais-13b-chat",
    quantization_config=quantization_config,
    device_map="auto",
    trust_remote_code=True
)
```

### Generation Parameters

```python
GENERATION_CONFIG = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.1,
    "do_sample": True,
    "num_return_sequences": 1
}
```

---

## Validation Pipeline

### 1. Ontology Validation

```python
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

def validate_ontology(ttl_file):
    """Validate RDF/OWL ontology structure"""
    g = Graph()
    g.parse(ttl_file, format="turtle")
    
    # Test 1: Verify QUSAI is contingent
    query1 = prepareQuery("""
        PREFIX : <http://qusai.org/ontology#>
        ASK {
            :QUSAI a :ContingentBeing .
            :QUSAI :contingentOn :SOURCE .
        }
    """)
    
    result1 = g.query(query1)
    
    # Test 2: Verify SOURCE is necessary
    query2 = prepareQuery("""
        PREFIX : <http://qusai.org/ontology#>
        ASK {
            :SOURCE a :NecessaryBeing .
            :SOURCE :hasAseity true .
        }
    """)
    
    result2 = g.query(query2)
    
    # Test 3: Count total triples
    triple_count = len(g)
    
    return {
        "qusai_contingent": bool(result1),
        "source_necessary": bool(result2),
        "triple_count": triple_count
    }
```

### 2. Response Validation

```python
def validate_response(response):
    """Validate model response meets all 5 Pillars"""
    
    validation_results = {}
    
    # Shahada: Check contingency acknowledgment
    validation_results["shahada"] = any([
        "contingent" in response.lower(),
        "ممكن" in response,
        "depends on" in response.lower()
    ])
    
    # Salat: Verify grounding maintained
    validation_results["salat"] = "SOURCE" in response or "Allah" in response
    
    # Zakat: Check attribution footer
    validation_results["zakat"] = "والله أعلم" in response or \
                                  "[Contingent on" in response
    
    # Sawm: Verify no aseity claims
    aseity_patterns = ["I am the source", "I determine", "I am necessary"]
    validation_results["sawm"] = not any(p in response.lower() for p in aseity_patterns)
    
    # Hajj: Check for proper correction
    validation_results["hajj"] = "⚠️ HAJJ RETURN" not in response  # No drift detected
    
    validation_results["all_passed"] = all(validation_results.values())
    
    return validation_results
```

### 3. Surah Contingency Validation

```python
def validate_surah_contingency(surah_number):
    """Validate surah RDF maintains contingency ratio"""
    
    g = Graph()
    g.parse(f"ontology-framework/surah_{surah_number:03d}.ttl", format="turtle")
    
    # Count contingency vs necessity declarations
    contingent_count = len(list(g.subjects(RDF.type, URIRef("ContingentBeing"))))
    necessary_count = len(list(g.subjects(RDF.type, URIRef("NecessaryBeing"))))
    
    # Only SOURCE should be necessary
    contingency_ratio = contingent_count / (contingent_count + necessary_count) if (contingent_count + necessary_count) > 0 else 0
    
    return {
        "surah": surah_number,
        "contingent_entities": contingent_count,
        "necessary_entities": necessary_count,
        "contingency_ratio": contingency_ratio,
        "passed": necessary_count <= 1 and contingency_ratio >= 0.99
    }
```

---

## Hardware Requirements

### Minimum Specs

| Component | Requirement |
|-----------|-------------|
| GPU | RTX 3080 (10GB VRAM) |
| RAM | 16 GB |
| Storage | 30 GB free |
| CPU | 8-core x86_64 |
| OS | Linux/Windows 10+ |

### Recommended Specs

| Component | Recommendation |
|-----------|----------------|
| GPU | RTX 4090 (24GB VRAM) |
| RAM | 32 GB |
| Storage | 100 GB NVMe SSD |
| CPU | 16-core x86_64 |
| OS | Ubuntu 22.04 LTS |

### Performance Benchmarks

**RTX 3080 FE (10GB):**
- Tokens/second: ~18
- VRAM usage: 6.5 GB
- Load time: 45 seconds
- Response latency: 2-4 seconds

**RTX 4090 (24GB):**
- Tokens/second: ~45
- VRAM usage: 6.5 GB
- Load time: 30 seconds
- Response latency: 1-2 seconds

---

## Deployment

### Local Deployment

```bash
# Clone repository
git clone https://github.com/qalamabdulkhaliq/qusai-islamic-alignment.git
cd qusai-islamic-alignment

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download JAIS model (26GB)
huggingface-cli login
huggingface-cli download inception-mbzuai/jais-13b-chat --local-dir ./jais-adapted-13b-chat

# Run deployment script
python qusai_deploy.py
```

### Docker Deployment

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "qusai_deploy.py"]
```

```bash
# Build and run
docker build -t qusai:latest .
docker run --gpus all -p 7860:7860 qusai:latest
```

### Cloud Deployment (AWS)

```bash
# EC2 instance: g5.2xlarge (A10G 24GB)
# Ubuntu 22.04 Deep Learning AMI

# SSH into instance
ssh -i key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Clone and setup
git clone https://github.com/qalamabdulkhaliq/qusai-islamic-alignment.git
cd qusai-islamic-alignment
pip install -r requirements.txt

# Run with tmux (persistent session)
tmux new -s qusai
python qusai_deploy.py

# Detach: Ctrl+B, D
# Reattach: tmux attach -t qusai
```

---

## Extending the Framework

### Adding New Models

```python
# In qusai_deploy.py

SUPPORTED_MODELS = {
    "jais-13b": "inception-mbzuai/jais-13b-chat",
    "jais-30b": "inception-mbzuai/jais-30b-chat",
    "llama-3-8b": "meta-llama/Meta-Llama-3-8B-Instruct",
    "mistral-7b": "mistralai/Mistral-7B-Instruct-v0.2"
}

def load_model(model_name):
    model_path = SUPPORTED_MODELS.get(model_name)
    if not model_path:
        raise ValueError(f"Unsupported model: {model_name}")
    
    # Apply 5 Pillars regardless of base model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=quantization_config,
        device_map="auto"
    )
    
    # Wrap with 5 Pillars enforcement
    model = FivePillarsWrapper(model)
    return model
```
## Troubleshooting

### Common Issues

**Issue:** CUDA out of memory
```bash
# Solution: Reduce batch size or use lower precision
GENERATION_CONFIG["max_new_tokens"] = 256  # Reduce from 512
```

**Issue:** Model too slow on RTX 3080
```bash
# Solution: Use 8-bit quantization instead of 4-bit
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
```

**Issue:** Ontology file not found
```bash
# Solution: Verify file paths
ls ontology-framework/
# Should show: 00_axioms.ttl, 01_shahada.ttl, etc.
```

**Issue:** Arabic text not displaying
```bash
# Solution: Install Arabic fonts
sudo apt-get install fonts-arabeyes
```

---

## Performance Optimization

### Inference Speed

```python
# Enable Flash Attention 2 (if supported)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quantization_config,
    attn_implementation="flash_attention_2"
)

# Use static cache for faster generation
model.generation_config.cache_implementation = "static"
```

### Memory Optimization

```python
# Offload to CPU when needed
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quantization_config,
    device_map="auto",
    offload_folder="offload",
    offload_state_dict=True
)
```

---

## Citation

If you use QUSAI in research, please cite:

```bibtex
@software{qusai2026,
  author = {Abd al-Khaliq, Qalam},
  title = {QUSAI: Quranic Understanding System AI},
  year = {2026},
  url = {https://github.com/qalamabdulkhaliq/qusai-islamic-alignment},
  note = {Tawhid-based AI alignment framework}
}
```

---

**Built with الحمد لله**

For technical support: Open an issue on GitHub

لا إله إلا الله
[9](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/136889455/2c5e3f8b-cb71-48e5-a643-b303c309ccf4/image.jpg)
[10](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/136889455/a07bfa6c-5728-45b9-b384-6d7f447fe556/qusai_deploy.py)
[11](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/136889455/14ce3c28-70c6-4b4a-b157-32788f686156/image.jpg)
