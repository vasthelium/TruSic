from sklearn.model_selection import train_test_split #function takes full dataset and splits
from sklearn.preprocessing import StandardScaler #class for scaling stats from training data
from sklearn.linear_model import LinearRegression #this is a regression model
from sklearn.ensemble import RandomForestClassifier #class - object created from it learns(fit) and predicts
from app.services.H5_trigger_states import mlpfunc, numerical_features
import numpy as np
import random

# ==== Scikit learn will be used to =====
# 	1.	Use Random Forest → quick learning baseline
# 	2.	Use Train/Test → validate behavior
# 	3.	Use Feature Importance → improve system design

def dataextract_sk():
    raw_numerics = numerical_features()
    X = mlpfunc(raw_numerics) #this is our x

    """below is our y"""
    y = []

    for samples in X:
        duration = random.randint(0,200)
        if duration < 10:
            y_skip = 0
        elif duration < 30:
            y_skip = 1
        elif duration < 120:
            y_skip = 2
        else:
            y_skip = 3
        y.append(y_skip)
    return X, y

X, y = dataextract_sk()

X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = np.mean(y_pred == y_test) 

feature_importance = model.feature_importances_
print(feature_importance)

 

