from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.Schemas import InputData
from service.Service import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "ML API is running"}

@app.post("/predict")
def get_prediction(data: InputData):
    input_dict = data.dict()
    result = predict(input_dict)
    return {"prediction": result}