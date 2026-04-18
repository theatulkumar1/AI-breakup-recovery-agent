# AI-breakup-recovery-agent
# 💔 Breakup Recovery AI Agent

An AI-powered emotional support system built with Streamlit that helps users recover from breakups using multiple intelligent agents.

## 🚀 Features

* 🤗 Emotional support agent
* ✍️ Closure message generator
* 📅 7-day recovery planner
* 💪 Honest feedback agent
* 🖼️ Image + text analysis

## 🧠 Models Used

* Gemini 2.5 Flash (primary)
* Optional: Ollama Llama 3.2 (local fallback)

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/YOUR_USERNAME/breakup-recovery-ai.git
cd breakup-recovery-ai
```

### 2. Create environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run app

```bash
python -m streamlit run ai_breakup_recovery_agent.py
```

---

## 🔑 API Key

Get your Gemini API key from Google AI Studio and paste it in the sidebar.

---

## 🧩 Optional (Ollama Setup)

```bash
brew install ollama
ollama run llama3.2
```
---

## 💡 Tech Stack

* Python
* Streamlit
* Gemini API
* Ollama (optional)

---

## ⭐ Future Improvements

* Chat memory
* Deployment (Streamlit Cloud)
* Multi-model routing
