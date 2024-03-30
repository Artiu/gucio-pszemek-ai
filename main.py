import pandas as pd
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from imblearn import over_sampling
from sklearn2pmml.pipeline import PMMLPipeline
from sklearn2pmml import sklearn2pmml


data = pd.read_csv("data/data.csv")

X = data[["day", "month", "weekday"]]
y = data["was_live"]

smote = over_sampling.SMOTE()
X, y = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = DecisionTreeClassifier(max_depth=None, max_features="sqrt", min_samples_leaf=1, min_samples_split=2)

pipeline = PMMLPipeline([
    ("classifier", model)
])
pipeline.fit(X_train, y_train)
print(pipeline.score(X_test, y_test))
sklearn2pmml(pipeline, "DecisionTreeModel.pmml", with_repr = True)


# param_grid = {
#     'max_depth': [3, 5, 7, None],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'max_features': ['sqrt', 'log2', None]
# }
#
# grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
# grid_search.fit(X_train, y_train)
#
# best_params = grid_search.best_params_
# print("Best Hyperparameters:")
# print(best_params)
#
# best_model = grid_search.best_estimator_
# test_score = best_model.score(X_test, y_test)
# print("Test Accuracy:", test_score)
# print(best_model)

# score = model.score(X_test, y_test)
# print(score)
#
# predictions = model.predict(X_test)
# print(predictions)

# cross_val_score = cross_val_score(model, X, y, cv=3)
# print(cross_val_score)
