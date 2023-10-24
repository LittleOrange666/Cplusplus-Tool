import json
from io import BytesIO

import pyzipper
import requests
from flask import Flask, Response, jsonify, request, render_template
from flask_cors import cross_origin

app = Flask(__name__, template_folder="./")

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


@app.route('/presenttestcase', methods=['POST'])
@cross_origin()
def present_testcase():
    global testcase
    if "title" not in request.form:
        return Response("argument missing: title", status=400)
    if "type" not in request.form:
        return Response("argument missing: type", status=400)
    if "timelimit" not in request.form:
        return Response("argument missing: timelimit", status=400)
    print(request.form["type"])
    data = []
    match request.form["type"]:
        case "zip":
            if "link" not in request.form:
                return Response("argument missing: link", status=400)
            link = request.form["link"]
            downloaded = requests.get(link, allow_redirects=True)
            datafile = BytesIO(downloaded.content)
            zip_file = pyzipper.AESZipFile(datafile)
            files = zip_file.filelist
            pairs = []
            di = {o.filename: o for o in files}
            for file in files:
                fn = file.filename
                if "in" in fn:
                    i = 0
                    while i != -1:
                        j = fn.find("in", i)
                        if j == -1:
                            break
                        o = fn[:j] + "out" + fn[j + 2:]
                        if o in di:
                            pairs.append((file, di[o]))
                            break
                        i = j + 1
            for a, b in pairs:
                data.append([zip_file.read(a).decode("utf8"), zip_file.read(b).decode("utf8")])
        case _:
            return Response("data type invalid", status=400)
    testcase["Title"] = request.form["title"]
    testcase["TimeLimit"] = float(request.form["timelimit"])
    testcase["Data"] = data
    return Response(status=200)


@app.route('/readtestcase', methods=['GET', 'POST'])
@cross_origin()
def read_testcase():
    global testcase
    return jsonify(**testcase)


@app.route('/inputtestcase', methods=['GET'])
def input_testcase():
    return render_template('input_testcase.html')


if __name__ == '__main__':
    try:
        responce = requests.get('http://127.0.0.1:5555/test', timeout=1)
        print("server is running")
        exit(0)
    except requests.exceptions.Timeout:
        pass
    app.run(port=5555)
