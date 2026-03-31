import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)


def analyze_job_description(job_description: str) -> dict:
    prompt = f"""
You are a career assistant. Analyze the following job description and return JSON only.

Return this exact structure:
{{
  "job_title_guess": "",
  "seniority_level": "",
  "required_skills": [],
  "preferred_skills": [],
  "key_responsibilities": [],
  "fit_assessment": "",
  "resume_suggestions": []
}}

Job description:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{content}")


def save_analysis(result: dict, filename: str = "analysis_output.json") -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)


def main() -> None:
    print("Paste the job description below. Type END on a new line when finished.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    job_description = "\n".join(lines).strip()

    if not job_description:
        print("No job description provided.")
        return

    print("\nAnalyzing...\n")
    result = analyze_job_description(job_description)

    print(json.dumps(result, indent=2))
    save_analysis(result)
    print("\nAnalysis saved to analysis_output.json")


if __name__ == "__main__":
    main()