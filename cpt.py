import os
import shutil
import tempfile
import sys
import json
import subprocess
import pyzipper


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
running = True
eofflag = "\\eof"
encoding = "utf8"
tmps = []
cptpath = os.path.join(os.path.expanduser("~"), ".cpt")
hidingexe = True


def system(s: str, timing: bool = False) -> int:
    if timing:
        s = repr(s)[1:-1]
        if s[0] == '"':
            s = '"\\"' + s[1:-1] + '\\""'
        s = 'powershell -Command "& {Measure-Command { ' + s + ' | Out-Default }}"'
    # print(s)
    return os.system(s)


def tmpf() -> str:
    o = tempfile.mkstemp(suffix=".txt")
    os.close(o[0])
    tmps.append(o[1])
    return o[1]


def tmpr() -> None:
    for s in tmps:
        os.remove(s)
    tmps.clear()


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


def getexename(filename):
    if filename.endswith(".cpp"):
        filename = filename[:-4]
    exefile = os.path.abspath(filename + ".exe")
    if hidingexe:
        exefile = os.path.join(cptpath, exefile.replace("\\", "_"))
        if not os.path.isdir(os.path.dirname(exefile)):
            os.makedirs(os.path.dirname(exefile))
    return exefile


def docompile(cmd: str, dorun: bool = True, force: bool = False, gdb: bool = False, timing: bool = False,
              possible_args=False) -> bool:
    cpp_version = config.cpp_version
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
        system(f'g++ -g "{cppfile}" -o "{exefile}" -std=c++{cpp_version} {config.constant_argv} {argv}')
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


def runwithfile(file: str, infile: str | None = None, outfile: str | None = None):
    sus = docompile(file, False)
    if not sus:
        return
    exefile = getexename(file)
    if infile is None:
        print(f"please input some content and ends with {eofflag}:")
        infile = tmpf()
        lines = []
        while True:
            s = input()
            if s == eofflag:
                break
            lines.append(s)
        with open(infile, "w", encoding=encoding) as f:
            f.writelines(lines)
    isstdout = outfile is None
    if isstdout:
        outfile = tmpf()
    print(f"start runnning {os.path.abspath(file)}.cpp")
    errorcode = system(f'"{exefile}" < {infile} > {outfile}')
    if isstdout:
        with open(outfile, encoding=encoding) as f:
            print(f.read())
    print(f"program exited with Code {errorcode}")
    tmpr()


