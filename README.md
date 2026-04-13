# AI Transformation Readiness Scorecard

A 20-question diagnostic that scores your organisation's AI readiness across 5 dimensions and delivers a personalised strategic report.

Built by CAL KNOX — Former Intelligence Analyst · C-Suite Strategy Consultant · AI Transformation Lead.

## Dimensions

1. **Strategic Alignment** — Is AI connected to real business goals?
2. **Data Foundations** — Is your data ready for AI workloads?
3. **Talent & Culture** — Do you have the human capacity to execute?
4. **Governance & Risk** — Are you managing AI risk properly?
5. **Execution Capability** — Can you actually ship?

## Running Locally

```bash
pip install -r requirements.txt
ANTHROPIC_API_KEY=your_key streamlit run app.py
```

## Deployment

Deploy to Streamlit Community Cloud:
1. Fork this repo
2. Connect to Streamlit Cloud
3. Add `ANTHROPIC_API_KEY` to secrets

## Stack

- Streamlit (UI)
- Anthropic Claude (report generation)
- Python