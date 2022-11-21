import sys
import time
import pathlib
import uvicorn

base_dir = pathlib.Path(__file__).parent.absolute().parent
print("base dir: ", base_dir)
sys.path.append(str(base_dir))

from utils.Logger import Logger
from config.common_config import options
from api_models import ScoringRequestData
from fastapi import FastAPI, Response, status
from models.ModelHandler import ModelController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
logger = Logger(log_file_name="api.logs").create_time_rotating_log(when="day", backup_count=7)

model_controller = ModelController(model_name=options["model_to_use"], logger=logger)
scoring_model = model_controller.get_model()


@app.post("/lead_scoring/score_data")
def score_data(response: Response, data: ScoringRequestData):
    logger.info("got request to score data")
    start = time.time()

    try:
        data_to_score = dict(data)
        logger.info(f"data to score is : {data_to_score}")
        lead_scores = scoring_model.predict_score(data_to_score)
        response.status_code = status.HTTP_200_OK
        logger.info(f"got scores: {lead_scores}")
        return {"score": lead_scores[-1]}

    except Exception:
        logger.exception("Got exception while trying to score data: ")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {}

    finally:
        end = time.time()
        logger.info(f"took {end - start} secs for lead scoring")
        logger.info("*" * 100)
        logger.info("\n")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run('api:app', host=options['api_host'], port=options['api_port'], reload=False,
                workers=options["api_workers"])
