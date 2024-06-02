import subprocess, json


def get_args_base():
    return [
        # '--gen-onefile',
        "--cs-gen-json-serializer",
        "--gen-object-api",
        "--gen-all",
    ]


def get_args_dot_net(fname):
    args = get_args_base()
    args.extend(["-n", "-o", rf".\dotnet", rf".\definitions\{fname}.fbs"])
    return args


def get_args_python(fname):
    args = get_args_base()
    args.append("--gen-onefile")
    args.extend(["--python", "-o", rf".\python", rf".\definitions\{fname}.fbs"])
    return args


def get_args_typescript(fname):
    args = get_args_base()
    args.append("--gen-onefile")
    args.extend(["--ts", "-o", rf".\ts\{fname}", rf".\definitions\{fname}.fbs"])
    return args


def get_cmds_map():
    with open(r"./definitions/cmds.json") as f:
        return json.load(f)


def generate_cmds_dotnet():
    cmds = get_cmds_map()
    cmd_definitions = "\n".join(
        [f'_cmdDict.Add("{cmd}", {value});' for cmd, value in cmds.items()]
    )

    dotnet_script = f"""
    using System.Collections.Generic;
    public class VROBOTS_CMDS
    {{
        private static readonly VROBOTS_CMDS _instance = new VROBOTS_CMDS();
        public static VROBOTS_CMDS Instance => _instance;
        private Dictionary<string, ushort> _cmdDict = new();
        VROBOTS_CMDS(){{
            {cmd_definitions}
        }}
        
        public Dictionary<string, ushort> CmdDict
        {{
            get {{ return _cmdDict; }}
        }}
    }}
    """

    with open(r".\dotnet\VROBOTS_CMDS.cs", "w") as f:
        f.write(dotnet_script)


def generate_cmds_python():
    cmds = get_cmds_map()
    cmd_definitions = "\n".join(
        [f'    "{cmd}": {value},' for cmd, value in cmds.items()]
    )

    python_script = f"""CMD_DICT = {{
        {cmd_definitions}
        }}
    """

    with open(r".\python\VROBOTS_CMDS.py", "w") as f:
        f.write(python_script)


def generate_cmds_typescript():
    cmds = get_cmds_map()
    cmd_definitions = "\n".join(
        [f'        this._cmdDict.set("{cmd}", {value});' for cmd, value in cmds.items()]
    )

    typescript_script = f"""
    class VROBOTS_CMDS {{
        private static _instance: VROBOTS_CMDS;
        private _cmdDict: Map<string, number> = new Map<string, number>();

        private constructor() {{
            this._initializeCmds();
        }}

        public static get Instance(): VROBOTS_CMDS {{
            if (!this._instance) {{
                this._instance = new VROBOTS_CMDS();
            }}
            return this._instance;
        }}

        private _initializeCmds(): void {{
    {cmd_definitions}
        }}

        public get cmdDict(): Map<string, number> {{
            return this._cmdDict;
        }}
    }}

    export default VROBOTS_CMDS;
    """

    with open(r".\ts\VROBOTS_CMDS.ts", "w") as f:
        f.write(typescript_script)


# assumes window.
def generate_msg(fname):
    command = r".\flatc.exe"

    print(f"Generating {fname} dotnet")
    args = get_args_dot_net(fname)
    subprocess.run([command] + args)
    generate_cmds_dotnet()

    print(f"Generating {fname} python")
    args = get_args_python(fname)
    subprocess.run([command] + args)
    generate_cmds_python()

    print(f"Generating {fname} typescript")
    args = get_args_typescript(fname)
    subprocess.run([command] + args)
    generate_cmds_typescript()


# for *.fbs in definitions, generate message.
def generate_all():
    import os

    # # clear the folders
    # for folder in ["dotnet", "python", "ts"]:
    #     for file in os.listdir(f"./{folder}"):
    #         os.remove(f"./{folder}/{file}")

    for file in os.listdir(r"./definitions"):
        if "vectors" in file:
            continue

        if file.endswith(".fbs"):
            fname = file[:-4]
            generate_msg(fname)


if __name__ == "__main__":
    generate_all()
