import pandas as pd
import yaml
import os
import json
import re

from datetime import time

from app.models.evaluation import Evaluation, EvaluationRun, LlmConfig, Score, EvaluationResult
from app.services.evaluation_runner import EvaluationRunner
from app.utils.config import app_config, logger
from app.utils.storage import storage

from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import VLLMOpenAI

from instructlab.eval.evaluator import Evaluator

MAX_TOKENS = 2048
TEMPERATURE = 0.00


class OpenAIEvaluationRunner(EvaluationRunner):
    def __init__(self, evaluation: Evaluation):
        super().__init__(evaluation)
        self.evaluation.openai_evaluation = self.run
        self.judge_client = OpenAI(api_key=app_config["judge"]["api_key"])
        self.scoring_prompt = PromptTemplate.from_template(app_config["judge"]["template"])
        self.judge_model_name = app_config["judge"]["model_name"]

    def update_evaluation(self):
        self.evaluation.openai_evaluation = self.run
        self.write_results()

    def grade_all_responses(self):
        self.run.status = "scoring responses"
        self.update_evaluation()

        for result in self.run.results:
            for i, score in enumerate(result.scores):
                score.score, score.reasoning = self._score_request(
                    score.user_input,
                    score.response,
                    score.reference
                )


    def _score_request(self, question, answer, reference_answer):
        messages = [
            {
                "role": "user",
                "content": self.scoring_prompt.format(
                    question=question,
                    answer=answer,
                    reference_answer=reference_answer
                )
            }
        ]

        completion = self.judge_client.chat.completions.create(
            model=self.judge_model_name,
            messages=messages,
            n=1,
            temperature=0.0,
            max_tokens=1024,
        )

        response_content = completion.choices[0].message.content
        response_content = re.sub(r'^```json', '', response_content)
        response_content = re.sub(r'```$', '', response_content)

        try:
            result = json.loads(response_content)
        except Exception as e:
            result = {"answer_quality": 0, "reasoning": "Error"}
            logger.debug("response_content:", response_content)
            logger.error(f"An error occurred: {e}")

        score = result["answer_quality"]
        reasoning = result["reasoning"]
        return score, reasoning