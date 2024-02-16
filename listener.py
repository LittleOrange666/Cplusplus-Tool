import json
from io import BytesIO

import pyzipper
import requests
from flask import Flask, Response, jsonify, request, render_template
from flask_cors import cross_origin

app = Flask(__name__, template_folder="./")

testcase = {"Title": "Nothing", "Data": [], "TimeLimit": 1.0, "Cansubmit": False}
all_testcase = {}
submissions = {}


@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def get_test():
    return Response(status=200)


@app.route('/writetestcase', methods=['POST'])
@cross_origin()
def write_testcase():
    global testcase, submission
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
    testcase["Cansubmit"] = "cansubmit" in request.form
    submission = ""
    all_testcase[testcase["Title"]] = testcase.copy()
    return Response(status=200)


@app.route('/presenttestcase', methods=['POST'])
@cross_origin()
def present_testcase():
    global testcase, submission
    if "title" not in request.form:
        return Response("argument missing: title", status=400)
    if "type" not in request.form:
        return Response("argument missing: type", status=400)
    if "timelimit" not in request.form:
        return Response("argument missing: timelimit", status=400)
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
            pairs.sort(key=lambda x: x[0].filename)
            for a, b in pairs:
                data.append([zip_file.read(a).decode("utf8"), zip_file.read(b).decode("utf8")])
        case "text":
            if "links" not in request.form:
                return Response("argument missing: link", status=400)
            links = json.loads(request.form["links"])
            if not type(links) is list:
                return Response("data format invalid", status=400)
            for o in links:
                if not (type(o) is list and len(o) == 2 and type(o[0]) is str and type(o[1]) is str):
                    return Response("data format invalid", status=400)
            for o in links:
                pair = [requests.get(link, allow_redirects=True).content.decode("utf8") for link in o]
                data.append(pair)
        case _:
            return Response("data type invalid", status=400)
    testcase["Title"] = request.form["title"]
    testcase["TimeLimit"] = float(request.form["timelimit"])
    testcase["Data"] = data
    testcase["Cansubmit"] = "cansubmit" in request.form
    submission = ""
    all_testcase[testcase["Title"]] = testcase.copy()
    return Response(status=200)


@app.route('/readtestcase', methods=['GET', 'POST'])
@cross_origin()
def read_testcase():
    ret = testcase
    key = None
    if request.method == 'POST':
        if "key" in request.form:
            key = request.form["key"]
    else:
        if "key" in request.args:
            key = request.args.get("key")
    key = None
    if key is not None:
        for k in all_testcase:
            if key in k:
                ret = all_testcase[k]
    return jsonify(**ret)


@app.route('/inputtestcase', methods=['GET'])
def input_testcase():
    return render_template('input_testcase.html')


@app.route('/submit', methods=['POST'])
def submit():
    target = testcase
    if "key" in request.form:
        key = request.form["key"]
        for k in all_testcase:
            if key in k:
                pass  # target = all_testcase[k]
    submissions[target["Title"]] = request.form["content"]
    return jsonify({"title": target["Title"], "cansubmit": target["Cansubmit"]})


@app.route('/waitsubmit', methods=['POST'])
@cross_origin()
def waitsubmit():
    global submission
    if "title" not in request.form:
        return Response("argument missing: title", status=400)
    if request.form["title"] in submissions:
        ret = Response(submissions.pop(request.form["title"]), status=200)
        ret.mimetype = "text/plain"
        return ret
    return Response(status=204)


if __name__ == '__main__':
    try:
        responce = requests.get('http://127.0.0.1:5555/test', timeout=1)
        print("server is running")
        exit(0)
    except requests.exceptions.Timeout:
        pass
    app.run(port=5555)
