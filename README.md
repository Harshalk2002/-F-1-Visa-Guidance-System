🎓 F-1 Visa Guidance System – Agent 1 + Agent 2
Timeline Generator, Checklist Builder & Policy Analyzer

This project implements a multi-agent F-1 Visa Guidance System built for the MSA 8770 Final Project.
It combines Agent 1 (Policy Extraction) and Agent 2 (Timeline & Checklist Coordinator) into a single modular system with a premium Streamlit UI.

🧠 System Overview

Agent 1 – Policy Extractor (RAG / Scraper)

Scrapes USCIS / ISSS websites

Chunks content

Extracts policies (rules, risks, required actions)

Outputs standardized JSON

Agent 2 – Timeline & Checklist Coordinator

Reads student profile

Reads Agent 1’s JSON rules

Builds:

CPT eligibility timeline

OPT filing window

Month-wise checklist

Policy-triggered action items

Streamlit UI (Frontend)

Premium Apple-style interface

Sidebar: Student profile + milestones

Main panel: Agent 1 JSON, timeline, checklist

JSON export button

🏗️ Project Architecture
f1_visa_system/
│
├── agents_backend.py      # Agent 1 (placeholder) + Agent 2 backend logic
├── app.py                 # Streamlit UI (Frontend)
├── requirements.txt       # Dependencies for Streamlit Cloud
└── README.md              # Documentation

🚀 Features
✔ Agent 1 (currently placeholder)

Provides sample policy rules

Can later be replaced with real scraping + RAG outputs

UI is already wired to accept JSON from Agent 1

✔ Agent 2

Computes CPT eligibility date

Computes OPT window

Generates month-wise checklist

Tracks milestones

Adds policy-driven tasks

✔ Streamlit UI

Premium dark gradient theme

Clean card-based layout

Sidebar for profile input

Policy JSON viewer

Risk-level chips (High / Medium / Low)

Export button (agent2_output.json)

📦 Installation (Local Machine)
1. Clone the repo
git clone https://github.com/<your-username>/f1_visa_system.git
cd f1_visa_system

2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py


Your browser will open at:

http://localhost:8501

🌐 Deploy on Streamlit Cloud

Go to https://share.streamlit.io

Connect your GitHub account

Click New App

Select:

Repository → <your repo>

Branch → main

Main file → app.py

Click Deploy

You will get a public link like:

https://f1-visa-system.streamlit.app


Share this link with your team & professor.

🔄 How Teammates Add Agent 1 Later

Once Pavithra / Abhay finalize Agent 1:

Open agents_backend.py

Replace the placeholder function:

def run_agent1(...):
    return get_default_agent1_updates()


with the real:

scraper

chunker

embedder

retriever

rule extractor

Make sure it returns a list of objects like:

[
  {
    "update": "CPT requires 1 academic year...",
    "source": "USCIS 2024",
    "risk_level": "medium",
    "action_needed": "Verify CPT eligibility window"
  }
]


No changes to the UI are needed — it will automatically start using real Agent 1 output.

📁 Requirements File
streamlit
python-dateutil


Perfect for Streamlit Cloud and local use.

🎤 Demo Flow (What to Say in Presentation)

“Agent 1 extracts immigration rules dynamically from USCIS.”

“Agent 2 combines those rules with student data.”

“The UI visualizes CPT/OPT windows & generates an actionable checklist.”

“Everything is modular — we can add Agent 3 later if needed.”

👑 Final Notes

This repo is designed for:

clean professor review

easy teammate collaboration

smooth future expansion

If you add new agents later, simply create new files like:

agent3_employer_checker.py
agent4_visa_risk_analyzer.py


The architecture can grow infinitely without breaking.
