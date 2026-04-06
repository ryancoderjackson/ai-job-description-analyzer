# AI Job Description Analyzer

An AI-powered CLI tool that analyzes job descriptions and compares resumes against job requirements to generate match scores, skill-gap analysis, and tailored resume suggestions.

## Features
- Extracts likely job title
- Estimates seniority level
- Identifies required and preferred skills
- Summarizes key responsibilities
- Generates fit assessment
- Suggests resume improvements

## Version 2 Features
- Compare resume text against a job description
- Generate a match score from 0 to 100
- Identify strengths and missing skills
- Produce tailored resume improvement suggestions
- Save structured output to JSON

## Tech Stack
- Python
- OpenAI API
- python-dotenv

## How to Run
1. Create a virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Create a `.env` file with:
   OPENAI_API_KEY=your_api_key_here
4. Run:
   python main.py

## Notes
This is version 1 of the project. Future versions will include:
- cleaner output formatting
- resume-to-job matching
- portfolio-ready improvements

## Sample Output

```json
{
  "job_title_guess": "AI Engineer - Autonomous Agents",
  "seniority_level": "Mid to Senior",
  "required_skills": [
    "Prompt engineering",
    "LLM integration",
    "RAG systems"
  ],
  "resume_suggestions": [
    "Highlight AI agent experience",
    "Showcase prompt engineering projects"
  ]
}