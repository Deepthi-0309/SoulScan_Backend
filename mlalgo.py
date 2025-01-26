# Linear Regression to predict the gad and phq 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def get_phq_severity(score):
    if score < 5:
        return "Minimal severity level"
    elif score < 10:
        return "Mild severity level"
    elif score < 15:
        return "Moderate severity level"
    else:
        return "Severe level"

def algo(number):
    phq_dataset = pd.read_csv('./datasets/phq.csv')

    user_phq_dataset = phq_dataset[phq_dataset['Score'] == number]

    phq_features = user_phq_dataset[['Score', 'Gender', 'Age', 'Employment Status', 'Relation Status']]
    phq_target = user_phq_dataset['Score']

    phq_features_encoded = pd.get_dummies(phq_features)

    X_phq_train, X_phq_test, y_phq_train, y_phq_test = train_test_split(phq_features_encoded, phq_target, test_size=0.2, random_state=42)

    phq_model = LinearRegression()

    phq_model.fit(X_phq_train, y_phq_train)

    next_phq_score = int(np.round(phq_model.predict(X_phq_test.iloc[-1:].values)[0]))

    actual_phq_score = y_phq_test.iloc[-1]

    predicted_phq_severity = get_phq_severity(next_phq_score)

    print(f"Predicted next PHQ-9 score for score {number} is:", next_phq_score, predicted_phq_severity)
    print("Actual Next PHQ-9 Score:", actual_phq_score)
    print("Prediction Accuracy (RMSE) for PHQ-9:", np.sqrt(mean_squared_error([actual_phq_score], [next_phq_score])))
    return {actual_phq_score , next_phq_score}




### *** python wont allow to import and export variables