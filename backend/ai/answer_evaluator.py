import json

from backend.ai.openai_client import client


def evaluate_answer(question, answer):
    prompt = f"""
You are an expert technical interview evaluator.

Evaluate the candidate's answer to the interview question.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer using these criteria:

1. Relevance:
How directly does the answer address the question?

2. Correctness:
Are the concepts and statements technically correct?

3. Completeness:
Does the answer adequately cover the important aspects expected for the question?

4. Technical Accuracy:
Are the technical details, terminology, reasoning, and examples accurate?

5. Overall Score:
Give an overall score from 0 to 100 based on the quality of the answer.

Provide concise, constructive feedback.
Also identify the candidate's strengths and areas for improvement.

Do not give credit merely because the answer contains keywords.
Evaluate the actual meaning and quality of the response.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "answer_evaluation",
                "description": "Structured technical interview answer evaluation.",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "relevance_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "correctness_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "completeness_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "technical_accuracy_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "overall_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "feedback": {
                            "type": "string"
                        },
                        "strengths": {
                            "type": "string"
                        },
                        "areas_for_improvement": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "relevance_score",
                        "correctness_score",
                        "completeness_score",
                        "technical_accuracy_score",
                        "overall_score",
                        "feedback",
                        "strengths",
                        "areas_for_improvement"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)