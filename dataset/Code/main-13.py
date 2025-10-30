#!/usr/bin/env python3
from flask import Flask, render_template, request
import json
import requests

# Edit this to turn on dummy data
app_test = False

# app = Flask(__name__)

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/api/test/listfiles', methods=['POST'])
def listFiles():
    content_type = request.headers.get('Content-Type')

    print("working....")

    urlBase = "https://16io2k9t.directus.app/"

    login = {
        "email": "slothfulgod@gmail.com",
        "password": "KpztBh[RL[#RbhzAL98WWyis"
    }

    auth = requests.post(urlBase + "auth/login", json = login)
    print(auth.text)
    print("Printed auth.text")

    token = auth.json()['data']['access_token'] # Dear Fuck I love github copilot
    print(token)
    print("Printed token")

    url = urlBase + "files"
    req = requests.get(url, headers = {'Authorization': 'Bearer ' + token})
    print(req)
    print(type(req.content))
    content = req.content.decode("utf-8")#["data"]
    contentJson = json.loads(content)
    data = contentJson["data"] 
    print(type(data))
    for i in data:
        print(i["filename_download"])
    # print(data)
    # print(req.content.decode("utf-8"))

    return {"data": data}

@app.route('/') # Equivalent to: app.add_url_rule('/', '', index)
def index():
    return render_template('index.html')