def mhc(cmd: str, argv: str):
    exefile = getexename(cmd)
    targetfolder = os.getcwd()
    targetfile = None
    if argv:
        if os.path.isdir(argv):
            targetfolder = argv
        elif os.path.isfile(argv):
            targetfile = argv
        else:
            print(f"Invalid file {argv!r}")
            return
    sus = docompile(cmd, False)
    if not sus:
        return
    proc = subprocess.Popen([exefile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if targetfile is None:
        files = os.listdir(targetfolder)
        files = [f for f in files if os.path.isfile(f)]
        for i, f in enumerate(files):
            iszip = pyzipper.is_zipfile(os.path.join(targetfolder, f))
            print(f"{i + 1}.{'(zipfile)' if iszip else ''}{f}")
        while True:
            choice = input("\nPlease input the number:")
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(files):
                    targetfile = os.path.join(targetfolder, files[choice - 1])
                    break
            print(f"Invalid choice {choice}")
        targetfile = os.path.abspath(targetfile)
        if pyzipper.is_zipfile(targetfile):
            zip_file = pyzipper.AESZipFile(targetfile)
            files = zip_file.filelist
            if len(files) == 0:
                print(f"Empty zipfile {choice}")
                return
            choicefile = files[0]
            if len(files) > 1:
                for i, f in enumerate(files):
                    print(f"{i + 1}.{f.filename}")
                while True:
                    choice = input("\nPlease input the number:")
                    if choice.isdigit():
                        choice = int(choice)
                        if 0 < choice <= len(files):
                            choicefile = files[choice - 1]
                            break
                    print(f"Invalid choice {choice}")
            tpf = tmpf()
            try:
                data = zip_file.read(choicefile)
            except RuntimeError:
                while True:
                    pwd = input("\nInput password:")
                    try:
                        data = zip_file.read(choicefile, pwd.encode(encoding))
                        break
                    except RuntimeError:
                        print("unzip faild")
            with open(tpf, "wb") as f:
                f.write(data)
            targetfile = tpf
    with open(targetfile, "rb") as f:
        send_data = f.read()
    if not send_data.endswith(b"\n"):
        send_data += b"\n"
    outfile = input("Output file:")
    outs, errs = proc.communicate(send_data)
    with open(outfile, "wb") as f:
        f.write(outs)
    print(f"program exited with Code {proc.returncode}")
    tmpr()


def tidy(args):
    match args[0]:
        case "fold":
            if len(args) < 2:
                print("Usage: tidy fold <prefix>")
            else:
                if not os.path.isdir(args[1]):
                    os.mkdir(args[1])
                cnt = 0
                key = args[1].lower()
                for filename in os.listdir():
                    if os.path.isfile(filename) and filename.lower().startswith(key):
                        cnt += 1
                        shutil.move(filename, os.path.join(args[1], filename))
                print(f"moved {cnt} files into folder {args[1]}")
        case "foldaz":
            names = {chr(ord("a") + i): [] for i in range(26)} | {chr(ord("0") + i): [] for i in range(10)}
            for filename in os.listdir():
                if os.path.isfile(filename):
                    ch = filename.lower()[0]
                    if ch in names:
                        names[ch].append(filename)
            for k, v in names.items():
                if len(v) == 0:
                    continue
                if not os.path.isdir(k):
                    os.mkdir(k)
                for filename in v:
                    shutil.move(filename, os.path.join(k, filename))
                print(f"moved {len(v)} files into folder {k!r}")
        case "foldAZ":
            names = {chr(ord("A") + i): [] for i in range(26)} | {chr(ord("0") + i): [] for i in range(10)}
            for filename in os.listdir():
                if os.path.isfile(filename):
                    ch = filename.upper()[0]
                    if ch in names:
                        names[ch].append(filename)
            for k, v in names.items():
                if len(v) == 0:
                    continue
                if not os.path.isdir(k):
                    os.mkdir(k)
                for filename in v:
                    shutil.move(filename, os.path.join(k, filename))
                print(f"moved {len(v)} files into folder {k!r}")
        case "unfold":
            if len(args) < 2:
                print("Usage: tidy unfold <foldername>")
            else:
                if os.path.isdir(args[1]):
                    for filename in os.listdir(args[1]):
                        shutil.move(os.path.join(args[1], filename), filename)
                    os.rmdir(args[1])
                else:
                    print(f"folder {args[1]} not exists")
        case "unfoldaz" | "unfoldAZ":
            names = [chr(ord("A") + i) for i in range(26)] + [chr(ord("a") + i) for i in range(26)] + [chr(ord("0") + i) for i in range(10)]
            for k in names:
                if os.path.isdir(k):
                    for filename in os.listdir(k):
                        shutil.move(os.path.join(k, filename), filename)
                    os.rmdir(k)
        case _:
            print(f"Usage: tidy [fold|unfold|foldaz|foldAZ]")


def cmds(cmd: str):
    global running
    args = cmd.split()
    if len(args) == 0:
        print(f"Unknow command {args[0]!r}, use '-help' to see command help")
        return
    match args[0]:
        case "help":
            print("""--- Tool Commands ---
-help                Show tool commands
-exit                Exit the Tool (-quit, -q)
-v (version)         Get/Set C++ version
-cd [path]           Change current directory
-argv (argv)         Get/Set default compile arguments (-args)
-c (file)            compile C++ file and no run
-run                 Run newwest C++ file
-gdb                 Debug newwest C++ file
-template (file)     Write template to file
-usaco (file) [name] Write usaco io to file
-r [file] (in) (out) Run C++ file with input and output file.
-rf (in) (out)       Run newwest C++ file with input and output file.
                     If no input, will require user input content.
                     If no output, will output to the screen after program ended.""")
        case "v":
            if len(args) == 1:
                print(f"Current C++ version is C++{config.cpp_version}")
            else:
                if args[1] in cpp_versions:
                    print(f"change C++ version to C++{args[1]}")
                    config.cpp_version = cpp_versions[args[1]]
                else:
                    print(f"invalid C++ version {args[1]!r}")
        case "cd":
            try:
                if len(args) < 2:
                    target = os.path.dirname(newest())
                else:
                    target = " ".join(args[1:])
                os.chdir(target)
            except FileNotFoundError:
                print("Invalid path")
            else:
                print(f"Change directory to {os.getcwd()!r}")
        case "c":
            if len(args) < 2:
                target = newest()
                if target is not None:
                    docompile(target, False, True)
            else:
                docompile(" ".join(args[1:]), False, True, possible_args=True)
        case "argv" | "args":
            if len(args) == 1:
                print(f"Current compile arguments is {config.constant_argv!r}")
            else:
                config.constant_argv = ' '.join(args[1:])
                print(f"set compile arguments to {config.constant_argv!r}")
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
            else:
                print("Target Missing")
        case "mhc":
            target = newest()
            if target is not None:
                if len(args) == 1:
                    mhc(target, "")
                else:
                    mhc(target, " ".join(args[1:]))
            else:
                print("Target Missing")
        case "run":
            target = newest()
            if target is not None:
                docompile(target)
            else:
                print("Target Missing")
        case "rt":
            target = newest()
            if target is not None:
                docompile(target, timing=True)
            else:
                print("Target Missing")
        case "gdb":
            target = newest()
            if target is not None:
                docompile(target, gdb=True)
            else:
                print("Target Missing")
        case "tidy":
            if len(args) == 1:
                print("Usage: tidy [fold|unfold|foldaz]")
            else:
                tidy(args[1:])
        case "format":
            if len(args) == 1:
                target = newest()
            else:
                target = args[1]
            if not os.path.isfile(target):
                print("Invalid path")
                return
            target = os.path.abspath(target)
            format_source = os.path.join(os.path.dirname(__file__), ".clang-format")
            format_target = os.path.join(os.path.dirname(target), ".clang-format")
            dotemp = not os.path.isfile(format_target)
            if dotemp:
                shutil.copy(format_source, format_target)
            os.system(f"clang-format -style=file -i \"{target}\"")
            if dotemp:
                os.remove(format_target)
            print(f"formated {target!r}")
        case "template":
            if len(args) == 1:
                target = newest()
            else:
                target = args[1]
            if not os.path.isfile(target):
                print("Invalid path")
            elif os.path.getsize(target) > 0:
                print(f"{target!r} is not a empty file")
            else:
                with open(os.path.join(os.path.dirname(__file__), "template.cpp")) as f:
                    template_content = f.read()
                with open(target, "w") as f:
                    f.write(template_content)
                    print(f"writed template to {target!r}")
        case "usaco":
            if len(args) == 1:
                print("argument missing")
                return
            if len(args) == 2:
                target = newest()
                name = args[1]
            else:
                target = args[1]
                name = args[2]
            if not os.path.isfile(target):
                print("Invalid path")
                return
            with open(target) as f:
                content = f.read()
            it = content.find("main(")
            if it == -1:
                print("main() function missing")
                return
            sp = content.find("\n", it)
            sp = content.find("\n", sp + 1)
            content = content[:sp] + \
                      f"""
#ifndef DEBUG
    ifstream cin("{name}.in");
    ofstream cout("{name}.out");
#endif""" + \
                      content[sp:]
            with open(target, "w") as f:
                f.write(content)
            print(f"writed usaco io {name!r} to {target!r}")

        case "exit" | "quit" | "q":
            running = False
        case _:
            print(f"Unknow command {args[0]!r}, use '-help' to see command help")


def solve(cmd):
    if cmd.startswith("!"):
        if cmd[1:].startswith("cd "):
            print("Warning: System command 'cd' is invalid, use '-cd' to change directory")
        system(cmd[1:])
    elif cmd.startswith("-"):
        cmds(cmd[1:])
    else:
        docompile(cmd, possible_args=True)


def main():
    print("Starting C++ Runner, Using '!' to run System Commands, Using '-' to run Tool Commands, Use '-exit' to exit")
    while running:
        try:
            cmd = input("\n(cpt) " + os.getcwd() + ">")
            if cmd == "":
                continue
        except KeyboardInterrupt:
            print("")
            return
        except EOFError:
            print("\nUnexpected Error")
            return
        solve(cmd)


if __name__ == '__main__':
    cmd = " ".join(sys.argv[1:])
    if cmd:
        if not cmd.startswith("-"):
            cmd = "-" + cmd
        try:
            solve(cmd)
        except KeyboardInterrupt:
            pass
    else:
        main()
        print("Stoping C++ Runner...")
