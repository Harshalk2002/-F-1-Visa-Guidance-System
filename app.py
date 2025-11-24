import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
import json

# ============================================================
# 1. DATE UTILITIES
# ============================================================

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def months_between(d1, d2):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)

# ============================================================
# 2. TIMELINE ENGINE (CPT, OPT, etc.)
# ============================================================

def compute_timeline(profile):
    arrival = parse_date(profile["arrival_date"])
    grad = parse_date(profile["graduation_date"])
    today = datetime.date.today()

    months_since_arrival = months_between(arrival, today)

    timeline = {
        "today": today.isoformat(),
        "months_since_arrival": months_since_arrival,
        "cpt_eligibility_date": (arrival + relativedelta(months=12)).isoformat(),
        "opt_eligibility_start": (grad - relativedelta(days=90)).isoformat(),
        "opt_eligibility_end": grad.isoformat()
    }

    return timeline

# ============================================================
# 3. CHECKLIST GENERATOR
# ============================================================

def generate_checklist(profile, timeline, agent1_updates):
    checklist = {
        "Month 1": [],
        "Month 6": [],
        "Month 12 (CPT Eligibility)": [],
        "Pre-OPT Window": [],
        "Policy-Triggered Steps": []
    }

    # ----- Month 1 Tasks -----
    if not profile["milestones"]["sevis_checkin"]:
        checklist["Month 1"].append("Complete SEVIS Check-In")

    if not profile["milestones"]["passport_uploaded"]:
        checklist["Month 1"].append("Upload Passport to ISSS Portal")

    # ----- Month 6 Tasks -----
    if not profile["milestones"]["first_semester_complete"]:
        checklist["Month 6"].append("Meet Academic Advisor")
        checklist["Month 6"].append("Confirm Full-Time Enrollment")

    # ----- Month 12 Tasks -----
    cpt_date = parse_date(timeline["cpt_eligibility_date"])
    checklist["Month 12 (CPT Eligibility)"].append(
        f"CPT becomes available on {cpt_date} – begin employer search"
    )
    checklist["Month 12 (CPT Eligibility)"].append(
        "Request CPT I-20 endorsement (30 days before CPT start date)"
    )

    # ----- Pre-OPT Tasks -----
    opt_start = parse_date(timeline["opt_eligibility_start"])
    checklist["Pre-OPT Window"].append(
        f"Prepare OPT documents (start 90 days before graduation → {opt_start})"
    )
    checklist["Pre-OPT Window"].append("Obtain employer letter for OPT")
    checklist["Pre-OPT Window"].append("Submit Form I-765")

    # ----- Policy-triggered tasks from Agent 1 -----
    for upd in agent1_updates:
        checklist["Policy-Triggered Steps"].append(
            f"{upd['action_needed']} (Rule: {upd['update']})"
        )

    return checklist

def run_agent2(user_profile, agent1_updates):
    timeline = compute_timeline(user_profile)
    checklist = generate_checklist(user_profile, timeline, agent1_updates)
    final_output = {
        "user_profile": user_profile,
        "timeline": timeline,
        "checklist": checklist,
        "agent1_updates_used": agent1_updates
    }
    return final_output

def summarize_policies(agent1_updates):
    summary = {"high": 0, "medium": 0, "low": 0}
    for upd in agent1_updates:
        lvl = upd.get("risk_level", "").lower()
        if lvl in summary:
            summary[lvl] += 1
    return summary

# ============================================================
# 4. STREAMLIT UI
# ============================================================

st.set_page_config(page_title="F-1 Visa Timeline & Chat Assistant", layout="wide")

# ---------- Premium CSS ----------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1e293b 0, #020617 45%, #020617 100%);
    color: #f5f5f5;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
}

