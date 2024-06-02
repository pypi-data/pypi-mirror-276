import requests, subprocess, os, shutil, threading, itertools, time
from tqdm import tqdm

try:
    import dcmake.tool as tool
    import dcmake.config as config
except:
    import tool, config

gitCloneBool = False
cmakeConfigBool = False
cmakeBuildBool = False

def downloadFile(url: str, path: str) -> bool:
    try:
        if path == None: path = "./"
        if not os.path.exists(path):
            os.makedirs(path)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        newFilePath = f"{path}/{url.split("/")[-1]}"
        with open(newFilePath, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=newFilePath) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: 
                        f.write(chunk)
                        pbar.update(len(chunk))
        return True
    except Exception:
        return False

def downloadFileList(uelList: str, path: str) -> bool:
    try:
        for url in uelList.split(";"):
            downloadFile(url, path)
        return True
    except Exception:
        return False

def install(url: str) -> bool:
    try:
        dirpath = "./.dcmake"
        path = f"{dirpath}/temp/{url.split("/")[-1]}"
        MessagesGit = itertools.cycle([
            f"{config.colors["yellow"]}[{config.colors["red"]}X{config.colors["yellow"]}] {config.colors["cyan"]}Clone Repository.{config.colors["end"]}",
            f"{config.colors["yellow"]}[{config.colors["red"]}X{config.colors["yellow"]}] {config.colors["cyan"]}Clone Repository..{config.colors["end"]}",
            f"{config.colors["yellow"]}[{config.colors["red"]}X{config.colors["yellow"]}] {config.colors["cyan"]}Clone Repository...{config.colors["end"]}"
        ])
        MessagesConfig = itertools.cycle([
            f"{config.colors['yellow']}[{config.colors['red']}X{config.colors['yellow']}] {config.colors['cyan']}Configure Project.{config.colors['end']}",
            f"{config.colors['yellow']}[{config.colors['red']}X{config.colors['yellow']}] {config.colors['cyan']}Configure Project..{config.colors['end']}",
            f"{config.colors['yellow']}[{config.colors['red']}X{config.colors['yellow']}] {config.colors['cyan']}Configure Project...{config.colors['end']}",
        ])
        MessagesBuild = itertools.cycle([
            f"{config.colors['yellow']}[{config.colors['red']}X{config.colors['yellow']}] {config.colors['cyan']}Build Project.{config.colors['end']}",
            f"{config.colors['yellow']}[{config.colors['red']}X{config.colors['yellow']}] {config.colors['cyan']}Build Project..{config.colors['end']}",
            f"{config.colors['yellow']}[{config.colors['red']}X{config.colors['yellow']}] {config.colors['cyan']}Build Project...{config.colors['end']}"
        ])
        if not os.path.exists(dirpath):
            os.makedirs(path)
            os.mkdir(dirpath + "/bin/")
            os.mkdir(dirpath + "/lib/")
        threading.Thread(target=gitClone, args=(url, path)).start()
        while not gitCloneBool:
            tool.clearConsole()
            print(f"{next(MessagesGit)}")
            time.sleep(1)
        if os.path.exists(path + "/CMakeLists.txt"):
            threading.Thread(target=cmakeConfig, args=(path,)).start()
            while not cmakeConfigBool:
                tool.clearConsole()
                print(f"{next(MessagesConfig)}")
                time.sleep(1)
            threading.Thread(target=cmakeBuild, args=(path,)).start()
            while not cmakeBuildBool:
                tool.clearConsole()
                print(f"{next(MessagesBuild)}")
                time.sleep(1)
            tool.clearConsole()
            for root, _, files in os.walk(path + "/build/Release/"):
                for file in files:
                    if file.endswith(".lib"):
                        shutil.copy2(os.path.join(root, file), os.path.join(dirpath, "lib", file))
                    elif file.endswith(".dll") or file.endswith(".exe"):
                        shutil.copy2(os.path.join(root, file), os.path.join(dirpath, "bin", file))
            shutil.rmtree("./" + path.split("/")[2], True)
            reset()
            return True
        reset()
        return False
    except Exception:
        return False

def reset() -> None:
    global gitCloneBool, cmakeConfigBool, cmakeBuildBool
    gitCloneBool = False
    cmakeConfigBool = False
    cmakeBuildBool = False

def gitClone(url: str, path: str) -> bool:
    global gitCloneBool
    try:
        subprocess.run(["git", "clone", "--recursive", url, path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        pass
    gitCloneBool = True

def cmakeConfig(path: str) -> bool:
    global cmakeConfigBool
    try:
        subprocess.run(["cmake", "--no-warn-unused-cli", "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE", "-S" + path, "-B" + path + "/build", "-G", "Visual Studio 17 2022", "-T", "host=x64", "-A", "x64"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        pass
    cmakeConfigBool = True

def cmakeBuild(path: str) -> bool:
    global cmakeBuildBool
    try:
        subprocess.run(["cmake", "--build", path + "/build", "--config", "Release", "--target", "ALL_BUILD" ,"-j", f"{tool.getCPUThreads() * 2}", "--"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        pass
    cmakeBuildBool = True