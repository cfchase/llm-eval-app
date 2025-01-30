from abc import abstractmethod

from datetime import time

from app.models.evaluation import Evaluation, EvaluationRun, LlmConfig, Score, EvaluationResult
from app.utils.config import app_config, logger
from app.utils.storage import storage

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import VLLMOpenAI

MAX_TOKENS = 2048
TEMPERATURE = 0.00

class EvaluationRunner:
    def __init__(self, evaluation: Evaluation):
        self.evaluation = evaluation
        self.run = EvaluationRun(status="pending")


    def generate_all_responses(self):
        logger.info("generate_responses")
        self.run.status = "generating responses"
        self.run.results = []
        self.write_results()

        testing_config = LlmConfig.model_validate(app_config["testing_config"])
        testing_config.endpoint_url = self.evaluation.endpoint_url
        testing_config.model_name = self.evaluation.model_name
        testing_config.api_key = self.evaluation.api_key

        result = EvaluationResult(name=testing_config.name)
        result.scores = self._generate_responses(testing_config)
        self.run.results.append(result)

        rag_testing_config = LlmConfig.model_validate(app_config["rag_testing_config"])
        rag_testing_config.endpoint_url = self.evaluation.endpoint_url
        rag_testing_config.model_name = self.evaluation.model_name
        rag_testing_config.api_key = self.evaluation.api_key

        result = EvaluationResult(name=rag_testing_config.name)
        result.scores = self._generate_responses(rag_testing_config)
        self.run.results.append(result)

        for llm_config_dict in app_config["comparison_configs"]:
            llm_config = LlmConfig.model_validate(llm_config_dict)
            result = EvaluationResult(name=llm_config.name)
            result.scores = self._generate_responses(llm_config)
            self.run.results.append(result)


    @abstractmethod
    def grade_all_responses(self):
        pass

    @abstractmethod
    def update_evaluation(self):
        pass

    def write_results(self):
        logger.info("write_results")
        storage.write_json(self.evaluation.model_dump(exclude={"api_key"}), f"{self.evaluation.id}/evaluation.json")


    def evaluate(self):
        logger.info("evaluate")
        self.generate_all_responses()
        self.grade_all_responses()
        self.run.status = "complete"
        self.write_results()


    def _create_llm(self, llm_config: LlmConfig) -> ChatOpenAI | VLLMOpenAI:
        if llm_config.model_type == "openai":
            # logger.info("Creating OpenAI model")
            return ChatOpenAI(
                openai_api_key=llm_config.api_key,
                model_name=llm_config.model_name,
                streaming=False)
        return VLLMOpenAI(
            openai_api_key=llm_config.api_key,
            openai_api_base=llm_config.endpoint_url,
            model_name=llm_config.model_name,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            streaming=False
        )


    def _get_response(self, llm, template_str, question, context=None) -> str:
        num_retries = 1
        for attempt in range(num_retries):
            try:
                prompt = PromptTemplate.from_template(template_str)
                chain = prompt | llm | StrOutputParser()
                params = {"question": question}
                if context:
                    params["context"] = context
                answer = chain.invoke(params)
                return answer.strip()
            except Exception as e:
                logger.error(f"Request failed: {e}")
                if attempt + 1 < num_retries:
                    logger.info(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    return ""


    def _generate_responses(self, llm_config: LlmConfig) -> list[Score]:
        scores = []
        llm = self._create_llm(llm_config)
        # index = 0
        for reference_answer in self.evaluation.reference_answers:
            score = Score(
                user_input=reference_answer.user_input,
                reference=reference_answer.reference
            )
            if llm_config.rag:
                score.retrieved_context = reference_answer.retrieved_context
            else:
                score.retrieved_context = None
            score.response = self._get_response(
                llm,
                llm_config.template,
                score.user_input,
                score.retrieved_context
            )
            # index += 1
            # score.response = f"Answer to question {index}"
            scores.append(score)
        return scores


