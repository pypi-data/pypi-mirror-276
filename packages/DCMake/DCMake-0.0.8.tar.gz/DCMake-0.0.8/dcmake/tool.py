import subprocess, psutil, zipfile, sys, os

def checkGitAndCMake() -> bool:
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["cmake", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def getCPUThreads() -> int:
    return psutil.cpu_count(logical=False)

def unzipFile(zip_file: str, extract_dir: str) -> None:
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def clearConsole() -> None:
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def deleteFileList(fileList: str, dir: str) -> None:
    if fileList.find(";") == -1:
        fileName = fileList.split('/')[-1]
        os.remove(f"{dir}/{fileName}")
    else:
        for file in fileList.split(";"):
            fileName = file.spilt("/")[-1]
            os.remove(f"{dir}/{fileName}")