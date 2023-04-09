# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
from functools import partial
import seaborn as sns
from google.colab import drive
from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from math import sqrt
from scipy import stats


def test_model_reg(model, model_name, x_train, y_train, x_test, y_test):
    """
    Performs model fit and metric evaluation and visualization on the tests data
    Args:
       model: model object with `fit` and `predict` methods
       model_name (str):  Human readable model name
       x_train (np.ndarray): training data input
       y_train (np.ndarray): training data output
       x_test:
       y_test:

    Returns:
        dictionary of the evaluated scores
    """
    model.fit(x_train, y_train)
    y_test_pred = model.predict(x_test)
    y_train_pred = model.predict(x_train)

    r2_train = r2_score(y_train, y_train_pred)
    r2_test = r2_score(y_test, y_test_pred)

    mae_train = mean_absolute_error(y_train, y_train_pred)
    mae_test = mean_absolute_error(y_test, y_test_pred)

    rmse_train = mean_squared_error(y_train, y_train_pred, squared=False)
    rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)

    scores = {
        'r2': {'train': r2_train, 'val': r2_test},
        'rmse': {'train': rmse_train, 'val': rmse_test},
        'mae': {'train': mae_train, 'val': mae_test}
    }

    plt.scatter(y_test, y_test_pred, s=5)
    plt.xlabel('GT')
    plt.ylabel('Predicted')
    plt.gca().set_aspect('equal')
    plt.title(model_name)
    plt.show()
    plt.close()

    return scores


def plot_r2(model_names, model_scores_t, model_scores_v):
    """

    Args:
        model_names:
        model_scores_t:
        model_scores_v:

    Returns:

    """
    plt.plot(model_names, model_scores_t, '*', label='training')
    plt.plot(model_names, model_scores_v, '*', label='validation')
    plt.ylabel(r'$R^2$')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(-0.1, 1)
    plt.legend()
    plt.show()
    plt.close()


def plot_score_reg(model_names, model_scores_t, model_scores_v):
    plt.plot(model_names, model_scores_t, '*', label='training')
    plt.plot(model_names, model_scores_v, '*', label='validation')
    plt.ylabel('score')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()
    plt.close()


def plot_mae(model_names, model_scores_t, model_scores_v):
    plt.plot(model_names, model_scores_t, '*', label='training')
    plt.plot(model_names, model_scores_v, '*', label='validation')
    plt.ylabel('MAE')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()
    plt.close()


def plot_rmse(model_names, model_scores_t, model_scores_v):
    plt.plot(model_names, model_scores_t, '*', label='training')
    plt.plot(model_names, model_scores_v, '*', label='validation')
    plt.ylabel('RMSE')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()
    plt.close()


def test_model_class(model, model_name, x_train, y_train, x_test, y_test):
    model.fit(x_train, y_train)
    y_test_pred = model.predict(x_test)
    y_train_pred = model.predict(x_train)

    score_train = model.score(x_train, y_train)
    score_test = model.score(x_test, y_test)

    f1_test = f1_score(y_test, y_test_pred)
    f1_train = f1_score(y_train, y_train_pred)

    # con_mtx = confusion_matrix(y_test, y_test_pred)

    precision_test = precision_score(y_test, y_test_pred, zero_division=0)
    precision_train = precision_score(y_train, y_train_pred, zero_division=0)

    recall_test = recall_score(y_test, y_test_pred)
    recall_train = recall_score(y_train, y_train_pred)

    scores = {
        'Score': {'train': score_train, 'val': score_test},
        'F1': {'train': f1_train, 'val': f1_test},
        'Precision': {'train': precision_train, 'val': precision_test},
        'Recall': {'train': recall_train, 'val': recall_test},
        'AP': None,
        'PR_curve': None,
    }

    try:
        y_test_pred_proba = model.predict_proba(x_test)
        y_train_pred_proba = model.predict_proba(x_train)

        ohe = OneHotEncoder(sparse=False)
        y_train_oh = ohe.fit_transform(y_train.reshape((-1, 1)))
        y_test_oh = ohe.fit_transform(y_test.reshape((-1, 1)))

        ap_test = average_precision_score(y_test_oh, y_test_pred_proba)
        ap_train = average_precision_score(y_train_oh, y_train_pred_proba)

        pr_curve_test = precision_recall_curve(y_test, y_test_pred_proba[:, -1])
        pr_curve_train = precision_recall_curve(y_train, y_train_pred_proba[:, -1])

        scores['AP'] = {'train': ap_train, 'val': ap_test}
        scores['PR_curve'] = {'train': pr_curve_train, 'val': pr_curve_test}
    except AttributeError as e:
        print(e)

    ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred, normalize='true')
    plt.title(model_name)
    plt.show()
    plt.close()

    return scores


