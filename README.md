# AI Job Description Analyzer

A Python CLI tool that uses the OpenAI API to analyze job descriptions and return structured JSON output.

## Features
- Extracts likely job title
- Estimates seniority level
- Identifies required and preferred skills
- Summarizes key responsibilities
- Generates fit assessment
- Suggests resume improvements

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