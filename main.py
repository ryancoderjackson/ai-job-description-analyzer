import json
import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)


def get_multiline_input(prompt_text: str) -> str:
    print(f"\n{prompt_text}")
    print("Type END on a new line when finished.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def analyze_resume_vs_job(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a technical resume analysis assistant.

Compare the candidate resume to the job description and return JSON only.

Return this exact structure:
{{
  "job_title_guess": "",
  "seniority_level": "",
  "required_skills": [],
  "preferred_skills": [],
  "resume_strengths": [],
  "missing_or_weak_skills": [],
  "match_score": 0,
  "fit_assessment": "",
  "tailored_resume_suggestions": []
}}

Rules:
- "match_score" must be an integer from 0 to 100.
- Only return valid JSON.
- Be realistic, not overly generous.
- Base the analysis only on the provided resume and job description.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    except RateLimitError:
        raise ValueError(
            "OpenAI API quota/billing issue: check your billing setup and available credits."
        )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{content}")


def save_analysis(result: dict, filename: str = "analysis_output.json") -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)


def print_pretty_report(result: dict) -> None:
    print("\n" + "=" * 60)
    print("RESUME VS JOB MATCH REPORT")
    print("=" * 60)

    print(f"\nJob Title Guess: {result.get('job_title_guess', 'N/A')}")
    print(f"Seniority Level: {result.get('seniority_level', 'N/A')}")
    print(f"Match Score: {result.get('match_score', 'N/A')}%")

    print("\nRequired Skills:")
    for skill in result.get("required_skills", []):
        print(f"- {skill}")

    print("\nPreferred Skills:")
    for skill in result.get("preferred_skills", []):
        print(f"- {skill}")

    print("\nResume Strengths:")
    for item in result.get("resume_strengths", []):
        print(f"- {item}")

    print("\nMissing or Weak Skills:")
    for item in result.get("missing_or_weak_skills", []):
        print(f"- {item}")

    print("\nFit Assessment:")
    print(result.get("fit_assessment", "N/A"))

    print("\nTailored Resume Suggestions:")
    for item in result.get("tailored_resume_suggestions", []):
        print(f"- {item}")

    print("\n" + "=" * 60)


def main() -> None:
    print("AI Resume vs Job Matcher v2")

    resume_text = get_multiline_input("Paste your resume text below.")
    if not resume_text:
        print("No resume text provided.")
        return

    job_description = get_multiline_input("Paste the job description below.")
    if not job_description:
        print("No job description provided.")
        return

    print("\nAnalyzing...\n")
    result = analyze_resume_vs_job(resume_text, job_description)

    print_pretty_report(result)
    save_analysis(result)
    print("\nAnalysis saved to analysis_output.json")


if __name__ == "__main__":
    main()