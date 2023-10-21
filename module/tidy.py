import os
import shutil


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
            names = [chr(ord("A") + i) for i in range(26)] + [chr(ord("a") + i) for i in range(26)] + \
                    [chr(ord("0") + i) for i in range(10)]
            for k in names:
                if os.path.isdir(k):
                    for filename in os.listdir(k):
                        shutil.move(os.path.join(k, filename), filename)
                    os.rmdir(k)
        case _:
            print(f"Usage: tidy [fold|unfold|foldaz|foldAZ]")


def solve(args):
    match args[0]:
        case "tidy":
            if len(args) == 1:
                print("Usage: tidy [fold|unfold|foldaz]")
            else:
                tidy(args[1:])
        case _:
            return False
    return True
