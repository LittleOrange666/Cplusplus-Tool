import json
import os
import subprocess

import module.base
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
            key = os.path.basename(target)[:-4]
            if not sus:
                return
            try:
                response = requests.get(url + "/readtestcase", {"key": key}, timeout=1)
            except requests.exceptions.Timeout:
                print("Cannot connect to listener, you may use 'cpt auto init' to open it")
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
                        print(v[1] + ("" if v[1].endswith("\n") else "\n"))
                        print(f"Output #{i + 1}:")
                    outs, errs = proc.communicate(v[0].encode(encoding="utf-8"), timeout=tl+5)
                    exitcode = proc.returncode
                    if exitcode>=2147483648:
                        exitcode -= 2147483648
                    if testing:
                        print(outs.decode(encoding="utf-8"), end="")
                        if exitcode:
                            print(f"Exited with code {exitcode}")
                    else:
                        if exitcode:
                            print(f"Runtime Error: Exited with code {exitcode}")
                            continue
                        ans: list[str] = v[1].split("\n")
                        out: list[str] = outs.decode(encoding="utf-8").split("\n")
                        while ans and not ans[-1].strip():
                            ans.pop()
                        while out and not out[-1].strip():
                            out.pop()
                        if len(ans) > len(out):
                            print(f"Wrong Answer: Output too short, required {len(ans)} lines, got {len(out)} lines")
                        elif len(ans) < len(out):
                            print(f"Wrong Answer: Output too long, required {len(ans)} lines, got {len(out)} lines")
                        else:
                            for j in range(len(ans)):
                                ans[j] = ans[j].strip()
                                out[j] = out[j].strip()
                                L0 = ans[j].split()
                                L1 = out[j].split()
                                if L0 != L1:
                                    if max(len(ans[j]), len(out[j])) < 100:
                                        print(f"Wrong Answer in Line {j + 1}: expected {ans[j]!r}, got {out[j]!r}")
                                    else:
                                        idx = next(i for i in range(len(L0)) if L0[i] != L1[i])
                                        th = (["th", "st", "nd", "rd"]+["th"]*6)[(i+1)%10]
                                        if (idx+1)%100//10 == 1:
                                            th = "th"
                                        print(f"Wrong Answer at {idx+1}{th} token in Line {j + 1} : expected {L0[idx]!r}, got {L1[idx]!r}")
                                        cnt = 0
                                        while cnt < idx and idx+cnt+1<len(L0) and idx+cnt+1<len(L1) and len(" ".join(L0[idx-cnt-1:idx+cnt+2])) < 100:
                                            cnt += 1
                                        print(f"output: {'... ' if idx>cnt else ''}{' '.join(L1[idx-cnt:idx+cnt+1])}{' ...' if idx+cnt+1<len(L1) else ''}")
                                        print(f"answer: {'... ' if idx>cnt else ''}{' '.join(L0[idx-cnt:idx+cnt+1])}{' ...' if idx+cnt+1<len(L0) else ''}")
                                    break
                            else:
                                print("Accepted")
                                ac += 1
                except subprocess.TimeoutExpired:
                    print("Time Limit Exceed")
                    proc.kill()
                    proc.communicate()
                    print(f"Stopped with code {proc.returncode}")
            if testing:
                print(f"\ntest completed")
            else:
                print(f"\ntest completed, {ac}/{len(tests)} Accepted")
                if 0 < ac == len(tests):
                    r = input("All Accepted, do you want to submit? (y/[n]): ")
                    if r.lower() == "y":
                        os.system("cpt auto submit")
        case "submit":
            target = module.base.newest()
            if target is None:
                return
            with open(target, "r") as f:
                content = f.read()
            try:
                key = os.path.basename(target)[:-4]
                response = requests.post(url + "/submit", {"content": content, "key": key}, timeout=1)
                if response.status_code == 200:
                    obj = response.json()
                    print(f"Submited for {obj['title']!r}")
                    if not obj['cansubmit']:
                        print(f"Warning: {obj['title']!r} may not support submission")
                else:
                    print(f"Submit Failed: error {response.status_code}")
            except requests.exceptions.Timeout:
                print("Cannot connect to listener, you may use 'cpt auto init' to open it")
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
