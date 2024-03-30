from pypmml import Model

model = Model.load('data/DecisionTreeModel74.pmml')
prediction = model.predict({"month": 4, "day": 1, "weekday": 0})
print(prediction)