def plot_score_generic(model_names, model_scores_t, model_scores_v, score_name):
    plt.plot(model_names, model_scores_t, '*', label='training')
    plt.plot(model_names, model_scores_v, '*', label='validation')
    plt.ylabel(score_name)
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()
    plt.close()


def plot_score(model_names, model_scores_t, model_scores_v):
    plot_score_generic(model_names, model_scores_t, model_scores_v, score_name='score')


def plot_f1_score(model_names, model_scores_t, model_scores_v):
    plot_score_generic(model_names, model_scores_t, model_scores_v, score_name='f1')


def plot_score_precision(model_names, model_scores_t, model_scores_v):
    plot_score_generic(model_names, model_scores_t, model_scores_v, score_name='precision')


def plot_score_recall(model_names, model_scores_t, model_scores_v):
    plot_score_generic(model_names, model_scores_t, model_scores_v, score_name='recall')


def plot_score_ap(model_names, model_scores_t, model_scores_v):
    plot_score_generic(model_names, model_scores_t, model_scores_v, score_name='AP')


def plot_curve_generic(model_names, model_scores_t, model_scores_v, x_score_name, y_score_name):
    for mn, (precision, recall, thresholds) in zip(model_names, model_scores_t):
        plt.plot(recall, precision, '--', label=f'{mn} training')
    for mn, (precision, recall, thresholds) in zip(model_names, model_scores_v):
        plt.plot(recall, precision, '-', label=f'{mn} validation')

    plt.ylabel(y_score_name)
    plt.xlabel(x_score_name)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.show()
    plt.close()


def merge_results_dict(res_merge_into, res_merge_from):
    if len(res_merge_into) == 0:
        for k, v_from in res_merge_from.items():
            if type(v_from) not in [list, np.ndarray]:
                continue
            res_merge_into[k] = v_from.copy()
        return

    for k, v_from in res_merge_from.items():
        if type(v_from) not in [list, np.ndarray]:
            continue

        if k not in res_merge_into:
            raise ValueError(f'Unexpected key in new result dict: {k}')

        v_into = res_merge_into[k]

        if type(v_from) == list and type(v_into) == list:
            v_into.extend(v_from)
        elif type(v_from) == np.ndarray and type(v_into) == np.ndarray:
            v_new = np.concatenate((v_into, v_from))
            res_merge_into[k] = v_new
        # elif type(v_into) == list:
        #   v_into.append(v_from)
        # else:
        #   v_new = [v_into, v_from]
        #   res_merge_into[k] = v_new


def grid_reg(model, params, features, target):
    scoring = {'r2': make_scorer(r2_score),
               'rmse': make_scorer(mean_squared_error),
               'mae': make_scorer(mean_absolute_error)
               }

    #####
    if type(params) == list:
        results = {}
        found_params = {}
        for params_i in params:
            print(f'found_params={found_params}, params_i={params_i}')
            test_params = found_params.copy()
            for k, v in params_i.items():
                print(f'k={k}, v={v}, test_params={test_params}')
                test_params[k] = v
                print(f'new test_params={test_params}')
            # {'max_depth':[4,16,22]}
            model_grid = GridSearchCV(model, test_params, scoring=scoring, refit='r2')
            model_grid.fit(features, target)

            found_params = {k: [v] for k, v in model_grid.best_params_.items()}

            merge_results_dict(results, model_grid.cv_results_)

        grid_results = pd.DataFrame(results)
    else:
        model_grid = GridSearchCV(model, params, scoring=scoring, refit='r2')
        model_grid.fit(features, target)
        grid_results = pd.DataFrame(model_grid.cv_results_)

    ####

    grid_results['params'] = list(map(lambda n: str(list(n.values())), grid_results['params']))
    grid_results['root_mean_test_mse'] = list(map(lambda n: sqrt(n), grid_results['mean_test_rmse']))

    return model_grid, grid_results


