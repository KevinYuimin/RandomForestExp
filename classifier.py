import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class RFClassifier:
    def __init__(self) -> None:
        self.randomForestModel = RandomForestClassifier(n_estimators=100, criterion = 'gini')
        self.load_data()
        self.train()
        self._test()

    def load_data(self, data_path='data.csv'):
        df_data = pd.read_csv(data_path)
        self. headers = list(df_data)
        x = df_data.drop(labels=['label'], axis=1).to_numpy()
        y = df_data['label'].to_numpy()
        self.x_train, self.x_test, self.y_train, self.y_test = \
            train_test_split(x, y, test_size=0.3, random_state=42, stratify=y)

    def update_data(self, new_data):
        self.x_train.append(new_data['env_data'])
        self.y_train.append(new_data['result'])

    def train(self):
        self.randomForestModel.fit(self.x_train, self.y_train)

    def _test(self):
        print('testing: ',self.randomForestModel.score(self.x_test, self.y_test))
        
    def inference(self, input_data):
        return self.randomForestModel.predict(input_data)