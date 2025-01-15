from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LlmConfig(BaseModel):
    name: str
    model_type: str = "vllm"
    endpoint_url: str = ""
    model_name: str
    api_key: str = ""
    rag: bool = False
    template: str


class ReferenceAnswer(BaseModel):
    user_input: str
    reference: str
    retrieved_context: str


class ReferenceAnswer(BaseModel):
    user_input: str
    reference: str
    retrieved_context: str


class Score(BaseModel):
    user_input: str
    reference: str
    retrieved_context: str | None = None
    response: str | None = None
    score: int | None = None
    reasoning: str | None = None


class EvaluationResult(BaseModel):
    name: str
    scores: List[Score] = Field(default_factory=list)


class EvaluationRun(BaseModel):
    status: str = "new"
    results: List[EvaluationResult] = Field(default_factory=list)


class Evaluation(BaseModel):
    id: str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    endpoint_url: str = None
    model_name: str = None
    api_key: str = None
    reference_answers: List[ReferenceAnswer] = Field(default_factory=list)
    openai_evaluation: EvaluationRun = EvaluationRun()
    ilab_evaluation: EvaluationRun = EvaluationRun()

