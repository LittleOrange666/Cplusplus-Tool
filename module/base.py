import os

import module


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
    if module.hidingexe:
        exefile = os.path.join(module.cptpath, exefile.replace("\\", "_"))
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
        system(f'g++ -g "{cppfile}" -o "{exefile}" -std=c++{cpp_version} {module.config.constant_argv} {argv}')
        if not os.path.isfile(exefile) or os.path.getmtime(exefile) < os.path.getmtime(cppfile):
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
        print(f"please input some content and ends with {module.eofflag}:")
        infile = module.tmpf()
        lines = []
        while True:
            s = input()
            if s == module.eofflag:
                break
            lines.append(s)
        with open(infile, "w", encoding=module.encoding) as f:
            f.writelines(lines)
    isstdout = outfile is None
    if isstdout:
        outfile = module.tmpf()
    print(f"start runnning {os.path.abspath(file)}.cpp")
    errorcode = system(f'"{exefile}" < {infile} > {outfile}')
    if isstdout:
        with open(outfile, encoding=module.encoding) as f:
            print(f.read())
    print(f"program exited with Code {errorcode}")
    module.tmpr()


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
                docompile(target, gdb=True)
        case _:
            return False
    return True
