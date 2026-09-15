# 🎓 Babson CourseWork — AI & Machine Learning

Hi! I'm **Laura Rodriguez**, a student at Babson College. This repository holds my classwork and in-class activities for my AI course — from first LLM API calls to building retrieval-augmented generation (RAG) pipelines with LlamaIndex and Google Gemini.

## 👩‍💻 About Me

I'm passionate about the intersection of business and technology, and I'm building hands-on experience applying AI tools to real problems. This repo documents that journey, one class session at a time.

## 🛠️ Skills & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

**Also working with:** LlamaIndex · LlamaParse · Google Gemini API · OpenAI API · python-dotenv

## 📁 Directory Structure

```
CourseWork/
├── 1 Session/            # Session 1 — first LLM API calls
├── 2 Session/            # Session 2 — Python concepts & notebooks
├── 3-Session/            # Session 3 — LlamaIndex RAG: parsing, indexing, retrieval
├── Generated Documents/  # Output files produced by class scripts
├── .gitignore            # Keeps secrets (.env) and the venv out of git
└── README.md
```

Each session folder contains the scripts and notebooks for that class meeting, numbered to match the course materials (e.g. `03-...` files belong to Session 3).

## 🚀 Install Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/laurarodriguezo13/CourseWork.git
   cd CourseWork
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install llama-cloud-services llama-index-llms-openai \
       llama-index-llms-google-genai llama-index-embeddings-google-genai \
       llama-index-indices-managed-llama-cloud python-dotenv
   ```

3. **Add your API keys** — create a `.env` file (never committed, see `.gitignore`) inside the session folder you're running:
   ```
   LLAMA_CLOUD_API_KEY="llx-..."
   ORGANIZATION_ID="..."
   GEMINI_API_KEY="..."
   ```

4. **Run a script**
   ```bash
   python "3-Session/03-demo_llama_retrieval.py"
   ```

## 🤝 Contact / Connect

- 💼 [LinkedIn](https://www.linkedin.com/in/laura-rodriguez-ortega)
