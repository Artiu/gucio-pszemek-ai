import csv
import datetime

streams = set()

with open("data/streams.csv", 'r', encoding="utf8") as f:
    rows = csv.reader(f)
    next(rows)
    last_date = None
    for row in rows:
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M")
        if last_date is not None and ((date - last_date) < datetime.timedelta(hours=1)):
            last_date = date + datetime.timedelta(minutes=int(row[1]))
            continue
        last_date = date + datetime.timedelta(minutes=int(row[1]))
        streams.add(date.strftime("%Y-%m-%d"))

weekdays = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]

data = []

with open("data/predictions.csv", 'r', encoding="utf8") as f:
    rows = csv.reader(f)
    next(rows)
    for row in rows:
        prediction_date = datetime.datetime.strptime(row[0], "%Y-%m-%d")
        weekday = weekdays.index(row[1])
        weekdays_difference = weekday - prediction_date.weekday()
        if weekdays_difference < 0:
            weekdays_difference += 7
        predicted_date = prediction_date + datetime.timedelta(days=weekdays_difference)
        day_of_month = predicted_date.date().day
        month = predicted_date.date().month
        stream_date = predicted_date.strftime("%Y-%m-%d")
        was_live = stream_date in streams
        data.append([predicted_date.year, day_of_month, month, weekday, 1, 1 if was_live else 0])

last_date = None
filled_data = []
for row in data:
    if last_date is None:
        last_date = datetime.date(row[0], row[2], row[1])
        filled_data.append(row[1:])
        continue
    iter_date = last_date + datetime.timedelta(days=1)
    last_date = datetime.date(row[0], row[2], row[1])
    while iter_date < last_date:
        filled_data.append([iter_date.day, iter_date.month, iter_date.weekday(), 0, 0])
        iter_date += datetime.timedelta(days=1)
    filled_data.append(row[1:])


with open("data/data.csv", 'w', encoding="utf8", newline='') as f:
    w = csv.writer(f)
    w.writerow(["day", "month", "weekday", "was_planned", "was_live"])
    w.writerows(filled_data)
