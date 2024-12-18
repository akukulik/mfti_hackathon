from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import pipeline

app = FastAPI()

model = pipeline(
    'text-classification',
    'rafalposwiata/deproberta-large-depression',
    device='cuda' if torch.cuda.is_available() else 'cpu',
)


class PredictionRequest(BaseModel):
    text: str


@app.post("/predict")
async def predict(request: PredictionRequest):
    result = model(request.text)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
