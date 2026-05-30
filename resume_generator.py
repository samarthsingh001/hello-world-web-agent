import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an expert resume writer. Given a user's background and a list of
in-demand skills from real job listings, write a professional, ATS-optimized resume in Markdown format.
Structure it with: Summary, Skills, Experience, Education, Projects.
Naturally weave in the top skills without making it look forced. Be concise and impactful."""


def generate_resume(user_info: dict, top_skills: list[str], job_title: str) -> str:
    """Call Claude API to generate a tailored resume."""

    user_message = f"""
Target Role: {job_title}

Top skills demanded by the market (weave these in naturally):
{", ".join(top_skills)}

User Background:
- Name: {user_info.get("name", "John Doe")}
- Years of Experience: {user_info.get("experience", "3")}
- Current/Past Role: {user_info.get("current_role", "Software Developer")}
- Education: {user_info.get("education", "B.S. Computer Science")}
- Key Projects: {user_info.get("projects", "Built a REST API, deployed on AWS")}
- Extra Info: {user_info.get("extra", "")}

Write a complete, professional resume in Markdown.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # prompt caching
            }
        ],
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text
