import os
import sys

import colorama

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "module"))

import module
cpp_versions = {"11": "11", "14": "14", "17": "17", "20": "2a"}
os.environ["PYTHONUTF8"] = "1"


def cmds(args: list[str]):
    if len(args) == 0:
        print(f"Unknow command {args[0]!r}")
        return
    match args[0]:
        case "v":
            if len(args) == 1:
                print(f"Current C++ version is C++{module.config.cpp_version}")
            else:
                if args[1] in cpp_versions:
                    print(f"change C++ version to C++{args[1]}")
                    module.config.cpp_version = cpp_versions[args[1]]
                else:
                    print(f"invalid C++ version {args[1]!r}")
        case "argv" | "args":
            if len(args) == 1:
                print(f"Current compile arguments is {module.config.constant_argv!r}")
            else:
                module.config.constant_argv = ' '.join(args[1:])
                print(f"set compile arguments to {module.config.constant_argv!r}")
        case _:
            if args[0] in module.command_map:
                key = module.command_map[args[0]]
                __import__(key).solve(args)
                return
            print(f"Unknow command {args[0]!r}")


if __name__ == '__main__':
    cmd = " ".join(sys.argv[1:])
    colorama.init()
    if cmd:
        try:
            cmds(cmd.split())
        except KeyboardInterrupt:
            pass