def plot_cv_r2(model_name, model_params, model_r2):
    fig, ax = plt.subplots()
    fig.set_size_inches(30, 10)
    plt.plot(model_params, model_r2, label='r2')
    plt.xticks(rotation=90, ha='right')
    plt.title(model_name)
    plt.legend()
    plt.show()
    plt.close()


def plot_mae_mse(model_name, model_params, model_mse, model_mae):
    fig, ax = plt.subplots()
    fig.set_size_inches(30, 10)
    plt.plot(model_params, model_mae, label='mae')
    plt.plot(model_params, model_mse, label='rmse')
    plt.xticks(rotation=90, ha='right')
    plt.title(model_name)
    plt.legend()
    plt.show()
    plt.close()


def grid_class(model, params, features, target):
    scoring = {'accuracy': make_scorer(accuracy_score),
               'precision': make_scorer(precision_score, average='macro', zero_division=0),
               'recall': make_scorer(recall_score, average='macro'),
               'f1': make_scorer(f1_score, average='macro')}

    ######
    if type(params) == list:
        results = {}
        found_params = {}
        for params_i in params:
            # print(f'found_params={found_params}, params_i={params_i}')
            test_params = found_params.copy()
            for k, v in params_i.items():
                # print(f'k={k}, v={v}, test_params={test_params}')
                test_params[k] = v
                # print(f'new test_params={test_params}')
            model_grid = GridSearchCV(model, test_params, scoring=scoring, refit='f1')
            model_grid.fit(features, target)

            found_params = {k: [v] for k, v in model_grid.best_params_.items()}

            merge_results_dict(results, model_grid.cv_results_)
            print(results)

        df_grid = pd.DataFrame(results)
    else:
        model_grid = GridSearchCV(model, params, scoring=scoring, refit='f1')
        model_grid.fit(features, target)
        df_grid = pd.DataFrame(model_grid.cv_results_)

    #####

    df_grid = pd.DataFrame(model_grid.cv_results_)
    df_grid['params'] = list(map(lambda n: str(list(n.values())), df_grid['params']))
    return model_grid, df_grid


def plot_cv_metrics(model_name, model_params, model_f1, model_recall, model_precision, model_accuracy):
    fig, ax = plt.subplots()
    fig.set_size_inches(30, 10)
    plt.plot(model_params, model_f1, label='f1')
    plt.plot(model_params, model_recall, label='recall')
    plt.plot(model_params, model_precision, label='precision')
    plt.plot(model_params, model_accuracy, label='accuracy')
    plt.xticks(rotation=90, ha='right')
    plt.title(model_name)
    plt.legend()
    plt.show()
    plt.close()


def display_corr_regr(x, y, **kws):
    r, _ = stats.pearsonr(x, y)
    ax = plt.gca()
    ax.annotate("r = {:.1f}".format(r),
                xy=(0.2, 0.95),
                xycoords=ax.transAxes, size=20)


def display_corr_class(x, y, **kws):
    r, _ = stats.pearsonr(x, y)
    ax = plt.gca()
    pos = (.1, .9) if kws['label'] == 'Yes' else (.5, .9)

    ax.annotate("{}: r = {:.2f}".format(kws['label'], r),
                xy=pos, xycoords=ax.transAxes)


def plot_pair_grid_ref(df, hue):
    g = sns.PairGrid(data=df, hue=hue, height=4, aspect=1.5)
    g.map_upper(sns.regplot, scatter_kws={'s': 6}, line_kws={'color': 'black'})
    g.map_lower(display_corr_regr)
    g.map_lower(sns.kdeplot)
    g.map_diag(sns.histplot)


