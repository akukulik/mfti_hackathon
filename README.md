# Проектный практикум МФТИ - Детекция признаков депрессии по постам в социальных сетях
##### О проекте
Проект выполнила команда 8:
- Артамонов Олег
- Кулик Анастасия
- Семерня Элина

Репозиторий содержит код реализации телеграм-бота для детекции признаков депрессии в тексте. 
Также в репозитории хранится IPYNB-файл для упрощенного доступа к модели.

##### Требования

python 3.8+
transformers 4.13.0
simpletransformers 0.63.7
pandas 1.2.5
scikit-learn 0.23.1
tqdm 4.62.3
fastapi
uvicorn
torch
transformers

Prepared datasets

We prepared two datasets. The first is a preprocessed dataset provided by the competition organizers. The second, Reddit Depression Corpora, was used to train the DepRoBERTa language model.

Preprocessed competition dataset

Dataset was prepared by removing duplicates and transfer some examples from the dev set to the train set. Files are available in the ./data/preprocessed_dataset folder.

Reddit Depression Corpora

We built a corpus based on the Reddit Mental Health Dataset (Low et al., 2020) and a dataset of 20,000 posts from r/depression and r/SuicideWatch subreddits. We filtered the data appropriately, leaving mainly those related to depression (31,2%), anxiety (20,5%) and suicide (18.1%), which resulted in a corpora consisting of 396,968 posts.

Trained models

DepRoBERTa

DepRoBERTa (RoBERTa for Depression Detection) - language model based on RoBERTa-large and further pre-trained on the Reddit Depression Corpora.

rafalposwiata/deproberta-large-v1

Models for detecting depression

rafalposwiata/roberta-large-depression

rafalposwiata/deproberta-large-depression


