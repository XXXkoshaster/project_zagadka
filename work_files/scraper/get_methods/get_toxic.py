import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
import pandas as pd

class Toxic:
    def __init__(self):
        MODEL = 'cointegrated/rubert-tiny-toxicity'
        self.tokinizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)     
    
    def text_toxicity(self, text, aggregate=False):
        with torch.no_grad():
            inputs = self.tokinizer(text, return_tensors='pt', truncation=True, padding=True).to(self.model.device)
            proba = torch.sigmoid(self.model(**inputs).logits).cpu().numpy()
        if isinstance(text, str):
            proba = proba[0]
        if aggregate:
            return 1 - proba.T[0] * (1 - proba.T[-1])
        return proba
    
    def process_set(self, wall):
        posts = pd.DataFrame(columns=["Text"])

        for i in wall:
            if (text := i["text"]):
                text = re.sub(r"[\n\t]", ' ', text)
                posts.loc[len(posts.index)] = re.sub(r"[^\w\s]", '', text)
            elif ("copy_history" in i) and (text := i["copy_history"][0]["text"]):
                text = re.sub(r"[\n\t]", ' ', text)
                posts.loc[len(posts.index)] = re.sub(r"[^\w\s]", '', text)

        return posts
    
    def apply_toxicity(self, row):
        proba = self.text_toxicity(row['Text'])
        row['Non-toxic'] = proba[0]
        row['Insult'] = proba[1]
        row['Obscenity'] = proba[2]
        row['Threat'] = proba[3]
        row['Dangerous'] = proba[4]
        return row
    
    
    def toxicity_info(self, wall):
        posts = self.process_set(wall)
        
        posts['Non-toxic'] = 0
        posts['Insult'] = 0
        posts['Obscenity'] = 0
        posts['Threat'] = 0
        posts['Dangerous'] = 0

        posts = posts.apply(self.apply_toxicity, axis=1)

        return pd.DataFrame(posts[['Non-toxic', 'Insult', 'Obscenity', 'Threat', 'Dangerous']].mean(), columns=["Probility"])