def plot_pair_grid_class(df, hue):
    g = sns.PairGrid(data=df, hue=hue, height=4, aspect=1.5)
    g.map_upper(sns.regplot, scatter_kws={'s': 6}, line_kws={'color': 'black'})
    g.map_lower(display_corr_class)
    g.map_lower(sns.kdeplot, gridsize=150)
    g.map_diag(sns.histplot)


def best_model(features, target, mode, grid, df, hue):
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

    models_fit_info = None

    if mode == 'regression':
        # plot_pair_grid_ref(df, hue = None)

        models_fit_info = {
            'LinearRegression': {'model': LinearRegression(), 'param': {}},
            # 'RandomForestRegressor': {'model': RandomForestRegressor(),'param' :{'n_estimators':[50,100,150,200,300,400,500],'max_depth':[1,2,4,8,16,64,128,512, 640,768,896]}},
            'RandomForestRegressor': {
                'model': RandomForestRegressor(),
                'param': [
                    {'max_depth': [4, 16, 32, 42]},
                    {'n_estimators': [50, 100, 150, 200, 300, 400, 500]}
                ]
            },
            'DecisionTreeRegressor': {'model': DecisionTreeRegressor(),
                                      'param': {'max_features': [0.1, 0.2, 0.3, 0.6, 0.7, 0.8, 1],
                                                'max_depth': [1, 2, 4, 8, 16, 64, 128, 512, 640, 768, 896]}},
            'Lasso': {'model': linear_model.Lasso(),
                      'param': {'alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0]}},
            'Ridge': {'model': Ridge(), 'param': {'alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 2.0, 2.3, 2.7, 3.0]}},
            'KNeighborsRegressor': {'model': KNeighborsRegressor(),
                                    'param': {'n_neighbors': [2, 3, 5, 10, 15, 17, 19, 21, 23, 25],
                                              'weights': ('uniform', 'distance')}},
            'GradientBoostingRegressor': {'model': GradientBoostingRegressor(),
                                          'param': {'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                                                    'n_estimators': [50, 100, 150, 200, 300, 400, 500]}},
            'AdaBoostRegressor': {'model': AdaBoostRegressor(),
                                  'param': {'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                                            'n_estimators': [50, 100, 150, 200, 300, 400, 500]}},
            'XGBRegressor': {'model': xgb.XGBRegressor(),
                             'param': {'objective': ['reg:squarederror'], 'max_depth': [1, 2, 4, 8, 16, 64, 128, 512],
                                       'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]}}
        }
        # iterate all models, do grid search and final training and evaluations
        for model_name, model_info in models_fit_info.items():
            if grid == 'Yes':
                model_grid, grid_results = grid_reg(model_info['model'], model_info['param'], features, target)
                # cv_model_with_best_params = model_grid.best_estimator_
                model_info['best_param'] = model_grid.best_params_
                model_class = model_info['model'].__class__
                new_model_with_best_params = model_class(**model_info['best_param'])
                model_info['model'] = new_model_with_best_params
                # plor metrics r2 for cv_model
                plot_cv_r2(model_name + 'CV', grid_results['params'], grid_results['mean_test_r2'])
                # plot mae, mse for cv_model
                plot_mae_mse(model_name + 'CV', grid_results['params'], grid_results['mean_test_mae'],
                             grid_results['root_mean_test_mse'])
            model = model_info['model']
            metrics_dict = test_model_reg(model, model_name, x_train, y_train, x_test, y_test)
            model_info['metrics'] = metrics_dict

        model_names = list(models_fit_info.keys())

        for score_name, score_plot_fn in zip(['r2', 'rmse', 'mae'], [plot_r2, plot_rmse, plot_mae]):
            model_score_tra = [models_fit_info[mn]['metrics'][score_name]['train'] for mn in model_names]
            model_score_val = [models_fit_info[mn]['metrics'][score_name]['val'] for mn in model_names]

            score_plot_fn(model_names, model_score_tra, model_score_val)

        return models_fit_info

    if mode == 'classification':
        plot_pair_grid_class(df, hue)
        models_fit_info = {
            'DecisionTree': {'model': DecisionTreeClassifier(), 'param': {'max_depth': [1, 2, 4, 8, 16, 64, 128, 512],
                                                                          'max_features': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
                                                                                           0.7, 1]}},
            # RandomForest': {'model': RandomForestClassifier(),'param' : {'max_depth':[1,2,4,6,10,328,16,64,128,256,512],'criterion':('gini', 'entropy')}},
            'RandomForest':
                {'model': RandomForestClassifier(),
                 'param': [{'max_depth': [1, 2, 4, 6, 10, 328, 16, 64, 128, 256, 512]},
                           {'criterion': ('gini', 'entropy')}]},
            'SVM': {'model': svm.SVC(), 'param': {'C': [0.1, 1, 10]}},
            'LogisticRegression': {'model': LogisticRegression(), 'param': {'C': [0.5, 1.0, 2.0, 3.0, 10.0, 20.0]}},
            'KNeighborsClassifier': {'model': KNeighborsClassifier(),
                                     'param': {'n_neighbors': [3, 5, 10, 12, 15, 20, 25],
                                               'weights': ('uniform', 'distance')}},
            'GradientBoostingClassifier': {'model': GradientBoostingClassifier(),
                                           'param': {'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                                                     'n_estimators': [50, 100, 150, 200, 300, 400, 500]}},
            'AdaBoostClassifier': {'model': AdaBoostClassifier(),
                                   'param': {'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                                             'n_estimators': [50, 100, 150, 200, 300, 400, 500]}},
            'XGBClassifier': {'model': xgb.XGBClassifier(), 'param': {'max_depth': [1, 2, 4, 8, 16, 64, 128, 512],
                                                                      'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
                                                                                        0.7]}},
            'GaussianNB': {'model': GaussianNB(), 'param': {}}
        }

        for model_name, model_info in models_fit_info.items():
            if grid == 'Yes':
                model_grid, df_grid = grid_class(model_info['model'], model_info['param'], features, target)

                model_info['best_param'] = model_grid.best_params_
                model_class = model_info['model'].__class__
                new_model_with_best_params = model_class(**model_info['best_param'])

                model_info['model'] = new_model_with_best_params
                # plot metrics for cv_model
                plot_cv_metrics(model_name + 'CV', df_grid['params'], df_grid['mean_test_f1'],
                                df_grid['mean_test_recall'], df_grid['mean_test_precision'],
                                df_grid['mean_test_accuracy'])

            model = model_info['model']
            metrics_dict = test_model_class(model, model_name, x_train, y_train, x_test, y_test)
            model_info['metrics'] = metrics_dict

        model_names = list(models_fit_info.keys())

        # for score_name, score_plot_fn in zip(['score', 'f1', 'precision', 'recall'], [plot_score, plot_f1_score, plot_score_precision,plot_score_recall]):
        for score_name in ['Score', 'F1', 'Precision', 'Recall', 'AP']:
            selected_model_names = []
            model_score_tra = []
            model_score_val = []

            for mn in model_names:
                model_metrics = models_fit_info[mn]['metrics'][score_name]
                if model_metrics is None:
                    continue

                selected_model_names.append(mn)
                model_score_tra.append(model_metrics['train'])
                model_score_val.append(model_metrics['val'])

            plot_score_generic(selected_model_names, model_score_tra, model_score_val, score_name)

        for score_name, (x_score_name, y_score_name) in [('PR_curve', ('Recall', 'Precision'))]:
            selected_model_names = []
            model_score_tra = []
            model_score_val = []

            for mn in model_names:
                model_metrics = models_fit_info[mn]['metrics'][score_name]
                if model_metrics is None:
                    continue

                selected_model_names.append(mn)
                model_score_tra.append(model_metrics['train'])
                model_score_val.append(model_metrics['val'])

            plot_curve_generic(selected_model_names, model_score_tra, model_score_val, x_score_name=x_score_name,
                               y_score_name=y_score_name)

        return models_fit_info
