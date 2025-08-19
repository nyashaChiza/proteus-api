# 🌀 Proteus API
**The Autonomous Job Hunter Backend**

Proteus API powers the AI-driven job hunting pipeline. It handles:
- Job scraping and aggregation
- Resume and cover letter customization
- Automated application submission via email or web forms
- Scoring applications and storing outcomes for future learning

## Tech Stack
- **Backend Framework**: FastAPI
- **Database**: SQLite (upgrade to Postgres when scaling)
- **Automation Tools**: Jobspy, Playwright, smtplib
- **AI / NLP**: GPT4All, spaCy, keyword-based scoring

## Endpoints
- `/jobs` → list and scrape new jobs
- `/resume/customize` → generate tailored resume for a specific job
- `/apply` → submit applications via email or web
- `/applications` → view status and outcomes
- `/scores` → calculate and retrieve keyword-based success rates

## Roadmap
- [ ] Implement Jobspy scraping and SQLite storage
- [ ] GPT4All-based resume and cover letter generation
- [ ] Automated email applications
- [ ] Playwright automation for web forms
- [ ] Application scoring and follow-up alerts
- [ ] Machine learning feedback loop for improved success rate
