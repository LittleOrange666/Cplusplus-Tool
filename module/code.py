import os
import shutil

import module

imports = os.path.join(os.path.dirname(os.path.dirname(__file__)), "import")
defines_prefix = ("#", "using", "const")


def doimport(target, name):
    source_file = os.path.join(imports, name + ".cpp")
    if not os.path.isfile(source_file):
        print(f"Library name {name!r} does not exist")
        return
    with open(target, "r") as f:
        source = f.read().split("\n")
    with open(source_file, "r") as f:
        lib = f.read().split("\n")
    src_def = [s.replace(" ", "") for s in source if any(s.startswith(k) for k in defines_prefix)]
    lib_def = [s for s in lib if any(s.startswith(k) for k in defines_prefix)]
    lib_def = [s for s in lib_def if s.replace(" ", "") not in src_def]
    lib_all = lib_def + [s for s in lib if not any(s.startswith(k) for k in defines_prefix)]
    main_line = 0
    for i in range(len(source)):
        if "main()" in source[i]:
            main_line = i
            break
    source = source[:main_line] + lib_all + source[main_line:]
    with open(target, "w") as f:
        f.write("\n".join(source))
    print(f"Imported {name!r} to {target}")


def solve(args: list[str]) -> bool:
    match args[0]:
        case "format":
            if len(args) == 1:
                target = module.base.newest()
            else:
                target = args[1]
            if not os.path.isfile(target):
                print("Invalid path")
                return True
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
                target = module.base.newest()
            else:
                target = args[1]
            if not target.endswith(".cpp"):
                target += ".cpp"
            if os.path.isfile(target) and os.path.getsize(target) > 0:
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
                return True
            if len(args) == 2:
                target = module.base.newest()
                name = args[1]
            else:
                target = args[1]
                name = args[2]
            if not os.path.isfile(target):
                print("Invalid path")
                return True
            with open(target) as f:
                content = f.read()
            it = content.find("main(")
            if it == -1:
                print("main() function missing")
                return False
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
        case "import":
            if len(args) == 1:
                print("argument missing")
                return True
            target = module.base.newest()
            if target is None:
                return True
            doimport(target, args[1])
        case _:
            return False
    return True
