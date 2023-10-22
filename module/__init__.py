import os
import json
import tempfile
import module.base as base
import module.special as special
import module.tidy as tidy
import module.code as code
import module.auto as auto


class JsonConfig:
    def __init__(self, filename):
        self.__dict__["_filename"] = filename
        with open(self._filename) as f:
            self.__dict__["_obj"] = json.load(f)

    def __getattr__(self, item):
        return self._obj[item]

    def __setattr__(self, key, value):
        with open(self._filename) as f:
            self.__dict__["_obj"] = json.load(f)
        self._obj[key] = value
        with open(self._filename, "w") as f:
            json.dump(self._obj, f)


os.environ["PYTHONUTF8"] = "1"

config = JsonConfig(os.path.join(os.path.dirname(__file__), "config.json"))

cpp_versions = {"11": "11", "14": "14", "17": "17", "20": "2a"}
eofflag = "\\eof"
encoding = "utf8"
tmps = []
cptpath = os.path.join(os.path.expanduser("~"), ".cpt")
hidingexe = True


def tmpf() -> str:
    o = tempfile.mkstemp(suffix=".txt")
    os.close(o[0])
    tmps.append(o[1])
    return o[1]


def tmpr() -> None:
    for s in tmps:
        os.remove(s)
    tmps.clear()
