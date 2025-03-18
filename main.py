from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from etl import run_etl
from model import train_model, predict_coursecompletion
from database import insert_raw_data, get_raw_data


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.post("/upload-data")
async def upload_data(input_data: list[dict]):
    insert_raw_data(input_data)
    return {"message": "Raw data uploaded successfully!"}

@app.post("/run_etl")
async def run_rtl_process():
    return run_etl()

@app.post('/train_model')
async def training_model():
    train_model()
    return {"message":"model trained successfully"}

@app.post('/predict_model')
async def predicting_model(input_data: dict):
    return predict_coursecompletion(input_data)