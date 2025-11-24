import datetime
from dateutil.relativedelta import relativedelta

# ============================================================
# AGENT 1: Policy / RAG Updates (Placeholder for now)
# ============================================================

# This is just a TEMPORARY implementation so the interface exists.
# Later, you can replace this with:
# - USCIS scraping
# - RAG retrieval
# - whatever Abhay / Pavithra build for Agent 1.


def get_default_agent1_updates():
    """Default hard-coded updates used for testing Agent 2."""
    return [
        {
            "update": "CPT requires 1 academic year of full-time enrollment.",
            "source": "USCIS Policy 2024",
            "risk_level": "medium",
            "action_needed": "Check CPT eligibility window",
        },
        {
            "update": "DSO must be notified within 10 days of job loss.",
            "source": "DHS 2025",
            "risk_level": "high",
            "action_needed": "Add job-loss notification step during OPT",
        },
    ]


def run_agent1(user_profile, raw_text: str | None = None):
    """
    Agent 1 placeholder.

    Parameters
    ----------
    user_profile : dict
        Student profile (arrival date, major, milestones, etc.)
    raw_text : str, optional
        Placeholder for future integration:
        - scraped USCIS content
        - ISSS rules
        - or any free-text corpus.

    Returns
    -------
    list[dict]
        A list of policy updates with keys:
        - 'update'
        - 'source'
        - 'risk_level'
        - 'action_needed'
    """
    # TODO: Replace this with actual RAG / LLM logic later.
    # For now, just return the default policy rules.
    return get_default_agent1_updates()


# ============================================================
# COMMON UTILITIES
# ============================================================

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def months_between(d1, d2):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)


# ============================================================
# AGENT 2: Timeline & Checklist Coordinator
# ============================================================

def compute_timeline(profile):
    """
    Compute CPT / OPT timeline based on arrival & graduation dates.
    """
    arrival = parse_date(profile["arrival_date"])
    grad = parse_date(profile["graduation_date"])
    today = datetime.date.today()

    months_since_arrival = months_between(arrival, today)

    timeline = {
        "today": today.isoformat(),
        "months_since_arrival": months_since_arrival,
        "cpt_eligibility_date": (arrival + relativedelta(months=12)).isoformat(),
        "opt_eligibility_start": (grad - relativedelta(days=90)).isoformat(),
        "opt_eligibility_end": grad.isoformat(),
    }

    return timeline


def generate_checklist(profile, timeline, agent1_updates):
    """
    Build a milestone-based checklist + policy-triggered actions.
    """
    checklist = {
        "Month 1": [],
        "Month 6": [],
        "Month 12 (CPT Eligibility)": [],
        "Pre-OPT Window": [],
        "Policy-Triggered Steps": [],
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
    """
    Main Agent 2 entry point used by the UI.
    """
    timeline = compute_timeline(user_profile)
    checklist = generate_checklist(user_profile, timeline, agent1_updates)
    final_output = {
        "user_profile": user_profile,
        "timeline": timeline,
        "checklist": checklist,
        "agent1_updates_used": agent1_updates,
    }
    return final_output


def summarize_policies(agent1_updates):
    """
    Helper for UI: count rules by risk level for status chips.
    """
    summary = {"high": 0, "medium": 0, "low": 0}
    for upd in agent1_updates:
        lvl = upd.get("risk_level", "").lower()
        if lvl in summary:
            summary[lvl] += 1
    return summary
