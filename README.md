# Проектный практикум МФТИ - Детекция признаков депрессии по постам в социальных сетях
### О проекте
Проект выполнила команда 8:
- Артамонов Олег
- Кулик Анастасия
- Семерня Элина

Репозиторий содержит код реализации телеграм-бота для детекции признаков депрессии в тексте. 
Также в репозитории хранится IPYNB-файл для упрощенного доступа к модели.

Для создания продукта мы использовали предобученную модель deproberta-large-depression (https://huggingface.co/rafalposwiata/deproberta-large-depression), которая решает задачу детекции уровня депрессии в разрезе трех классов - "нет депрессии", "умеренная депрессия" и "сильная депрессия". Модель работает с текстом на английском языке, поэтому для обработки текстов на русском языке мы используем сервис машинного перевода Yandex Translate (https://yandex.cloud/ru/services/translate). В качестве интерфейса взаимодействия мы развернули телеграм-бот @hackathon_mfti_bot, который принимает на вдох текст на русском языке и возвращает возможную степень депрессии и F1-скор

### Требования

- python 3.8+
- transformers
- simpletransformers
- pandas
- scikit-learn
- tqdm
- fastapi
- uvicorn
- torch
- httpx
- aiogram
- python-dotenv
- requests


### Быстрый старт 
### Разворачивание телеграм-бота
### Модели
### Датасеты


We prepared two datasets. The first is a preprocessed dataset provided by the competition organizers. The second, Reddit Depression Corpora, was used to train the DepRoBERTa language model.

Preprocessed competition dataset

Dataset was prepared by removing duplicates and transfer some examples from the dev set to the train set. Files are available in the ./data/preprocessed_dataset folder.

Reddit Depression Corpora: https://zenodo.org/records/3941387#.Y5L6O_fMKUl

We built a corpus based on the Reddit Mental Health Dataset (Low et al., 2020) and a dataset of 20,000 posts from r/depression and r/SuicideWatch subreddits. We filtered the data appropriately, leaving mainly those related to depression (31,2%), anxiety (20,5%) and suicide (18.1%), which resulted in a corpora consisting of 396,968 posts.

Trained models

DepRoBERTa

DepRoBERTa (RoBERTa for Depression Detection) - language model based on RoBERTa-large and further pre-trained on the Reddit Depression Corpora.

rafalposwiata/deproberta-large-v1

Models for detecting depression

rafalposwiata/roberta-large-depression

rafalposwiata/deproberta-large-depression


