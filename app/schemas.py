from typing import List
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str

class AnswerRequest(BaseModel):
    answer: str
    references: List[str]