import json
import os

from app.models import Evaluation
from app.models.evaluation import EvaluationRun
from app.services.evaluation_runner import EvaluationRunner
from app.utils.instructlab.instructlab_ragas import RagasEvaluator
from app.utils.storage import storage

MAX_TOKENS = 2048
TEMPERATURE = 0.00

class IlabEvaluationRunner(EvaluationRunner):
    def __init__(self, evaluation: Evaluation):
        super().__init__(evaluation)
        self.evaluation.ilab_evaluation = self.run

    def update_evaluation(self):
        self.evaluation.ilab_evaluation = self.run
        self.write_results()

    def grade_all_responses(self):
        self.run.status = "scoring responses"
        self.update_evaluation()

        evaluator = RagasEvaluator()

        for result in self.run.results:
            dataset = [score.dict() for score in result.scores]
            evaluation_result = evaluator.run(dataset=dataset)
            for i, score in enumerate(result.scores):
                score.score = evaluation_result.scores[i].get("domain_specific_rubrics")




