import os
import subprocess

import pyzipper

import module


def mhc(target: str, argv: str) -> None:
    exefile = module.base.getexename(target)
    targetfolder = os.getcwd()
    targetfile = None
    if argv:
        argv = os.path.abspath(argv)
        if os.path.isdir(argv):
            targetfolder = argv
        elif os.path.isfile(argv):
            targetfile = argv
        else:
            print(f"Invalid file {argv!r}")
            return
    sus = module.base.docompile(target, False)
    if not sus:
        return
    print(f"start runnning {os.path.abspath(target)}")
    proc = subprocess.Popen([exefile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outfile = input("Output file:")
    outfile = os.path.join(targetfolder, outfile)
    send_data = None
    if targetfile is None:
        files = os.listdir(targetfolder)
        files = [f for f in files if os.path.isfile(os.path.join(targetfolder,f)) and not f.endswith(".cpp")]
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
            try:
                data = zip_file.read(choicefile)
            except RuntimeError:
                while True:
                    pwd = input("\nInput password:")
                    try:
                        data = zip_file.read(choicefile, pwd.encode(module.encoding))
                        break
                    except RuntimeError:
                        print("unzip faild")
            send_data = data
    if send_data is None:
        with open(targetfile, "rb") as f:
            send_data = f.read()
    if not send_data.endswith(b"\n"):
        send_data += b"\n"
    outs, errs = proc.communicate(send_data)
    with open(outfile, "wb") as f:
        f.write(outs)
    print(f"program exited with Code {proc.returncode}")


def solve(args: list[str]) -> bool:
    match args[0]:
        case "mhc":
            target = module.base.newest()
            if target is not None:
                if len(args) == 1:
                    mhc(target, "")
                else:
                    mhc(target, " ".join(args[1:]))
        case _:
            return False
    return True
