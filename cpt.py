import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import module


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
                print(f"Current C++ version is C++{module.config.cpp_version}")
            else:
                if args[1] in module.cpp_versions:
                    print(f"change C++ version to C++{args[1]}")
                    module.config.cpp_version = module.cpp_versions[args[1]]
                else:
                    print(f"invalid C++ version {args[1]!r}")
        case "cd":
            try:
                if len(args) < 2:
                    target = os.path.dirname(module.base.newest())
                else:
                    target = " ".join(args[1:])
                os.chdir(target)
            except FileNotFoundError:
                print("Invalid path")
            else:
                print(f"Change directory to {os.getcwd()!r}")
        case "argv" | "args":
            if len(args) == 1:
                print(f"Current compile arguments is {module.config.constant_argv!r}")
            else:
                module.config.constant_argv = ' '.join(args[1:])
                print(f"set compile arguments to {module.config.constant_argv!r}")
        case "exit" | "quit" | "q":
            running = False
        case _:
            if module.base.solve(args):
                return
            if module.special.solve(args):
                return
            if module.tidy.solve(args):
                return
            if module.code.solve(args):
                return
            print(f"Unknow command {args[0]!r}, use '-help' to see command help")


def solve(cmd):
    if cmd.startswith("!"):
        if cmd[1:].startswith("cd "):
            print("Warning: System command 'cd' is invalid, use '-cd' to change directory")
        module.base.system(cmd[1:])
    elif cmd.startswith("-"):
        cmds(cmd[1:])
    else:
        module.base.docompile(cmd, possible_args=True)


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
