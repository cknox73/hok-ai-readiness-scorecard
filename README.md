# AI Transformation Readiness Scorecard

A 20-question diagnostic that scores your organisation's AI readiness across 5 dimensions and delivers a personalised strategic report.

Built by CAL KNOX — Former Intelligence Analyst · C-Suite Strategy Consultant · AI Transformation Lead.

**Live App: https://hok-ai-readiness-scorecard.streamlit.app**

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

## Deployment to Streamlit Community Cloud

### Quick Deploy (One Click)

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge.svg)](https://share.streamlit.io/deploy)

### Manual Deployment

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"Deploy a public app"**
4. Select repository: `cknox73/hok-ai-readiness-scorecard`
5. Branch: `master`
6. Main file path: `app.py`
7. Click **Deploy**

### Required Secrets

After deployment, add the following secret in Streamlit Cloud settings:
- `ANTHROPIC_API_KEY` — Your Anthropic API key (starts with `sk-ant-`)

Get an API key at: [console.anthropic.com](https://console.anthropic.com)

## Repository

GitHub: https://github.com/cknox73/hok-ai-readiness-scorecard

## Stack

- Streamlit (UI)
- Anthropic Claude Opus 4 (report generation)
- Python 3.12+
