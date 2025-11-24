# 🎓 F-1 Visa Guidance System  
### **AI-Powered CPT / OPT Timeline + Checklist Generator**

This project implements a multi-agent F-1 visa assistance system designed to help international students understand their CPT and OPT eligibility, requirements, and compliance tasks.

The system combines:

- **Agent 1 — Policy Extractor (Scraper + RAG)**
- **Agent 2 — Timeline & Checklist Coordinator**
- **Streamlit UI — Modern, premium interface for end users**

This application transforms raw USCIS/ISSS immigration rules into a structured, personalized roadmap for international students.

---

## 🚀 Features

### **🧠 Agent 1 — Policy Extraction (Placeholder for Now)**
- Scrapes USCIS / ISSS content  
- Extracts rules, risks, timelines  
- Outputs standardized JSON  
- UI accepts this JSON manually for now  
- Will be fully integrated once the team uploads Agent 1 code  

### **📅 Agent 2 — Timeline Engine**
- Computes CPT eligibility date  
- Computes OPT application window  
- Generates milestone-based monthly checklist  
- Adds policy-triggered action steps  
- Fully integrated with Streamlit UI  

### **🎨 Premium Streamlit UI**
- Apple-style dark gradient theme  
- Sidebar student profile input  
- Policy dashboard with risk chips  
- Dynamic cards for:
  - Student snapshot  
  - Timeline overview  
  - Personalized checklist  
- Export button (`agent2_output.json`)  
- Ready for public deployment on Streamlit Cloud  

---

## 🏗️ Repository Structure

```
f1_visa_system/
│
├── app.py                 # Streamlit UI (Frontend)
├── agents_backend.py      # Agent 1 + Agent 2 backend logic
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## 📦 Installation (Local Development)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/f1_visa_system.git
cd f1_visa_system
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit application
```bash
streamlit run app.py
```

The UI will open at:  
👉 [http://localhost:8501](https://f-1-visa-guidance-system.streamlit.app/)

---

## 🌐 Deployment (Streamlit Cloud)

1. Push this full project to GitHub  
2. Open: **https://share.streamlit.io**  
3. Click **New App**  
4. Select:
   - Repository → this repo  
   - Branch → `main`  
   - Main file → `app.py`  
5. Click **Deploy**

You will get a public link like:

```
https://f1-visa-system.streamlit.app
```

Share this link with your team & professor.

---

## 🔄 Updating Agent 1

Once your teammates upload their Agent 1 code:

1. Open **agents_backend.py**
2. Replace this placeholder:

```python
def run_agent1(...):
    return get_default_agent1_updates()
```

3. Replace with real scraping + RAG pipeline  
4. Make sure it returns JSON in the format:

```json
[
  {
    "update": "CPT requires 1 academic year...",
    "source": "USCIS 2024",
    "risk_level": "medium",
    "action_needed": "Verify CPT eligibility window"
  }
]
```

The UI will automatically support it.  
No changes needed in `app.py`.

---

## 📁 requirements.txt (for local + cloud)

```
streamlit
python-dateutil
```

---

## 🧪 Demo Summary for Presentations

- Agent 1 extracts & structures immigration rules  
- Agent 2 merges rules + student profile  
- Streamlit UI displays:
  - CPT/OPT dates  
  - Month-wise checklist  
  - Policy-triggered compliance actions  
- Deployable on Streamlit Cloud with a shareable link  
