from backend.ai.openai_client import client


def generate_questions(skills, domain, difficulty, count=5):
    if not skills:
        skills_text = "General software engineering concepts"
    else:
        skills_text = ", ".join(skills)

    prompt = f"""
You are an expert technical interviewer.

Generate {count} technical interview questions for a candidate.

Candidate skills:
{skills_text}

Target interview domain:
{domain}

Difficulty:
{difficulty}

Requirements:
- Questions must be relevant to the candidate's skills and the selected domain.
- Questions should test actual understanding, not simple memorization.
- Avoid duplicate or nearly identical questions.
- Match the requested difficulty.
- Questions should be suitable for a real technical interview.
- Do not provide answers.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "interview_questions",
                "description": "Structured technical interview questions.",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["questions"],
                    "additionalProperties": False
                }
            }
        }
    )

    import json

    result = json.loads(response.output_text)

    return result["questions"]