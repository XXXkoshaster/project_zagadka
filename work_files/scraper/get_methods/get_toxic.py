import re

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class Toxic:
    """
    Класс для определения токсичности текстов с использованием модели 'cointegrated/rubert-tiny-toxicity'.

    Attributes
    ----------
    tokinizer : transformers.AutoTokenizer
        Токенизатор, используемый для преобразования текста в тензоры.
    model : transformers.AutoModelForSequenceClassification
        Модель для классификации текстов на токсичность.

    Methods
    -------
    text_toxicity(text, aggregate=False)
        Определяет вероятность токсичности для заданного текста.
    process_set(wall)
        Обрабатывает список постов и возвращает DataFrame с текстами постов.
    apply_toxicity(row)
        Применяет модель токсичности к строке DataFrame.
    toxicity_info(wall)
        Возвращает среднюю вероятность различных типов токсичности для списка постов.
    """

    def __init__(self):
        """
        Инициализирует токенизатор и модель для определения токсичности текстов.
        """
        MODEL = "cointegrated/rubert-tiny-toxicity"
        self.tokinizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    def text_toxicity(self, text, aggregate=False):
        """
        Определяет вероятность токсичности для заданного текста.

        Parameters
        ----------
        text : str or list of str
            Текст или список текстов для анализа токсичности.
        aggregate : bool, optional
            Если True, возвращает агрегированную вероятность токсичности, по умолчанию False.

        Returns
        -------
        numpy.ndarray or float
            Вероятность каждого типа токсичности для каждого текста или агрегированная вероятность токсичности.
        """
        with torch.no_grad():
            inputs = self.tokinizer(
                text, return_tensors="pt", truncation=True, padding=True
            ).to(self.model.device)
            proba = torch.sigmoid(self.model(**inputs).logits).cpu().numpy()
        if isinstance(text, str):
            proba = proba[0]
        if aggregate:
            return 1 - proba.T[0] * (1 - proba.T[-1])
        return proba

    def process_set(self, wall):
        """
        Обрабатывает список постов и возвращает DataFrame с текстами постов.

        Parameters
        ----------
        wall : list of dict
            Список словарей, где каждый словарь представляет собой пост на стене пользователя.
            Каждый пост должен содержать ключ 'text' или 'copy_history'.

        Returns
        -------
        pd.DataFrame
            DataFrame с одним столбцом 'Text', содержащим обработанные тексты постов.
        """
        posts = pd.DataFrame(columns=["Text"])

        for i in wall:
            if text := i["text"]:
                text = re.sub(r"[\n\t]", " ", text)
                posts.loc[len(posts.index)] = re.sub(r"[^\w\s]", "", text)
            elif ("copy_history" in i) and (text := i["copy_history"][0]["text"]):
                text = re.sub(r"[\n\t]", " ", text)
                posts.loc[len(posts.index)] = re.sub(r"[^\w\s]", "", text)

        return posts

    def apply_toxicity(self, row):
        """
        Применяет модель токсичности к строке DataFrame.

        Parameters
        ----------
        row : pd.Series
            Строка DataFrame, содержащая текст поста.

        Returns
        -------
        pd.Series
            Строка DataFrame с добавленными вероятностями токсичности.
        """
        proba = self.text_toxicity(row["Text"])
        row["Non-toxic"] = proba[0]
        row["Insult"] = proba[1]
        row["Obscenity"] = proba[2]
        row["Threat"] = proba[3]
        row["Dangerous"] = proba[4]
        return row

    def toxicity_info(self, wall):
        """
        Возвращает среднюю вероятность различных типов токсичности для списка постов.

        Parameters
        ----------
        wall : list of dict
            Список словарей, где каждый словарь представляет собой пост на стене пользователя.

        Returns
        -------
        pd.DataFrame
            DataFrame с вероятностями различных типов токсичности.
        """
        posts = self.process_set(wall)

        posts["Non-toxic"] = 0
        posts["Insult"] = 0
        posts["Obscenity"] = 0
        posts["Threat"] = 0
        posts["Dangerous"] = 0

        posts = posts.apply(self.apply_toxicity, axis=1)

        return pd.DataFrame(
            posts[["Non-toxic", "Insult", "Obscenity", "Threat", "Dangerous"]].mean(),
            columns=["Probability"],
        )
