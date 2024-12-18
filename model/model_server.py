from fastapi import FastAPI # для создания веб-приложения
from pydantic import BaseModel # для валидации данных запросов
import torch  # для работы с нейросетями
from transformers import pipeline   # для работы с предобученными моделями

# Инициализация FastAPI-приложения
app = FastAPI()


# Настройка предобученной модели для классификации текста по степени депрессивности
# Используется модель deproberta-large-depression из библиотеки Hugging Face.
# Устройство выбирается автоматически: GPU (если доступно) или CPU.
model = pipeline(
    'text-classification',
    'rafalposwiata/deproberta-large-depression',
    device='cuda' if torch.cuda.is_available() else 'cpu',
)


# Ожидается, что запрос содержит поле "text", которое должно быть строкой.
class PredictionRequest(BaseModel):
    text: str


# Принимает запрос с текстом, обрабатывает его моделью и возвращает результат.
@app.post("/predict")
async def predict(request: PredictionRequest):
    result = model(request.text)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn # сервер для запуска приложения
    uvicorn.run(app, host="0.0.0.0", port=8000) # запуск приложения на порту 8000
