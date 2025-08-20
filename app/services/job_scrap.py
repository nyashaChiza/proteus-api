# app/services/jobscraper.py
import requests
from bs4 import BeautifulSoup
import random
from typing import List, Dict
from typing import List, Dict
from app.models.job import Job
from app.db.database import get_db


BASE_HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    ]),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}


def scrape_vacancymail(query: str, limit: int = 10) -> List[Dict]:
    url = f"https://vacancymail.co.zw/jobs/?search={query.replace(' ', '+')}&location="
    resp = requests.get(url, headers=BASE_HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    for job_card in soup.select(".job-listing-details"):
        title_el = job_card.select_one("h3.job-listing-title")
        company_el = job_card.select_one("h4.job-listing-company")
        summary_el = job_card.select_one("p.job-listing-text")
        
        # Try to find link if the parent <a> exists
        link_el = job_card.find_parent("a")
        link = link_el['href'] if link_el else None

        if not title_el:
            continue

        jobs.append({
            "title": title_el.get_text(strip=True),
            "company": company_el.get_text(strip=True) if company_el else None,
            "summary": summary_el.get_text(" ", strip=True) if summary_el else None,
            "link": link,
            "source": "vacancymail"
        })

        if len(jobs) >= limit:
            break

    return jobs


def scrape_zimbajob(query: str, limit: int = 10) -> list[dict]:
    url = f"https://www.zimbajob.com/job-vacancies-search-zimbabwe/{query.replace(' ', '+')}"
    resp = requests.get(url, headers=BASE_HEADERS, timeout=10)
    print(url, resp.status_code)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    for job_card in soup.select(".card.card-job"):
        # Link from data-href
        link = job_card.get("data-href")

        # Title
        title_el = job_card.select_one("h3 a")
        title = title_el.get_text(strip=True) if title_el else None

        # Company
        company_el = job_card.select_one("a.card-job-company.company-name")
        company = company_el.get_text(strip=True) if company_el else None

        # Summary
        summary_el = job_card.select_one("div.card-job-description p")
        summary = summary_el.get_text(" ", strip=True) if summary_el else None

        # Location: <li> containing "Region of"
        location_el = None
        for li in job_card.select("ul li"):
            if "Region of" in li.get_text():
                location_el = li.get_text(strip=True).replace("Region of :", "").strip()
                break

        if not title:
            continue

        jobs.append({
            "title": title,
            "company": company,
            "location": location_el,
            "summary": summary,
            "link": link,
            "source": "zimjob"
        })

        if len(jobs) >= limit:
            break

    return jobs


def scrape_ihararejobs(query: str, limit: int = 10) -> list[dict]:
    url = f"https://ihararejobs.com/jobs/?search={query.replace(' ', '+')}"
    resp = requests.get(url, headers=BASE_HEADERS, timeout=10)
    print(url, resp.status_code)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    for job_card in soup.select(".sidebar-list-single"):
        details = job_card.select_one(".company-list-details")
        if not details:
            continue

        # Title & link
        title_el = details.select_one("h3 a")
        link = title_el['href'] if title_el else None

        # Location: first <p class="company-state"> with map-marker icon
        location_el = details.select_one('p.company-state i.fa-map-marker')
        location = location_el.parent.get_text(strip=True).replace('Harare', 'Harare') if location_el else None

        # Company: <p class="company-state"> with building icon
        company_el = details.select_one('p.company-state i.fa-building')
        company = company_el.parent.get_text(strip=True) if company_el else None

        if not title_el:
            continue

        jobs.append({
            "title": title_el.get_text(strip=True),
            "company": company,
            "location": location,
            "link": f"https://ihararejobs.com{link}" if link else None,
            "source": "ihararejobs"
        })

        if len(jobs) >= limit:
            break

    return jobs



def scrape_all_sites(query: str, limit_per_site: int = 5) -> List[Dict]:
    jobs = []
    jobs.extend(scrape_vacancymail(query, limit_per_site))
    jobs.extend(scrape_zimbajob(query, limit_per_site))
    jobs.extend(scrape_ihararejobs(query, limit_per_site))
    return jobs[:limit_per_site * 4]

from app.db.database import get_db
from app.models.job import Job

def save_jobs(query: str) -> int:
    """
    Save a list of jobs to the database.
    Skips jobs that already exist (based on URL).
    Returns the number of jobs inserted.
    """
    inserted_count = 0

    # Get the actual session from the generator
    db = next(get_db())

    jobs = scrape_all_sites(query, limit_per_site=5)
    for job_data in jobs:
        url = job_data.get("link") or job_data.get("url")
        if not url:
            continue

        # Check if job with same URL already exists
        existing = db.query(Job).filter(Job.url == url).first()
        if existing:
            continue

        job = Job(
            title=job_data.get("title"),
            company=job_data.get("company"),
            location=job_data.get("location"),
            description=job_data.get("summary") or job_data.get("description"),
            url=url,
            source=job_data.get("source"),
        )
        db.add(job)
        inserted_count += 1

    db.commit()
    db.close()
    return inserted_count

