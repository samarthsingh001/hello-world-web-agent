from flask import Flask, render_template, request, jsonify
from crawler import scrape_indeed
from analyzer import extract_skills, summarize
from resume_generator import generate_resume

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    job_title = data.get("job_title", "Software Engineer")
    location = data.get("location", "")
    user_info = {
        "name": data.get("name", ""),
        "experience": data.get("experience", ""),
        "current_role": data.get("current_role", ""),
        "education": data.get("education", ""),
        "projects": data.get("projects", ""),
        "extra": data.get("extra", ""),
    }

    jobs = scrape_indeed(job_title, location)
    skills = extract_skills(jobs)
    market_summary = summarize(jobs, skills)
    resume = generate_resume(user_info, skills["top_skills"], job_title)

    return jsonify({
        "resume": resume,
        "market_summary": market_summary,
        "top_skills": skills["top_skills"],
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
