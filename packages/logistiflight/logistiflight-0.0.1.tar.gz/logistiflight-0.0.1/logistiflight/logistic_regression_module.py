import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from mord import LogisticIT
import matplotlib.pyplot as plt
import seaborn as sns
from dmba import classificationSummary, gainsChart, liftChart
from dmba.metric import AIC_score


def preprocess_universal_bank_data(file_path):
    bank_df = pd.read_csv(file_path)
    bank_df.drop(columns=['ID', 'ZIP Code'], inplace=True)
    bank_df.columns = [c.replace(' ', '_') for c in bank_df.columns]

    bank_df['Education'] = bank_df['Education'].astype('category')
    new_categories = {1: 'Undergrad', 2: 'Graduate', 3: 'Advanced/Professional'}
    bank_df.Education.cat.rename_categories(new_categories, inplace=True)
    bank_df = pd.get_dummies(bank_df, prefix_sep='_', drop_first=True)

    y = bank_df['Personal_Loan']
    X = bank_df.drop(columns=['Personal_Loan'])
    
    return train_test_split(X, y, test_size=0.4, random_state=1)

def logistic_regression(train_X, train_y, valid_X, valid_y):
    logit_reg = LogisticRegression(penalty="l2", C=1e42, solver='liblinear')
    logit_reg.fit(train_X, train_y)

    intercept = logit_reg.intercept_[0]
    coefficients = pd.DataFrame({'coeff': logit_reg.coef_[0]}, index=train_X.columns).transpose()

    logit_reg_pred = logit_reg.predict(valid_X)
    logit_reg_proba = logit_reg.predict_proba(valid_X)
    logit_result = pd.DataFrame({
        'actual': valid_y,
        'p(0)': [p[0] for p in logit_reg_proba],
        'p(1)': [p[1] for p in logit_reg_proba],
        'predicted': logit_reg_pred
    })

    return intercept, coefficients, logit_result

def nominal_logistic_regression(data_file, outcome, predictors):
    data = pd.read_csv(data_file)
    y = data[outcome]
    X = data[predictors]
    logit = LogisticRegression(penalty="l2", solver='lbfgs', C=1e24, multi_class='multinomial')
    logit.fit(X, y)

    intercept = logit.intercept_
    coefficients = logit.coef_
    probs = logit.predict_proba(X)
    results = pd.DataFrame({
        'actual': y,
        'predicted': logit.predict(X),
        'P(0)': [p[0] for p in probs],
        'P(1)': [p[1] for p in probs],
        'P(2)': [p[2] for p in probs]
    })

    return intercept, coefficients, results

def ordinal_logistic_regression(data_file, outcome, predictors):
    data = pd.read_csv(data_file)
    y = data[outcome]
    X = data[predictors]
    logit = LogisticIT(alpha=0)
    logit.fit(X, y)

    theta = logit.theta_
    coefficients = logit.coef_
    probs = logit.predict_proba(X)
    results = pd.DataFrame({
        'actual': y,
        'predicted': logit.predict(X),
        'P(0)': [p[0] for p in probs],
        'P(1)': [p[1] for p in probs],
        'P(2)': [p[2] for p in probs]
    })

    return theta, coefficients, results

def plot_charts(df):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    gainsChart(df.actual, ax=axes[0])
    liftChart(df.actual, title=False, ax=axes[1])
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    pass