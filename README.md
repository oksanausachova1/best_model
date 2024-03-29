# best_model
This modul performs a hyperparameter search and model selection process for a given set of models and their parameters. This function works for both regression and classification problems and helps you find the best model for your data.
There examples of using this code.
For regression problems, the function tries to optimize the performance of the following models by hyperparameter search:

Random Forest Regressor

Decision Tree Regressor

Lasso

Ridge

K Neighbors Regressor

Gradient Boosting Regressor

Ada Boost Regressor

XGB Regressor

The function trains each model with the best set of hyperparameters and calculates R-squared, root mean squared error (RMSE), and mean absolute error (MAE) metrics on the training and validation sets. Finally, the function generates a plot for each metric for comparison among models.

For classification problems, the function tries to optimize the performance of the following models by hyperparameter search:

Decision Tree Classifier

Random Forest Classifier

K Neighbors Classifier

Gradient Boosting Classifier

Ada Boost Classifier

XGB Classifier

The function trains each model with the best set of hyperparameters and calculates accuracy, F1 score, precision, recall, and ROC AUC metrics on the training and validation sets. Finally, the function generates a plot for each metric for comparison among models.Also show a confusion matrix for models

The function takes the following arguments:

features: a pandas dataframe containing the features to be used in the analysis

target: a pandas series containing the target variable for the analysis

mode: a string indicating the type of analysis ('regression' or 'classification')

grid: a string indicating whether a grid search should be performed ('Yes' or 'No')

df: a pandas dataframe containing the features and target variable for visualization purposes

hue: a string indicating the variable to be used for color coding the visualization

models: a list of tuples containing models to be included in the analysis, along with their respective hyperparameters, to override the default models and hyperparameters. If None, default models and hyperparameters will be used.

The function returns a dictionary containing the model names as keys and their respective hyperparameters, trained models, and metrics as values.
These functions generate pair plots of the given dataframe df:

 - for regression problems -  generates a grid of regplot that creates a scatter plot with a regression line fit to the data  in the upper triangle and kernel density with annotations of correlation coefficients  estimates in the lower triangle. The scatterplots in the upper triangle show the relationship between each pair of variables, while the annotations of correlation coefficients in the lower triangle show the strength and direction of the correlation between each pair of variables, histograms of each variable on the diagonal of the PairGrid.

 - for classification problems - generates a grid of regplot that creates a scatter plot with a regression line fit to the data  in the upper triangle and kernel density with annotations of correlation coefficients  estimates in the lower triangle. The scatterplots in the upper triangle show the relationship between each pair of variables, while the annotations of correlation coefficients in the lower triangle show the strength and direction of the correlation between each pair of variables, histograms of each variable on the diagonal of the PairGrid.

The hue parameter is used to color-code the plots based on a categorical variable, making it easier to see how different subgroups of the data are related.
