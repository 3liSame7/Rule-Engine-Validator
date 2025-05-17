

https://github.com/user-attachments/assets/2da278d8-5c65-4a78-9b4b-ffbd4d931a08

**📄🧠✅ Document Rule Validator**

An end-to-end AI-powered application for validating business documents against natural language rules using LLMs.

**🚀 Live Demo**

Frontend (Streamlit): [\[your-streamlit-url\]  ](https://3lysame7-rule-engine-validator.streamlit.app/)
 Backend (FastAPI on Render): [https://rule-engine-validator.onrender.com](https://rule-engine-validator.onrender.com)

---

**What It Does**

1. Document Extraction  
    Upload a PDF/image and extract fields like totals and dates via OCR and LLM (Groq-hosted LLaMA 3).

2. Rule Parsing  
    Write a rule in plain English (e.g., "Total must be more than $1000") and convert it into structured JSON logic.

3. Validation  
    Check if the extracted document data meets the structured rules and return a pass/fail summary.

---

**Project Structure**

rag-validator/  
 │  
 ├── .env \-\> Secret API key (excluded from repo)  
 ├── docker-compose.yml \-\> Compose file for local dev  
 │  
 ├── rule\_engine/ \-\> FastAPI backend  
 │ ├── doc\_extractor.py \-\> Extract fields from text using LLM  
 │ ├── llm\_parser.py \-\> Convert rule text to JSON using LLM  
 │ ├── logic.py \-\> Core logic for validation  
 │ ├── main.py \-\> FastAPI endpoints  
 │ ├── schemas.py \-\> Pydantic data models  
 │ ├── Dockerfile \-\> Backend Docker image  
 │ └── requirements.txt  
 │  
 ├── ui/ \-\> Streamlit UI frontend  
 │ ├── app.py \-\> Main navigation controller  
 │ ├── document\_extractor.py \-\> Document extraction UI page  
 │ ├── rule\_parser.py \-\> Rule parsing UI page  
 │ ├── validator.py \-\> Validation UI page  
 │ ├── Dockerfile \-\> UI Docker image (for local)  
 │ └── requirements.txt  
 │  
 └── README.md \-\> This file

---

**Technologies Used**

| Component | Stack |
| ----- | ----- |
| LLM | Groq API (LLaMA 3\) |
| OCR/PDF | Tesseract, PyMuPDF |
| API Backend | FastAPI |
| Frontend UI | Streamlit |
| Containerized | Docker & Docker Compose |
| Hosting | Render (Backend), Streamlit (Frontend) |

---

**How to Use the App**

1. Go to the "Document Extractor" tab  
    Upload a PDF or image (with invoice/contract/etc.)  
    Extracted fields will be saved automatically.

2. Go to the "Rule Parser" tab  
    Write a business rule in plain English  
    Parsed rule is converted to JSON and saved.

3. Go to the "Validator" tab  
    Extracted fields and parsed rules auto-fill  
    Press Validate to check compliance  
    See accumulated summary of passed/failed validations.

4. Use the Clear button to reset the summary.

---

**Sample Inputs**

Example Rule:  
 The invoice\_total must be greater than $1000

Parsed Rule:  
 {  
 "field": "invoice\_total",  
 "operator": "\>",  
 "value": 1000  
 }

---

**Running Locally (Optional)**

1. Clone the Repository

git clone [https://github.com/3liSame7/Rule-Engine-Validator.git](https://github.com/3liSame7/Rule-Engine-Validator.git)  
 cd Rule-Engine-Validator

2. Set Your API Key

Create a file named `.env` and paste:

GROQ\_API\_KEY=your\_groq\_api\_key\_here

3. Run with Docker Compose

docker-compose up \--build

Visit:

* [http://localhost:8501](http://localhost:8501) (Streamlit UI)

* [http://localhost:8000](http://localhost:8000) (FastAPI backend)

---

**Deployment**

Backend (FastAPI)  
 Deployed on Render.com  
 URL: [https://rule-engine-validator.onrender.com](https://rule-engine-validator.onrender.com)

Frontend (Streamlit)  
 Deployed on Streamlit Community Cloud  
 Make sure to use the full backend URL inside all requests:

Example:  
 res \= requests.post("[https://rule-engine-validator.onrender.com/extract](https://rule-engine-validator.onrender.com/extract)", ...)

---

**Secrets Management**

In Streamlit Cloud → Settings → Secrets, store your environment variable:

GROQ\_API\_KEY="your-api-key-here"

Do not push `.env` to the public repo.

---

**Credits**

Developed by Ali Abdelrhman  
 Data Scientist & AI Engineer  
 LinkedIn:[Ali Abdelrhman | LinkedIn](https://www.linkedin.com/in/ali-abdelrhman-77376622b/)

---

**License**

MIT License – Free to use and modify.






