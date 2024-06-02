import requests, subprocess, os, shutil
import dcmake.tool as tool
from tqdm import tqdm

def downloadFile(url: str, path: str) -> bool:
    try:
        if path == None:
            path = "./" + url.split('/')[-1]
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=path) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: 
                        f.write(chunk)
                        pbar.update(len(chunk))
        return True
    except Exception:
        return False

def install(url: str) -> bool:
    try:
        dirpath = "./.dcmake"
        path = f"{dirpath}/.temp/{url.split('/')[-1]}"
        if not os.path.exists(dirpath):
            os.makedirs(path)
            os.mkdir(dirpath + "/bin/")
            os.mkdir(dirpath + "/lib/")
        subprocess.run(["git", "clone", "--recursive", url, path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(path + "/CMakeLists.txt"):
            subprocess.run(["cmake", "--no-warn-unused-cli", "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE", "-S" + path, "-B" + path + "/build", "-G", "Visual Studio 17 2022", "-T", "host=x64", "-A", "x64"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["cmake", "--build", path + "/build", "--config", "Release", "--target", "ALL_BUILD" ,"-j", f"{tool.getCPUThreads() * 2}", "--"])
            for root, _, files in os.walk(path + "/build/"):
                for file in files:
                    if file.endswith(".lib"):
                        shutil.copy2(os.path.join(root, file), os.path.join(dirpath, "lib", file))
                    elif file.endswith(".dll") or file.endswith(".exe"):
                        shutil.copy2(os.path.join(root, file), os.path.join(dirpath, "bin", file))
            shutil.rmtree("./" + path.split("/")[2], True)
            return True
        return False
    except Exception:
        return False