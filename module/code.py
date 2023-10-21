import os
import shutil

import module


def solve(args: list[str]) -> bool:
    match args[0]:
        case "format":
            if len(args) == 1:
                target = module.base.newest()
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
                return
            if len(args) == 2:
                target = module.base.newest()
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
        case _:
            return False
    return True
