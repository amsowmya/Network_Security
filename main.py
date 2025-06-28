import os 
import sys 
import pandas as pd 

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run 
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import ModelResolver
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR
from networksecurity.utils.main_utils.utils import load_object

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./temolates")


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.") 
        
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        # print(df.head())
        model = ModelResolver(model_dir=SAVED_MODEL_DIR)
        latest_model_path = model.get_best_model_path()
        latest_model = load_object(file_path=latest_model_path)
        
        y_pred = latest_model.predict(df)
        df['predicted_column'] = y_pred 
        df['predicted_column'].replace(-1, 0)
        # return df.to_json()
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
         
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)