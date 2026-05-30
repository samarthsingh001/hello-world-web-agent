import re
from collections import Counter

SKILL_KEYWORDS = [
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby",
    "react", "angular", "vue", "node.js", "next.js", "django", "flask", "fastapi",
    "spring", "express",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd",
    "git", "linux", "rest", "graphql", "grpc",
    "machine learning", "deep learning", "tensorflow", "pytorch", "pandas", "numpy",
    "agile", "scrum", "communication", "teamwork", "problem-solving",
]


def extract_skills(jobs: list[dict]) -> dict:
    """Return skill frequency counts and top skills from job listings."""
    all_text = " ".join(
        (j.get("title", "") + " " + j.get("description", "")).lower()
        for j in jobs
    )

    counts = Counter()
    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        matches = re.findall(pattern, all_text)
        if matches:
            counts[skill] = len(matches)

    top_skills = [skill for skill, _ in counts.most_common(15)]
    return {"counts": dict(counts), "top_skills": top_skills}


def summarize(jobs: list[dict], skills: dict) -> str:
    """Human-readable summary of what the market wants."""
    lines = [f"Analyzed {len(jobs)} job listings.", "Top skills in demand:"]
    for skill in skills["top_skills"]:
        lines.append(f"  - {skill} (mentioned {skills['counts'][skill]}x)")
    return "\n".join(lines)