/* Gradient header strip */
.hero-strip {
    background: linear-gradient(120deg, #6366f1, #22c55e, #0ea5e9);
    padding: 1.1rem 2rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 18px 45px rgba(15,23,42,0.8);
}

/* Main title */
.hero-title {
    font-size: 2.4rem;
    font-weight: 750;
    margin: 0;
}
.hero-subtitle {
    margin: 0;
    font-size: 0.96rem;
    opacity: 0.9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: rgba(15,23,42,0.96);
    padding: 18px 12px;
    border-right: 1px solid #1f2937;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e5e7eb !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stDateInput input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    border: 1px solid #1f2937 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #4f46e5, #06b6d4) !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 0.7rem 1.8rem;
    font-size: 0.98rem;
    font-weight: 650;
    border: none;
    box-shadow: 0 10px 25px rgba(15,23,42,0.6);
}
.stButton>button:hover {
    filter: brightness(1.1);
}

/* Chat styles */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 0.5rem;
}
.chat-row-user {
    display: flex;
    justify-content: flex-end;
}
.chat-row-bot {
    display: flex;
    justify-content: flex-start;
}
.chat-bubble {
    max-width: 70%;
    padding: 0.6rem 0.9rem;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.4;
}
.chat-bubble-user {
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    color: white;
    border-bottom-right-radius: 4px;
}
.chat-bubble-bot {
    background-color: #020617;
    border: 1px solid rgba(148,163,184,0.45);
    color: #e5e7eb;
    border-bottom-left-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero header ----------
st.markdown("""
<div class="hero-strip">
    <div style="display:flex;align-items:center;gap:1rem;">
        <div style="font-size:2.1rem;">🎓</div>
        <div>
            <p class="hero-title">F-1 Visa Timeline & Chat Assistant</p>
            <p class="hero-subtitle">Smart multi-agent system for CPT, OPT, SEVIS & immigration guidance.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ----- Sidebar Inputs -----
st.sidebar.header("Student Profile")

name = st.sidebar.text_input("Name", value="", placeholder="e.g., Amina")
major = st.sidebar.text_input("Major", value="", placeholder="e.g., Computer Science")
degree_level = st.sidebar.selectbox("Degree Level", ["Bachelors", "Masters", "PhD"], index=1)

arrival_date_input = st.sidebar.date_input("Arrival Date", value=datetime.date(2025, 1, 5))
graduation_date_input = st.sidebar.date_input("Graduation Date", value=datetime.date(2026, 12, 15))

st.sidebar.subheader("Milestones")
sevis_checkin = st.sidebar.checkbox("SEVIS Check-In completed", value=True)
passport_uploaded = st.sidebar.checkbox("Passport uploaded", value=True)
first_semester_complete = st.sidebar.checkbox("First semester complete", value=False)
cpt_applied = st.sidebar.checkbox("CPT applied", value=False)
opt_applied = st.sidebar.checkbox("OPT applied", value=False)

user_profile = {
    "name": name if name.strip() else "Student",
    "arrival_date": arrival_date_input.isoformat(),
    "major": major if major.strip() else "N/A",
    "degree_level": degree_level,
    "graduation_date": graduation_date_input.isoformat(),
    "milestones": {
        "sevis_checkin": sevis_checkin,
        "passport_uploaded": passport_uploaded,
        "first_semester_complete": first_semester_complete,
        "cpt_applied": cpt_applied,
        "opt_applied": opt_applied,
    },
}

# ----- Maintain Chat State -----
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "assistant", "content": "Hi! I’m your F-1 visa assistant. Ask me anything about CPT, OPT, SEVIS, or timelines."}
    ]

# ----- Tabs -----
tab1, tab2 = st.tabs(["📊 Timeline & Checklist", "💬 Chat Assistant"])

# ============================================================
# TIMELINE TAB
# ============================================================
with tab1:

    st.subheader("📘 Agent 1 Policy Updates (Temporary JSON Input)")

    default_agent1 = json.dumps([
        {
            "update": "CPT requires 1 academic year of full-time enrollment.",
            "source": "USCIS Policy 2024",
            "risk_level": "medium",
            "action_needed": "Check CPT eligibility window"
        },
        {
            "update": "DSO must be notified within 10 days of job loss.",
            "source": "DHS 2025",
            "risk_level": "high",
            "action_needed": "Add job-loss notification step during OPT"
        }
    ], indent=4)

    agent1_text = st.text_area("Agent 1 JSON", value=default_agent1, height=200)

    try:
        agent1_updates = json.loads(agent1_text)
        parse_error = False
    except:
        st.error("Invalid JSON")
        agent1_updates = []
        parse_error = True

    if not parse_error and agent1_updates:
        summary = summarize_policies(agent1_updates)
        st.write(f"High risk: {summary['high']} | Medium: {summary['medium']} | Low: {summary['low']}")

    run = st.button("Generate Timeline & Checklist")

    if run and not parse_error:
        output = run_agent2(user_profile, agent1_updates)

        st.success("Generated!")

        st.subheader("👤 Student Snapshot")
        st.write(output["user_profile"])

        st.subheader("📅 Timeline")
        st.write(output["timeline"])

        st.subheader("📝 Checklist")
        for section, items in output["checklist"].items():
            with st.expander(section):
                for item in items:
                    st.markdown(f"- {item}")

        st.download_button(
            "Download JSON",
            data=json.dumps(output, indent=4),
            file_name="agent2_output.json"
        )

# ============================================================
# CHAT TAB
# ============================================================
with tab2:

    st.subheader("💬 Chat with Your F-1 Assistant")
    st.caption("Backend team will plug in multi-agent logic here.")

    # Display chat messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='chat-row-user'><div class='chat-bubble chat-bubble-user'>{msg['content']}</div></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-row-bot'><div class='chat-bubble chat-bubble-bot'>{msg['content']}</div></div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question...", placeholder="When can I apply for OPT?")
        send = st.form_submit_button("Send")

    if send and user_input.strip():
        # Store user message
        st.session_state["chat_messages"].append(
            {"role": "user", "content": user_input}
        )

        # =======================
        # BACKEND TEAM TODO HERE
        # =======================
        assistant_reply = (
            "Thanks for your question! In the final system, this answer will come from "
            "the integrated multi-agent system (Agent 1 + Agent 2)."
        )

        st.session_state["chat_messages"].append(
            {"role": "assistant", "content": assistant_reply}
        )

        st.rerun()
