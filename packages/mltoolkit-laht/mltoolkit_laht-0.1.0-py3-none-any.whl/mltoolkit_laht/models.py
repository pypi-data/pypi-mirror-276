from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

class Model:
    def __init__(self, model_type='logistic_regression'):
        if model_type == 'logistic_regression':
            self.model = LogisticRegression()
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier()
        else:
            raise ValueError("Invalid model type. Expected 'logistic_regression' or 'random_forest'.")

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)