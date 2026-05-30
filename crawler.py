import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def scrape_indeed(job_title: str, location: str = "", num_pages: int = 2) -> list[dict]:
    jobs = []
    query = job_title.replace(" ", "+")
    loc = location.replace(" ", "+")

    for page in range(num_pages):
        start = page * 10
        url = f"https://www.indeed.com/jobs?q={query}&l={loc}&start={start}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[crawler] Failed to fetch page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("div", class_="job_seen_beacon")

        for card in cards:
            title_el = card.find("h2", class_="jobTitle")
            company_el = card.find("span", attrs={"data-testid": "company-name"})
            desc_el = card.find("div", class_="job-snippet")

            title = title_el.get_text(strip=True) if title_el else ""
            company = company_el.get_text(strip=True) if company_el else ""
            description = desc_el.get_text(separator=" ", strip=True) if desc_el else ""

            if title:
                jobs.append({
                    "title": title,
                    "company": company,
                    "description": description,
                })

        time.sleep(1)  # polite delay between pages

    # fallback sample data if scraping is blocked
    if not jobs:
        jobs = _fallback_jobs(job_title)

    return jobs


def _fallback_jobs(role: str) -> list[dict]:
    """Returns sample job data when live scraping is blocked."""
    return [
        {
            "title": f"Senior {role}",
            "company": "TechCorp Inc.",
            "description": (
                "Looking for a skilled professional with experience in Python, "
                "REST APIs, SQL, Docker, AWS, and strong communication skills. "
                "Agile environment, 3+ years experience required."
            ),
        },
        {
            "title": f"{role}",
            "company": "StartupXYZ",
            "description": (
                "Join our team! Requirements: JavaScript, React, Node.js, "
                "MongoDB, Git, CI/CD pipelines, problem-solving mindset."
            ),
        },
        {
            "title": f"Junior {role}",
            "company": "GlobalSoft",
            "description": (
                "Great entry-level opportunity. Skills: Java, Spring Boot, "
                "MySQL, unit testing, communication, teamwork."
            ),
        },
    ]
