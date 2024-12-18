# Проектный практикум МФТИ - Детекция признаков депрессии по постам в социальных сетях
# Telegram Bot for Detecting Signs of Depression in Text

### О проекте

Проект разработан **командой 8**:  
- Артамонов Олег  
- Кулик Анастасия  
- Семерня Элина  

Этот репозиторий содержит код для реализации телеграм-бота, который способен определять признаки депрессии в текстах. Также в репозитории представлен IPYNB-файл для упрощённого доступа к модели.

Для анализа текста используется предобученная модель [deproberta-large-depression](https://huggingface.co/rafalposwiata/deproberta-large-depression), классифицирующая текст на три категории:  
- "Нет депрессии"  
- "Умеренная депрессия"  
- "Сильная депрессия"  

Модель обрабатывает текст на английском языке. Для работы с русскими текстами применяется сервис машинного перевода [Yandex Translate](https://yandex.cloud/ru/services/translate).

Мы реализовали удобный интерфейс взаимодействия через [телеграм-бота @hackathon_mfti_bot](https://t.me/hackathon_mfti_bot).  
Бот принимает текст на русском языке и возвращает:  
- Возможный уровень депрессии  
- F1-скор модели  

---

### Требования

Для работы с проектом установите следующие зависимости:  
```bash
python 3.8+
transformers
simpletransformers
pandas
scikit-learn
tqdm
fastapi
uvicorn
torch
httpx
aiogram
python-dotenv
requests
```


### Быстрый старт
- Для простого запуска модели скачайте deroberta_depression_russian_text.ipynb на личном ПК или в Google collab.
- Установите все необходимые пакеты
- Зарегистрируйтесь в Yandex Translate (https://yandex.cloud/ru/services/translate) и получите токен для доступа к машинному переводу

### Разворачивание телеграм-бота
Для разворачивания телеграм-бота выполните следующую инструкцию:
- Установите Докер (https://www.docker.com/get-started)
- Создайте свой Телеграм-бот @BotFather
- Клонируйте репозиторий
- Настройте переменные окружения в файле .env.example
- Постройте Докер-образ docker build -t имя_образа .
- Запустите контейнер docker run -d --name имя_контейнера имя_образа

Вы пострясающие! 


### Модели
- rafalposwiata/deproberta-large-depression

### Датасеты
- Модель deproberta-large-depression обучалась на корпусе данных Reddit Depression Corpora (https://zenodo.org/records/3941387#.Y5L6O_fMKUl), основанном на 396 968 постов Реддита.








