"""
AI Transformation Readiness Scorecard
by CAL KNOX — thecalknox.gumroad.com

A 20-question diagnostic that scores your organisation's AI readiness
across 5 dimensions and delivers a prioritised action report.
"""

import streamlit as st
import anthropic
import json
from datetime import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Readiness Scorecard | CAL KNOX",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── STYLING ────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background: #0D0D0D; }
    
    .hero {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border: 1px solid #C8A84B33;
        border-radius: 12px;
        padding: 2.5rem;
        margin-bottom: 2rem;
    }
    
    .hero h1 {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .hero p {
        color: #C8A84B;
        font-size: 1rem;
        margin: 0;
    }
    
    .dimension-header {
        background: #1A1A2E;
        border-left: 3px solid #C8A84B;
        padding: 0.75rem 1rem;
        margin: 1.5rem 0 1rem 0;
        border-radius: 0 6px 6px 0;
    }
    
    .dimension-header h3 {
        color: #C8A84B;
        margin: 0;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    .dimension-header p {
        color: #AAAAAA;
        margin: 0.25rem 0 0 0;
        font-size: 0.9rem;
    }

    .score-card {
        background: #1A1A2E;
        border: 1px solid #C8A84B44;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .score-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: #C8A84B;
    }
    
    .score-label {
        color: #FFFFFF;
        font-size: 1.1rem;
        margin-top: 0.25rem;
    }

    .report-section {
        background: #111111;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #C8A84B, #A8882B);
        color: #000000;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        width: 100%;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    
    .stButton > button:hover { opacity: 0.85; }
    
    .stRadio > div { gap: 0.5rem; }
    
    .footer {
        text-align: center;
        color: #555;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# ─── QUESTIONS ──────────────────────────────────────────────────
DIMENSIONS = [
    {
        "id": "strategy",
        "name": "Strategic Alignment",
        "description": "How clearly is AI connected to your business objectives",
        "questions": [
            {
                "id": "s1",
                "text": "Does your organisation have a documented AI strategy with clear goals?",
                "options": [
                    ("No strategy exists", 0),
                    ("Informal discussions have happened", 1),
                    ("A strategy exists but isn't widely shared", 2),
                    ("A clear strategy exists and is actively used", 3),
                ]
            },
            {
                "id": "s2",
                "text": "How well do your AI initiatives connect to measurable business outcomes?",
                "options": [
                    ("No connection — AI is exploratory", 0),
                    ("Loose connection — we hope it helps", 1),
                    ("Some KPIs defined but not consistently tracked", 2),
                    ("Clear ROI metrics for each AI initiative", 3),
                ]
            },
            {
                "id": "s3",
                "text": "How involved is senior leadership in AI decisions?",
                "options": [
                    ("AI is owned by IT/tech only", 0),
                    ("Occasional executive interest", 1),
                    ("One senior sponsor but limited broader engagement", 2),
                    ("AI is a board-level strategic priority", 3),
                ]
            },
            {
                "id": "s4",
                "text": "How does your AI investment compare to your strategic ambition?",
                "options": [
                    ("We talk about AI but invest very little", 0),
                    ("Small experiments with no committed roadmap", 1),
                    ("Moderate investment with a 12-month plan", 2),
                    ("Sustained investment with a multi-year roadmap", 3),
                ]
            },
        ]
    },
    {
        "id": "data",
        "name": "Data Foundations",
        "description": "The quality and accessibility of your data infrastructure",
        "questions": [
            {
                "id": "d1",
                "text": "How would you describe the quality of data your organisation holds?",
                "options": [
                    ("Poor — inconsistent, incomplete, untrusted", 0),
                    ("Mixed — some reliable sources, much noise", 1),
                    ("Reasonable — most key data is reliable", 2),
                    ("Strong — governed, clean, well-documented", 3),
                ]
            },
            {
                "id": "d2",
                "text": "How accessible is your data to the people and systems that need it?",
                "options": [
                    ("Siloed — data is locked in systems and teams", 0),
                    ("Partially accessible — some sharing, many barriers", 1),
                    ("Mostly accessible with some friction", 2),
                    ("Fully accessible — unified, self-serve, documented", 3),
                ]
            },
            {
                "id": "d3",
                "text": "Do you have data governance policies in place?",
                "options": [
                    ("No governance — data is ungoverned", 0),
                    ("Informal practices — no formal policy", 1),
                    ("Policy exists but inconsistently applied", 2),
                    ("Strong governance with clear ownership and compliance", 3),
                ]
            },
            {
                "id": "d4",
                "text": "How prepared is your data for AI/ML workloads?",
                "options": [
                    ("Not prepared — significant cleaning and structuring needed", 0),
                    ("Partially prepared — some datasets are AI-ready", 1),
                    ("Mostly prepared — key datasets are structured and labelled", 2),
                    ("Fully prepared — pipelines, labels, and infrastructure in place", 3),
                ]
            },
        ]
    },
    {
        "id": "talent",
        "name": "Talent & Culture",
        "description": "Your organisation's human capacity for AI adoption",
        "questions": [
            {
                "id": "t1",
                "text": "How would you describe AI literacy across your organisation?",
                "options": [
                    ("Very low — most people are unaware or fearful", 0),
                    ("Low — awareness exists but limited understanding", 1),
                    ("Moderate — pockets of capability, uneven distribution", 2),
                    ("High — broad AI literacy across functions", 3),
                ]
            },
            {
                "id": "t2",
                "text": "Does your organisation have dedicated AI/data science capability?",
                "options": [
                    ("No internal capability — fully dependent on vendors", 0),
                    ("1-2 people with relevant skills but no formal team", 1),
                    ("A small team exists but is under-resourced", 2),
                    ("A well-resourced team with clear mandate", 3),
                ]
            },
            {
                "id": "t3",
                "text": "How does your organisation's culture respond to AI-driven change?",
                "options": [
                    ("Resistant — significant fear and pushback", 0),
                    ("Cautious — scepticism is the default", 1),
                    ("Neutral — open but waiting to see results", 2),
                    ("Embracing — curiosity and experimentation are encouraged", 3),
                ]
            },
            {
                "id": "t4",
                "text": "How actively does your organisation invest in AI upskilling?",
                "options": [
                    ("No investment — learning is ad hoc", 0),
                    ("Occasional training with no systematic approach", 1),
                    ("Structured programmes for key roles", 2),
                    ("Organisation-wide upskilling with clear development paths", 3),
                ]
            },
        ]
    },
    {
        "id": "governance",
        "name": "Governance & Risk",
        "description": "How well your organisation manages AI risk and accountability",
        "questions": [
            {
                "id": "g1",
                "text": "Does your organisation have an AI ethics or responsible AI policy?",
                "options": [
                    ("No — ethics has not been considered formally", 0),
                    ("Informally — principles exist but aren't documented", 1),
                    ("A policy exists but isn't actively applied", 2),
                    ("A robust policy with clear accountability and review process", 3),
                ]
            },
            {
                "id": "g2",
                "text": "How does your organisation manage AI-related regulatory risk (GDPR, EU AI Act, etc.)?",
                "options": [
                    ("Not managing it — compliance is not on the radar", 0),
                    ("Aware but not yet acting", 1),
                    ("Partially compliant — some controls in place", 2),
                    ("Fully compliant with proactive monitoring", 3),
                ]
            },
            {
                "id": "g3",
                "text": "Is there a clear process for approving and deploying AI use cases?",
                "options": [
                    ("No process — teams do what they want", 0),
                    ("Informal — ad hoc approvals", 1),
                    ("A process exists for some use cases", 2),
                    ("A formal, consistent process for all AI deployments", 3),
                ]
            },
            {
                "id": "g4",
                "text": "How well does your organisation monitor AI systems in production?",
                "options": [
                    ("No monitoring — systems run without oversight", 0),
                    ("Basic monitoring — alerts for failures only", 1),
                    ("Regular reviews but no automated monitoring", 2),
                    ("Continuous monitoring with performance dashboards and drift detection", 3),
                ]
            },
        ]
    },
    {
        "id": "execution",
        "name": "Execution Capability",
        "description": "Your organisation's track record of delivering AI outcomes",
        "questions": [
            {
                "id": "e1",
                "text": "How many AI projects has your organisation successfully delivered to production?",
                "options": [
                    ("None", 0),
                    ("1-2 proof of concepts (not fully in production)", 1),
                    ("2-5 live use cases", 2),
                    ("5+ live use cases with measurable impact", 3),
                ]
            },
            {
                "id": "e2",
                "text": "How quickly can your organisation move from AI idea to working prototype?",
                "options": [
                    ("No clear pathway — would take many months", 0),
                    ("3-6 months with significant effort", 1),
                    ("4-8 weeks with the right team", 2),
                    ("1-2 weeks — rapid experimentation is the norm", 3),
                ]
            },
            {
                "id": "e3",
                "text": "How well does your technology infrastructure support AI workloads?",
                "options": [
                    ("Not at all — significant investment required first", 0),
                    ("Partially — some cloud or compute capability exists", 1),
                    ("Mostly — infrastructure is capable with some gaps", 2),
                    ("Fully — scalable, modern infrastructure purpose-built for AI", 3),
                ]
            },
            {
                "id": "e4",
                "text": "How effectively does your organisation learn from AI failures and iterate?",
                "options": [
                    ("Failures are avoided or hidden", 0),
                    ("Failures are acknowledged but rarely learned from", 1),
                    ("Post-mortems happen but learnings aren't always applied", 2),
                    ("Failure is a learning mechanism — rapid iteration is built in", 3),
                ]
            },
        ]
    },
]

# ─── SCORING ────────────────────────────────────────────────────
def calculate_scores(answers):
    dim_scores = {}
    total = 0
    max_total = 0
    for dim in DIMENSIONS:
        dim_total = 0
        dim_max = len(dim["questions"]) * 3
        for q in dim["questions"]:
            val = answers.get(q["id"], 0)
            dim_total += val
        pct = round((dim_total / dim_max) * 100)
        dim_scores[dim["id"]] = {
            "name": dim["name"],
            "score": dim_total,
            "max": dim_max,
            "pct": pct,
            "label": score_label(pct)
        }
        total += dim_total
        max_total += dim_max
    overall = round((total / max_total) * 100)
    return dim_scores, overall

def score_label(pct):
    if pct >= 80: return "Advanced"
    if pct >= 60: return "Developing"
    if pct >= 40: return "Emerging"
    return "Foundation"

def score_colour(pct):
    if pct >= 80: return "#4CAF50"
    if pct >= 60: return "#C8A84B"
    if pct >= 40: return "#FF9800"
    return "#F44336"

# ─── REPORT GENERATION ──────────────────────────────────────────
def generate_report(org_name, org_size, industry, dim_scores, overall, answers):
    client = anthropic.Anthropic()

    dim_summary = "\n".join([
        f"- {v['name']}: {v['pct']}% ({v['label']})"
        for v in dim_scores.values()
    ])

    answer_detail = []
    for dim in DIMENSIONS:
        for q in dim["questions"]:
            val = answers.get(q["id"], 0)
            option_text = q["options"][val][0]
            answer_detail.append(f"[{dim['name']}] {q['text']}\nAnswer: {option_text} (score: {val}/3)")

    answers_text = "\n\n".join(answer_detail)

    prompt = f"""You are CAL KNOX — a former intelligence analyst and C-suite strategy consultant specialising in AI transformation. Your voice is direct, authoritative, and precise. No filler. No corporate fluff.

You have just assessed {org_name}, a {org_size} organisation in {industry}.

ASSESSMENT RESULTS:
Overall AI Readiness Score: {overall}%

Dimension Breakdown:
{dim_summary}

DETAILED ANSWERS:
{answers_text}

Write a strategic AI readiness report with the following sections:

## Executive Summary
2-3 sentences. What's the headline verdict on this organisation's AI readiness? Be direct.

## Where You Stand
A clear interpretation of the overall score and what it means in practice. Reference the stage (Foundation/Emerging/Developing/Advanced). What does this score mean for competitive position?

## Dimension Analysis
For each of the 5 dimensions, write 2-3 sentences: what the score reveals, what the specific answers tell you, and one concrete implication.

## Priority Actions (Top 3)
The three highest-leverage actions this organisation should take in the next 90 days. Be specific. Reference their actual answers. Explain the sequencing — why these three, why in this order.

## What Good Looks Like
A brief picture of where this organisation could realistically be in 12 months if they execute well. Make it concrete and ambitious but credible.

## One Thing To Avoid
The single biggest mistake organisations at this stage make. Direct warning.

---
Tone: Direct. Credible. No hedging. Write as someone who has sat in these rooms and seen what works and what fails. The reader is a senior executive — don't explain things they already know, give them the uncomfortable truths they haven't faced yet."""

    with st.spinner("Generating your personalised report..."):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

    return response.content[0].text

# ─── APP STATE ──────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "report" not in st.session_state:
    st.session_state.report = None
if "org_info" not in st.session_state:
    st.session_state.org_info = {}

# ─── INTRO ──────────────────────────────────────────────────────
if st.session_state.step == "intro":
    st.markdown("""
    <div class="hero">
        <h1>AI Transformation Readiness Scorecard</h1>
        <p>Intelligence-grade diagnostic for organisations serious about AI</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Most AI transformation efforts fail — not because the technology doesn't work, but because organisations don't honestly assess where they stand before they move.

    This scorecard gives you a rigorous, honest picture of your AI readiness across five dimensions:

    - **Strategic Alignment** — Is AI connected to real business goals?
    - **Data Foundations** — Is your data ready for AI workloads?
    - **Talent & Culture** — Do you have the human capacity to execute?
    - **Governance & Risk** — Are you managing AI risk properly?
    - **Execution Capability** — Can you actually ship?

    **20 questions. 10 minutes. A report that tells you the truth.**
    """)

    st.divider()

    with st.form("org_info"):
        st.subheader("Tell me about your organisation")
        org_name = st.text_input("Organisation name (or use a pseudonym)", placeholder="e.g. Acme Corp")
        org_size = st.selectbox("Organisation size", [
            "1-10 people", "11-50 people", "51-250 people",
            "251-1,000 people", "1,000-10,000 people", "10,000+ people"
        ])
        industry = st.selectbox("Industry", [
            "Financial Services", "Healthcare & Life Sciences", "Retail & Consumer",
            "Manufacturing", "Technology", "Professional Services / Consulting",
            "Public Sector / Government", "Media & Entertainment", "Energy & Utilities",
            "Education", "Other"
        ])
        your_role = st.text_input("Your role", placeholder="e.g. CTO, Head of Digital, CEO")

        submitted = st.form_submit_button("Start Assessment →")
        if submitted and org_name:
            st.session_state.org_info = {
                "name": org_name,
                "size": org_size,
                "industry": industry,
                "role": your_role
            }
            st.session_state.step = "questions"
            st.rerun()

    st.markdown("""
    <div class="footer">
        CAL KNOX · Former Intelligence Analyst · C-Suite AI Transformation Consultant<br>
        <a href="https://x.com/TheCalKnox" style="color: #C8A84B;">@TheCalKnox</a>
    </div>
    """, unsafe_allow_html=True)

# ─── QUESTIONS ──────────────────────────────────────────────────
elif st.session_state.step == "questions":
    st.markdown(f"""
    <div class="hero">
        <h1>AI Readiness Assessment</h1>
        <p>Assessing: {st.session_state.org_info.get('name', 'Your Organisation')}</p>
    </div>
    """, unsafe_allow_html=True)

    progress = len(st.session_state.answers) / 20
    st.progress(progress, text=f"{len(st.session_state.answers)}/20 questions answered")

    with st.form("questions_form"):
        all_answered = True
        for dim in DIMENSIONS:
            st.markdown(f"""
            <div class="dimension-header">
                <h3>{dim['name']}</h3>
                <p>{dim['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            for q in dim["questions"]:
                options = [opt[0] for opt in q["options"]]
                current = st.session_state.answers.get(q["id"], None)
                current_idx = current if current is not None else 0
                answer = st.radio(
                    q["text"],
                    options=options,
                    index=current_idx,
                    key=f"q_{q['id']}"
                )
                idx = options.index(answer)
                st.session_state.answers[q["id"]] = idx

        submitted = st.form_submit_button("Generate My Report →")
        if submitted:
            st.session_state.step = "report"
            st.rerun()

# ─── REPORT ─────────────────────────────────────────────────────
elif st.session_state.step == "report":
    org = st.session_state.org_info
    answers = st.session_state.answers

    dim_scores, overall = calculate_scores(answers)

    st.markdown(f"""
    <div class="hero">
        <h1>AI Readiness Report</h1>
        <p>{org.get('name', 'Your Organisation')} · {org.get('industry', '')} · {datetime.now().strftime('%B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Overall score
    overall_label = score_label(overall)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number" style="color: {score_colour(overall)}">{overall}%</div>
            <div class="score-label">Overall AI Readiness — {overall_label}</div>
        </div>
        """, unsafe_allow_html=True)

    # Dimension scores
    st.subheader("Dimension Breakdown")
    cols = st.columns(5)
    for i, (dim_id, data) in enumerate(dim_scores.items()):
        with cols[i]:
            st.metric(
                label=data["name"].split(" ")[0],
                value=f"{data['pct']}%",
                delta=data["label"]
            )

    st.divider()

    # Generate or show cached report
    if not st.session_state.report:
        st.session_state.report = generate_report(
            org.get("name", "Your Organisation"),
            org.get("size", ""),
            org.get("industry", ""),
            dim_scores,
            overall,
            answers
        )

    st.markdown(st.session_state.report)

    st.divider()

    # CTA
    st.markdown("""
    ### What Next?

    This report gives you the honest picture. What you do with it determines whether you're still having the same conversation in 12 months.

    If you want to move faster — or want a second opinion from someone who's run AI transformations across global enterprises — reach out.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Follow @TheCalKnox on X →", "https://x.com/TheCalKnox")
    with col2:
        st.link_button("More tools & frameworks →", "https://thecalknox.gumroad.com")

    if st.button("Retake Assessment"):
        st.session_state.step = "intro"
        st.session_state.answers = {}
        st.session_state.report = None
        st.rerun()

    st.markdown("""
    <div class="footer">
        CAL KNOX · AI Readiness Scorecard · thecalknox.gumroad.com
    </div>
    """, unsafe_allow_html=True)
