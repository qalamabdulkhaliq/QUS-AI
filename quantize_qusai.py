import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# 4-bit config for RTX 3080
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

print("⚡ Loading JAIS-13B in 4-bit from LOCAL path...")

# YOUR LOCAL MODEL PATH
model = AutoModelForCausalLM.from_pretrained(
    "jais-adapted-13b-chat",  # This is the folder name you have
    quantization_config=quant_config,
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained("jais-adapted-13b-chat")

print(f"⚡ VRAM used: {torch.cuda.memory_allocated()/1e9:.2f}GB")
print("✓ JAIS-13B loaded and quantized!")

# Test it
prompt = "ما هو التوحيد؟"  # Arabic test
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=128)
print("\n" + tokenizer.decode(outputs[0], skip_special_tokens=True))
