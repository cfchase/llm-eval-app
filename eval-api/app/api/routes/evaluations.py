from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.utils.config import logger
from app.utils.storage import storage

from ...dependencies import get_token_header
from ...models import Evaluation
from ...services import OpenAIEvaluationRunner, IlabEvaluationRunner

router = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("")
@router.get("/")
async def read_evaluations():
    files = storage.list_files("", "**", recursive=True)
    return files


def run_open_ai_evaluation(evaluation: Evaluation):
    logger.info(f"Running OpenAI evaluation for {evaluation.id}")
    openai_evaluation = OpenAIEvaluationRunner(evaluation)
    openai_evaluation.evaluate()
    logger.info(f"Finished OpenAI evaluation for {evaluation.id}")

def run_ilab_evaluation(evaluation: Evaluation):
    logger.info(f"Running ilab evaluation for {evaluation.id}")
    ilab_evaluation = IlabEvaluationRunner(evaluation)
    ilab_evaluation.evaluate()
    logger.info(f"Finished ilab evaluation for {evaluation.id}")

@router.post("")
@router.post("/")
async def create_evaluation(evaluation_in: Evaluation, background_tasks: BackgroundTasks) -> Evaluation:
    evaluation_in.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    logger.info(f"Creating evaluation {evaluation_in.id}")
    evaluation = Evaluation.model_validate(evaluation_in)
    storage.make_dirs(f"{evaluation_in.id}")
    storage.write_json(evaluation.model_dump(), f"{evaluation.id}/evaluation.json", )
    background_tasks.add_task(run_ilab_evaluation, evaluation)
    background_tasks.add_task(run_open_ai_evaluation, evaluation)
    return evaluation


@router.get("/{evaluation_id}")
async def read_evaluation(evaluation_id: str):
    evaluation = storage.read_json(f"{evaluation_id}/evaluation.json", )

    return evaluation
