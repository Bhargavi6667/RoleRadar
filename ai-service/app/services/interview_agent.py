import json
import uuid
from typing import Dict, Any, List
from openai import OpenAI
from app.config import settings
from app.schemas.interview import InterviewQuestion, InterviewEvaluation

class InterviewAgent:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.client = None
        if self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None

    def start_interview(self, resume_text: str, job_description: str, topics: List[str] = None) -> InterviewQuestion:
        """Generate the first adaptive question tailored to the candidate's resume and job requirements."""
        if self.client:
            prompt = f"""You are an adaptive senior technical interviewer at CareerLens AI.
Generate the FIRST interview question tailored specifically to the candidate's resume and target job.

RULES:
- Anchor the question in a specific project or technology claimed in the resume.
- Avoid generic trivia like "What is Java?". Ask applied, architectural, or implementation questions.
- Return ONLY valid JSON:
{{
  "question_id": "{str(uuid.uuid4())[:8]}",
  "topic": "Topic Name",
  "question": "Question text...",
  "context": "Context from resume...",
  "difficulty": "Medium"
}}

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{job_description[:2000]}
"""
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert technical interviewer. Return JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                data = json.loads(response.choices[0].message.content)
                return InterviewQuestion(**data)
            except Exception as e:
                print(f"LLM start_interview failed: {e}. Using fallback.")

        # Fallback first question
        topic = topics[0] if (topics and len(topics) > 0) else "Spring Boot & REST APIs"
        return InterviewQuestion(
            question_id=str(uuid.uuid4())[:8],
            topic=topic,
            question=f"In your project experience, how did you design and secure your REST APIs using {topic}? Walk me through your request lifecycle and authentication mechanism.",
            context="Based on your resume experience building full-stack applications.",
            difficulty="Medium"
        )

    def evaluate_and_next(
        self,
        question: str,
        answer: str,
        resume_context: str = "",
        job_context: str = "",
        history: List[Dict[str, Any]] = None
    ) -> InterviewEvaluation:
        """Evaluate the candidate's answer and generate the next adaptive follow-up or new topic question."""
        if self.client:
            prompt = f"""You are an adaptive technical interviewer.
Evaluate the candidate's answer to the previous question and formulate the NEXT question.

ADAPTIVE RULES:
- If the answer was strong, acknowledge what was good and increase depth (e.g. edge cases, performance, failure handling).
- If the answer was weak or missed critical concepts, ask a targeted follow-up to give them a chance to clarify.
- If the topic is sufficiently covered, transition smoothly to another required job skill.

PREVIOUS QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Return ONLY valid JSON matching this schema:
{{
  "evaluation": "Clear evaluation paragraph explaining how well the candidate answered...",
  "score": 8.5,
  "strengths": ["Clear explanation of token validation", "Good architectural awareness"],
  "areas_for_improvement": ["Did not mention token expiry or refresh strategies"],
  "follow_up_question": "Optional immediate follow-up if clarification is needed",
  "next_question": {{
    "question_id": "{str(uuid.uuid4())[:8]}",
    "topic": "Database Concurrency / Microservices",
    "question": "Next interview question...",
    "context": "Context for the question",
    "difficulty": "Medium"
  }}
}}
"""
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are CareerLens AI technical evaluator. Return strict JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                data = json.loads(response.choices[0].message.content)
                return InterviewEvaluation(**data)
            except Exception as e:
                print(f"LLM evaluate_and_next failed: {e}. Using fallback.")

        # Fallback adaptive evaluation
        ans_len = len(answer.strip())
        score = 8.5 if ans_len > 120 else (7.0 if ans_len > 40 else 5.0)

        strengths = ["Structured thought process", "Directly addressed the core question"]
        areas = ["Could elaborate more on error handling, scale, and performance trade-offs"]

        next_q = InterviewQuestion(
            question_id=str(uuid.uuid4())[:8],
            topic="Database & System Design",
            question="Suppose your application experiences a sudden 10x traffic spike on the API endpoints. How would you diagnose bottlenecks across the database connection pool and application layer?",
            context="Assessing system resilience and operational troubleshooting.",
            difficulty="Hard" if score >= 8.0 else "Medium"
        )

        return InterviewEvaluation(
            evaluation=f"Good practical answer demonstrating core understanding. With a score of {score}/10, you showed familiarity with the pattern.",
            score=score,
            strengths=strengths,
            areas_for_improvement=areas,
            follow_up_question="How would you handle token invalidation upon user logout?",
            next_question=next_q
        )

interview_agent = InterviewAgent()
