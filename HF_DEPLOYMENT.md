# Deploying QUS-AI v2 to Hugging Face Spaces

These instructions assume you have a Hugging Face account and a created Space.

## 1. Prepare Files
Ensure your local folder contains the following structure ready for upload. You do *not* need to upload the entire legacy history, just the new architecture.

**Files to Upload:**
- `qusai_core/` (The entire folder)
- `qusai_app.py`
- `requirements.txt`
- `quran_root_ontology_v3.ttl` (Must be in root or path updated in constants.py)
- `quranic_grammar_rules.json` (Must be in root or path updated in constants.py)

## 2. Configure the Space (`README.md`)
Hugging Face Spaces use the `README.md` YAML header to configure the environment. Create or edit the `README.md` in your Space with the following:

```yaml
---
title: QUSAI Mizan v2
emoji: 🕌
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.9.1
app_file: qusai_app.py
pinned: true
python_version: 3.10
license: mit
---

# QUSAI Mizan v2 - Modular Architecture

Quranic Ontological Syntax Architectural Intelligence.
Powered by the `qusai_core` alignment middleware.
```

**Crucial Change:** Note the line `app_file: qusai_app.py`. This tells Hugging Face to run the new modular entry point instead of the default `app.py`.

## 3. Environment Variables (Optional)
If you are using a gated model (like Llama 3) or need higher rate limits:
1. Go to your Space **Settings**.
2. Scroll to **Variables and secrets**.
3. Add `HF_TOKEN` with your write-access token.
   * *Note: The default model `Qwen/Qwen2.5-3B-Instruct` in the code is non-gated and does not strictly require a token, but it is recommended.*

## 4. Hardware Selection
- **CPU Basic (Free)**: The current configuration uses `device_map="cpu"` and `low_cpu_mem_usage=True`. It will run on the free tier, though generation might be slow.
- **T4 Small (GPU)**: If you upgrade the Space hardware, the `llm/loader.py` script is written to use `device_map="auto"`, so it will automatically utilize the GPU.

## 5. Troubleshooting
If the Space fails to build:
1. **Check Paths**: Ensure `quran_root_ontology_v3.ttl` is exactly where `qusai_core/utils/constants.py` expects it (default is the root directory).
2. **Check Logs**: Click the "Logs" tab in the Space.
3. **Memory**: If it crashes with "OOM" (Out of Memory), switch to a smaller model in `qusai_app.py` (e.g., `Qwen/Qwen2.5-1.5B-Instruct`) or upgrade the hardware.
