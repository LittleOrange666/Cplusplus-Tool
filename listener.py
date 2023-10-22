import json

import requests
from flask import Flask, Response, jsonify, request
from flask_cors import cross_origin

app = Flask(__name__)

testcase = {"Title": "Nothing", "Data": [], "TimeLimit": 1.0}


@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def get_test():
    return Response(status=200)


@app.route('/writetestcase', methods=['POST'])
@cross_origin()
def write_testcase():
    global testcase
    if "title" not in request.form:
        return Response("argument missing: title", status=400)
    if "data" not in request.form:
        return Response("argument missing: data", status=400)
    if "timelimit" not in request.form:
        return Response("argument missing: timelimit", status=400)
    print(request.form["data"])
    data = json.loads(request.form["data"])
    if not type(data) is list:
        return Response("data format invalid", status=400)
    for o in data:
        if not (type(o) is list and len(o) == 2 and type(o[0]) is str and type(o[1]) is str):
            return Response("data format invalid", status=400)
    testcase["Title"] = request.form["title"]
    testcase["TimeLimit"] = float(request.form["timelimit"])
    testcase["Data"] = data
    return Response(status=200)


@app.route('/readtestcase', methods=['GET', 'POST'])
@cross_origin()
def read_testcase():
    global testcase
    return jsonify(**testcase)


if __name__ == '__main__':
    try:
        responce = requests.get('http://127.0.0.1:5555/test', timeout=1)
        print("server is running")
        exit(0)
    except requests.exceptions.Timeout:
        pass
    app.run(port=5555)
