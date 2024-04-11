import m2cgen
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from imblearn import over_sampling

data = pd.read_csv("data/data.csv")

X = data[["day", "month", "weekday", "was_planned"]]
y = data["was_live"]

smote = over_sampling.SMOTE()
X, y = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearSVC(dual=True, C=0.001)
model.fit(X_train, y_train)

# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# precision = precision_score(y_test, y_pred)
# recall = recall_score(y_test, y_pred)
# f1 = f1_score(y_test, y_pred)
# roc_auc = roc_auc_score(y_test, y_pred)
#
# print(f'Accuracy: {accuracy}')
# print(f'Precision: {precision}')
# print(f'Recall: {recall}')
# print(f'F1-Score: {f1}')
# print(f'ROC AUC: {roc_auc}')
# print(classification_report(y_test, y_pred))
#
# cm = confusion_matrix(y_test, y_pred)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm)
# disp.plot()
# disp.ax_.set(title='Confusion Matrix')
# plt.show()
# print(precision_score(model))
# print(model.score(X_test, y_test))

# fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred)
# roc_auc = metrics.auc(fpr, tpr)
# display = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc)
# display.plot()
# plt.show()


code = m2cgen.export_to_javascript(model)
with open("generated_model.js", "w", encoding="utf8") as f:
    f.write(code)

# param_grid = {
#     'C': [0.001, 0.01, 0.1, 1, 10, 100],
#     'penalty': ['l1', 'l2'],
#     'loss': ['hinge', 'squared_hinge'],
#     'dual': [True, False]
# }
#
# grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
# grid_search.fit(X_train, y_train)
#
# best_params = grid_search.best_params_
# best_estimator = grid_search.best_estimator_
# print("Best Hyperparameters:")
# print(best_params)
# print(best_estimator.score(X_test, y_test))
#
#
# best_model = grid_search.best_estimator_
# test_score = best_model.score(X_test, y_test)
# print("Test Accuracy:", test_score)
# print(best_model)

score = model.score(X_test, y_test)
print(score)

predictions = model.predict(X_test)
print(predictions)
#
# cross_val_score = cross_val_score(model, X, y, cv=3)
# print(cross_val_score)
