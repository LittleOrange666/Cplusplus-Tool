import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import module


def cmds(args: list[str]):
    if len(args) == 0:
        print(f"Unknow command {args[0]!r}")
        return
    match args[0]:
        case "v":
            if len(args) == 1:
                print(f"Current C++ version is C++{module.config.cpp_version}")
            else:
                if args[1] in module.cpp_versions:
                    print(f"change C++ version to C++{args[1]}")
                    module.config.cpp_version = module.cpp_versions[args[1]]
                else:
                    print(f"invalid C++ version {args[1]!r}")
        case "argv" | "args":
            if len(args) == 1:
                print(f"Current compile arguments is {module.config.constant_argv!r}")
            else:
                module.config.constant_argv = ' '.join(args[1:])
                print(f"set compile arguments to {module.config.constant_argv!r}")
        case _:
            if module.base.solve(args):
                return
            if module.special.solve(args):
                return
            if module.tidy.solve(args):
                return
            if module.code.solve(args):
                return
            print(f"Unknow command {args[0]!r}")


if __name__ == '__main__':
    cmd = " ".join(sys.argv[1:])
    if cmd:
        try:
            cmds(cmd.split())
        except KeyboardInterrupt:
            pass
