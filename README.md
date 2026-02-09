# 🧠 Recursive Medical Gemma Agent (R-MedLM)

A **recursive, tool-using clinical reasoning system** built around **Gemma LLMs** and structured medical data.

This project implements a **Recursive Language Model (RLM) architecture** for medical analysis, where the model:
- Writes executable Python code
- Uses structured medical tools
- Recursively calls itself for focused reasoning
- Operates inside a persistent REPL environment

The system is designed for **research in long-horizon medical reasoning** and **agentic LLM workflows**.

---

## 🏗️ Architecture Overview

User Query
↓
Root Model (Gemma via Ollama)
↓
Writes Python code
↓
REPL Environment
↓
Medical Tool Calls (labs, vitals, cohorts)
↓
Optional Recursive Sub-calls
↓
Final structured result

---

## 🚀 Features

✔ Recursive LLM reasoning  
✔ Persistent execution environment (REPL)  
✔ Modular medical tool layer  
✔ Cohort-based analysis  
✔ Local LLM inference using **Ollama + Gemma**  
✔ No cloud dependency required  

---

## 💻 System Requirements

- macOS (Apple Silicon recommended) or Linux
- Python **3.10+**
- Ollama installed locally
- At least **8GB RAM** recommended

---

## 🧠 Model Setup (Gemma)

This project runs **Gemma locally** using Ollama.

### 1️⃣ Install Ollama

```bash
brew install ollama
```

### Start the Ollama server:
```bash
ollama serve
```
### 2️⃣ Pull the Gemma Model
```bash
ollama pull gemma:2b-instruct
```
## 📦 Installation
Clone the repo and install dependencies:
```bash
git clone <your-repo-url>
cd medgemma

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
## ▶️ Running the System

Run the recursive medical agent:
```bash
python run_pipeline.py
```
You should see iterative reasoning steps like:
```bash
🔁 Iteration 1
🧠 Model generated code:
patients = cohort_tools.get_patients_with_diagnosis("A41")
...
Final = results
```

## 🗄️ Data Layer

The system currently uses DuckDB for local structured storage.

Future extensions may include:
	•	MIMIC-IV integration
	•	EHR pipelines
	•	Real-time streaming data

## 🧩 Project Structure

```code
medgemma/
│
├── rlm_core/        # Recursive controller + REPL
├── models/          # LLM interfaces (Ollama-based)
├── tools/           # Medical data tool functions
├── mimic_memory/    # Database and schema layer
├── prompts/         # System prompts for root & subcall models
├── config/          # Model and DB configs
└── run_pipeline.py  # Main entry point
```
## 🧪 Development Notes
This project is an experimental research system exploring:
	•	Recursive LLM inference
	•	Symbolic + neural hybrid reasoning
	•	Tool-based clinical analysis

Expect frequent updates and evolving APIs.
```
