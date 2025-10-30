# created using github copilot

import json
import requests
import sqlite3


def get_question(amount):
    url = "https://opentdb.com/api.php?amount=" + str(amount) + "&type=multiple"
    response = requests.get(url)
    data = response.json()
    return data


def add_question(data):
    conn = sqlite3.connect('Trivia.sqlite')
    c = conn.cursor()
    # add and id for each question
    c.execute(
        "CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question text, questionData text)")
    for i in range(len(data['results'])):
        data['results'][i].pop('type')
        data['results'][i].pop('difficulty')
        question = data['results'][i]['question'].replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                          "\'\'")
        data['results'][i].pop('question')
        questionData = json.dumps(data['results'][i]).replace("\"", "\"\"").replace("&quot;", "\"\"").replace("&#039;",
                                                                                                              "\'")
        c.execute(
            "INSERT INTO questions (question, questionData)" + " VALUES(\"" + question + "\", \"" + questionData + "\")")

    conn.commit()
    conn.close()


def main():
    amount = 1000
    for i in range(int(amount / 50)):
        data = get_question(50)
        add_question(data)


if __name__ == "__main__":
    main()
