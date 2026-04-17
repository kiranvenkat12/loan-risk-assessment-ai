from fastapi import FastAPI
from schemas.Schemas import InputData
from service.Service import predict

app = FastAPI()


@app.post("/predict")
def get_prediction(data: InputData):
    result = predict(data.dict())
    return {"prediction": result}