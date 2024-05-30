import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split
from dmba import classificationSummary, gainsChart
from dmba.metric import AIC_score

__version__ = '0.0.1'

__all__ = [
    'load_and_preprocess_data', 
    'createGraph', 
    'graphDepartureTime', 
    'plot_all_graphs', 
    'create_heatmap',
    'prepare_model_data',
    'logistic_regression_model',
    'reduced_model'
]


def load_and_preprocess_data(file_path):

    delays_df = pd.read_csv(file_path)
    delays_df['isDelayed'] = [1 if status == 'delayed' else 0 for status in delays_df['Flight Status']]
    return delays_df


def createGraph(delays_df, group, xlabel, axis):
    groupAverage = delays_df.groupby([group])['isDelayed'].mean()

    if group == 'DAY_WEEK':
        groupAverage = groupAverage.reindex(index=np.roll(groupAverage.index, 1))
        groupAverage.index = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    ax = groupAverage.plot.bar(color='C0', ax=axis)
    ax.set_ylabel('Average Delay')
    ax.set_xlabel(xlabel)
    return ax


def graphDepartureTime(delays_df, xlabel, axis):
 
    temp_df = pd.DataFrame({'CRS_DEP_TIME': delays_df['CRS_DEP_TIME'] // 100, 'isDelayed': delays_df['isDelayed']})
    groupAverage = temp_df.groupby(['CRS_DEP_TIME'])['isDelayed'].mean()

    ax = groupAverage.plot.bar(color='C0', ax=axis)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Average Delay')


def plot_all_graphs(delays_df):

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 10))

    createGraph(delays_df, 'DAY_WEEK', 'Day of week', axis=axes[0][0])
    createGraph(delays_df, 'DEST', 'Destination', axis=axes[0][1])
    graphDepartureTime(delays_df, 'Departure time', axis=axes[1][0])
    createGraph(delays_df, 'CARRIER', 'Carrier', axis=axes[1][1])
    createGraph(delays_df, 'ORIGIN', 'Origin', axis=axes[2][0])
    createGraph(delays_df, 'Weather', 'Weather', axis=axes[2][1])

    plt.tight_layout()
    plt.show()


def create_heatmap(delays_df):

    agg = delays_df.groupby(['ORIGIN', 'DAY_WEEK', 'CARRIER']).isDelayed.mean().reset_index()

    height_ratios = [len(agg[agg.ORIGIN == origin].CARRIER.unique()) for origin in sorted(delays_df.ORIGIN.unique())]
    gridspec_kw = {'height_ratios': height_ratios, 'width_ratios': [15, 1]}

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 6), gridspec_kw=gridspec_kw)
    axes[0, 1].axis('off')
    axes[2, 1].axis('off')

    maxIsDelay = agg.isDelayed.max()

    for i, origin in enumerate(sorted(delays_df.ORIGIN.unique())):
        data = pd.pivot_table(agg[agg.ORIGIN == origin], values='isDelayed', aggfunc=np.sum, index=['CARRIER'], columns=['DAY_WEEK'])
        data = data[[7, 1, 2, 3, 4, 5, 6]]
        ax = sns.heatmap(data, ax=axes[i][0], vmin=0, vmax=maxIsDelay, cbar_ax=axes[1][1], cmap=sns.light_palette("navy"))
        ax.set_xticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
        if i != 2:
            ax.get_xaxis().set_visible(False)
        ax.set_ylabel('Airport ' + origin)

    plt.show()


def prepare_model_data(delays_df):

    delays_df.DAY_WEEK = delays_df.DAY_WEEK.astype('category')
    delays_df.CRS_DEP_TIME = [round(t / 100) for t in delays_df.CRS_DEP_TIME]
    delays_df.CRS_DEP_TIME = delays_df.CRS_DEP_TIME.astype('category')

    predictors = ['DAY_WEEK', 'CRS_DEP_TIME', 'ORIGIN', 'DEST', 'CARRIER', 'Weather']
    outcome = 'isDelayed'

    X = pd.get_dummies(delays_df[predictors], drop_first=True)
    y = delays_df[outcome]
    return train_test_split(X, y, test_size=0.4, random_state=1)


def logistic_regression_model(train_X, train_y, valid_X, valid_y):

    logit_full = LogisticRegression(penalty="l2", C=1e42, solver='liblinear')
    logit_full.fit(train_X, train_y)

    print('intercept ', logit_full.intercept_[0])
    print(pd.DataFrame({'coeff': logit_full.coef_[0]}, index=train_X.columns).transpose())
    print('AIC', AIC_score(valid_y, logit_full.predict(valid_X), df=len(train_X.columns) + 1))

    logit_reg_pred = logit_full.predict_proba(valid_X)

    full_result = pd.DataFrame({'actual': valid_y,
                                'p(0)': [p[0] for p in logit_reg_pred],
                                'p(1)': [p[1] for p in logit_reg_pred],
                                'predicted': logit_full.predict(valid_X)})
    full_result = full_result.sort_values(by=['p(1)'], ascending=False)

    classificationSummary(full_result.actual, full_result.predicted, class_names=['ontime', 'delayed'])
    gainsChart(full_result.actual, figsize=[5, 5])
    plt.show()


def reduced_model(delays_df):

    delays_df['CRS_DEP_TIME'] = [round(t / 100) for t in delays_df['CRS_DEP_TIME']]

    delays_red_df = pd.DataFrame({
        'Sun_Mon': [1 if d in (1, 7) else 0 for d in delays_df.DAY_WEEK],
        'Weather': delays_df.Weather,
        'CARRIER_CO_MQ_DH_RU': [1 if d in ("CO", "MQ", "DH", "RU") else 0 for d in delays_df.CARRIER],
        'MORNING': [1 if d in (6, 7, 8, 9) else 0 for d in delays_df.CRS_DEP_TIME],
        'NOON': [1 if d in (10, 11, 12, 13) else 0 for d in delays_df.CRS_DEP_TIME],
        'AFTER2P': [1 if d in (14, 15, 16, 17, 18) else 0 for d in delays_df.CRS_DEP_TIME],
        'EVENING': [1 if d in (19, 20) else 0 for d in delays_df.CRS_DEP_TIME],
        'isDelayed': delays_df['isDelayed'],
    })

    X = delays_red_df.drop(columns=['isDelayed'])
    y = delays_red_df['isDelayed']

    train_X, valid_X, train_y, valid_y = train_test_split(X, y, test_size=0.4, random_state=1)

    logit_reg = LogisticRegressionCV(penalty="l1", solver='liblinear', cv=5)
    logit_reg.fit(train_X, train_y)

    print('intercept', logit_reg.intercept_[0])
    print(pd.DataFrame({'coeff': logit_reg.coef_[0]}, index=X.columns).transpose())
    print('AIC', AIC_score(valid_y, logit_reg.predict(valid_X), df=len(train_X.columns) + 1))

    classificationSummary(valid_y, logit_reg.predict(valid_X), class_names=['ontime', 'delayed'])

    logit_reg_proba = logit_reg.predict_proba(valid_X)

    red_result = pd.DataFrame({'actual': valid_y,
                               'p(0)': [p[0] for p in logit_reg_proba],
                               'p(1)': [p[1] for p in logit_reg_proba],
                               'predicted': logit_reg.predict(valid_X)})
    red_result = red_result.sort_values(by=['p(1)'], ascending=False)

    ax = gainsChart(red_result.actual, color='C0', figsize=[5, 5], label='Reduced model')
    gainsChart(red_result.actual, color='C1', ax=ax, label='Full model')
    plt.legend(loc='upper left')
    plt.show()
