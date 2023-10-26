import json
import os


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


config = JsonConfig(os.path.join(os.path.dirname(__file__), "config.json"))
command_map = {
    "auto": "auto",
    "format": "content",
    "usaco": "content",
    "import": "content",
    "template": "content",
    "mhc": "special",
    "tidy": "tidy",
    "c": "base",
    "r": "base",
    "rf": "base",
    "rt": "base",
    "run": "base",
    "gdb": "base"
}