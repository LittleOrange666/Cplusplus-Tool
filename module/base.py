import os
import re
import subprocess
from io import StringIO
from colorama import Fore

import module

cptpath = os.path.join(os.path.expanduser("~"), ".cpt")
eofflag = "\\eof"


def system(s: str, timing: bool = False) -> int:
    if timing:
        s = repr(s)[1:-1]
        if s[0] == '"':
            s = '"\\"' + s[1:-1] + '\\""'
        s = 'powershell -Command "& {Measure-Command { ' + s + ' | Out-Default }}"'
    return os.system(s)


def newest() -> str | None:
    target = None
    for dirPath, dirNames, fileNames in os.walk(os.getcwd()):
        for f in fileNames:
            file = os.path.join(dirPath, f)
            if file.endswith(".cpp") and (target is None or os.path.getmtime(file) > os.path.getmtime(target)):
                target = file
    if target is None:
        print(f"no cpp file here")
        return None
    return target


def getexename(filename: str) -> str:
    if filename.endswith(".cpp"):
        filename = filename[:-4]
    exefile = os.path.abspath(filename + ".exe")
    exefile = os.path.join(cptpath, exefile.replace("\\", "_"))
    if not os.path.isdir(os.path.dirname(exefile)):
        os.makedirs(os.path.dirname(exefile))
    return exefile


def docompile(cmd: str, dorun: bool = True, force: bool = False, gdb: bool = False, timing: bool = False,
              possible_args=False) -> bool:
    cpp_version = module.config.cpp_version
    argv = ""
    if possible_args and " " in cmd:
        argv = cmd[cmd.find(" ") + 1:]
        cmd = cmd[:cmd.find(" ")]
    if cmd.endswith(".cpp"):
        cmd = cmd[:-4]
    cppfile = os.path.abspath(cmd + ".cpp")
    exefile = getexename(cmd)
    if not os.path.isfile(cppfile):
        print(f"file {cppfile!r} not existed")
        return False
    if not os.path.isfile(exefile) or os.path.getmtime(exefile) < os.path.getmtime(cppfile) or force:
        print(f"start compiling {cmd}.cpp in C++{cpp_version}")
        compile_cmd = f'g++ -g "{cppfile}" -o "{exefile}" -std=c++{cpp_version} {module.config.constant_argv} {argv}'
        proc = subprocess.run(compile_cmd, capture_output=True)
        if proc.returncode:
            err = proc.stderr.decode("utf8")
            key = cppfile+":"
            ok = False
            outs = {}
            for line in err.split("\n"):
                if line.startswith(key) or True:
                    check = re.match("([A-Z]:[^\\:]*):(\\d+):(\\d+): error: (.*)", line)
                    if check is not None:
                        ok = True
                        s = f"{Fore.RED}Error{Fore.RESET} at line {Fore.YELLOW}{check.group(2)}{Fore.RESET}: {check.group(4)}"
                        if check.group(1) not in outs:
                            outs[check.group(1)] = [s]
                        else:
                            outs[check.group(1)].append(s)
            for k,v in outs.items():
                print(f"errors in {k}:")
                for s in v:
                    print(s)
            if not ok:
                for line in err.split("\n"):
                    if "error" in line:
                        print(line) 
            print("compile faild")
            return False
        else:
            print("compile success")
    if dorun:
        print(f"start runnning {cmd}.cpp")
        oldpath = os.getcwd()
        os.chdir(os.path.dirname(cppfile))
        if gdb:
            system(f'gdb -silent "{exefile}"', timing)
        else:
            errorcode = system(f'"{exefile}"', timing)
            print(f"program exited with Code {errorcode}")
        os.chdir(oldpath)
    return True


def runwithfile(file: str, infile: str | None = None, outfile: str | None = None) -> None:
    sus = docompile(file, False)
    if not sus:
        return
    exefile = getexename(file)
    if infile is None:
        print(f"please input some content and ends with {eofflag}:")
        lines = []
        while True:
            s = input()
            if s == eofflag:
                break
            lines.append(s)
        in_stream = StringIO("\n".join(lines) + "\n")
    else:
        in_stream = open(infile, "r", encoding="utf-8")
    out_stream = None
    if outfile is not None:
        out_stream = open(outfile, "w", encoding="utf-8")
    print(f"start runnning {os.path.abspath(file)}.cpp")
    proc = subprocess.Popen([exefile], stdin=in_stream, stdout=out_stream)
    proc.wait()
    print(f"program exited with Code {proc.returncode}")


def solve(args: list[str]) -> bool:
    match args[0]:
        case "c":
            if len(args) < 2:
                target = newest()
                if target is not None:
                    docompile(target, False, True)
            else:
                docompile(" ".join(args[1:]), False, True, possible_args=True)
        case "r":
            if len(args) == 1:
                print("Filename required")
            if len(args) == 2:
                runwithfile(args[1])
            if len(args) == 3:
                runwithfile(args[1], args[2])
            if len(args) >= 4:
                runwithfile(args[1], args[2], args[3])
        case "rf":
            target = newest()
            if target is not None:
                if len(args) == 1:
                    runwithfile(target[:-4])
                if len(args) == 2:
                    runwithfile(target[:-4], args[1])
                if len(args) >= 3:
                    runwithfile(target[:-4], args[1], args[2])
        case "run":
            target = newest()
            if target is not None:
                docompile(target)
        case "rt":
            target = newest()
            if target is not None:
                docompile(target, timing=True)
        case "gdb":
            target = newest()
            if target is not None:
                docompile(target, force=True, gdb=True)
        case _:
            return False
    return True
