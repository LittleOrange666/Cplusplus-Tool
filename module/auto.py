import json
import os
import signal
import subprocess
from time import sleep

import module
import requests

url = 'http://127.0.0.1:5555'


def auto(args: list[str]) -> None:
    match args[0]:
        case "judge" | "test":
            testing = "test" == args[0]
            target = module.base.newest()
            if target is None:
                return
            sus = module.base.docompile(target, False)
            exefile = module.base.getexename(target)
            if not sus:
                return
            try:
                response = requests.get(url + "/readtestcase", timeout=1)
            except requests.exceptions.Timeout:
                print("Cannot connect to listener")
                return
            data = json.loads(response.text)
            print(f"start testing '{os.path.abspath(target)}' with {data['Title']!r}")
            tests = data['Data']
            tl = data["TimeLimit"]
            ac = 0
            for i, v in enumerate(tests):
                print(f"\nstart testing for testcase #{i + 1}")
                proc = subprocess.Popen([exefile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                try:
                    if not v[0].endswith("\n"):
                        v[0] += "\n"
                    if testing:
                        print(f"Input #{i + 1}:")
                        print(v[0])
                        print(f"Answer #{i + 1}:")
                        print(v[1])
                        print(f"Output #{i + 1}:")
                    outs, errs = proc.communicate(v[0].encode(encoding=module.encoding), timeout=tl)
                    if testing:
                        print(outs.decode(encoding=module.encoding), end="")
                    else:
                        ans: list[str] = v[1].split("\n")
                        out: list[str] = outs.decode(encoding=module.encoding).split("\n")
                        while ans and not ans[-1]:
                            ans.pop()
                        while out and not out[-1]:
                            out.pop()
                        if len(ans) > len(out):
                            print(f"Wrong Answer: Output too short, required {len(ans)} lines, got {len(out)} lines")
                        elif len(ans) < len(out):
                            print(f"Wrong Answer: Output too long, required {len(ans)} lines, got {len(out)} lines")
                        else:
                            for j in range(len(ans)):
                                ans[j] = ans[j].strip()
                                out[j] = out[j].strip()
                                if ans[j].split() != out[j].split():
                                    print(f"Wrong Answer in Line {j + 1}: expected {ans[j]!r}, got {out[j]!r}")
                                    break
                            else:
                                print("Accepted")
                                ac += 1
                except subprocess.TimeoutExpired:
                    print("Time Limit Exceed")
            if testing:
                print(f"\ntest completed")
            else:
                print(f"\ntest completed, {ac}/{len(tests)} Accepted")
        case "submit":
            target = module.base.newest()
            if target is None:
                return
            with open(target, "r") as f:
                content = f.read()
            response = requests.post(url + "/submit", {"content": content}, timeout=1)
            if response.status_code == 200:
                print(f"Submit Success for {response.text!r}")
            else:
                print(f"Submit Failed: error {response.status_code}")
        case "init":
            print("try to init listener")
            target = os.path.join(os.path.dirname(os.path.dirname(__file__)), "listener.py")
            subprocess.Popen(["start", "python", target], shell=True)
        case _:
            print("Usage: cpt auto [test|judge|submit]")


def solve(args) -> bool:
    match args[0]:
        case "auto":
            if len(args) == 1:
                print("Usage: cpt auto [test|judge|submit]")
            else:
                auto(args[1:])
        case _:
            return False
    return True
