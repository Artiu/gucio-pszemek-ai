import csv
import os
import re

LOGS_PATH = "data/h2p_gucio-2024-03-15-messages/"
MESSAGES_REGEX = "\\[([0-9]{2}:[0-9]{2}:[0-9]{2})]\\s+([a-zA-Z0-9_]{4,25}):\\s+(.*)"
PSZEMEK_REGEX = "(poniedziałek|wtorek|środa|czwartek|piątek|sobota|niedziela)"
LOGS_REGEX = "([a-zA-Z0-9_]{4,25})-([0-9]{4}-[0-9]{2}-[0-9]{2})"


def parse_message(msg: str):
    found = re.search(MESSAGES_REGEX, msg)
    if found is None:
        return None
    time, nickname, content = found.groups()
    return {"nickname": nickname, "content": content}


def get_prediction_from_message(msg: str):
    found = re.search(PSZEMEK_REGEX, msg.lower())
    if found is None:
        return None
    return found.group(0)


def is_pszemek_message(msg: str):
    return "Następny stream -" in msg


def extract_data_from_chatterino_logs():
    paths = os.listdir(LOGS_PATH)
    predictions = []
    for path in paths:
        data = re.search(LOGS_REGEX, path)
        channel_name, date = data.groups()
        with open(LOGS_PATH + path, encoding='utf8') as file:
            messages = file.readlines()
            parsed_messages = [parse_message(message) for message in messages]
            bots_messages = [message for message in parsed_messages if
                             message is not None and (message["nickname"] == "streamelements" or message[
                                 "nickname"] == "streamlabs")]
            predictions_messages = [get_prediction_from_message(message["content"]) for message in bots_messages if
                                    is_pszemek_message(message["content"])]
            predictions_messages = [prediction for prediction in predictions_messages if
                                    prediction is not None]
            for message in predictions_messages:
                if len(predictions) > 0 and message == predictions[-1][1]:
                    continue
                predictions.append([date, message])
    filtered_predictions = []
    for i in range(len(predictions)):
        if i > 0 and predictions[i][0] == predictions[i - 1][0]:
            continue
        filtered_predictions.append(predictions[i])
    with open('data/predictions.csv', 'w', encoding='UTF8', newline='') as f:
        headers = ["date", "prediction"]
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(filtered_predictions)


extract_data_from_chatterino_logs()
