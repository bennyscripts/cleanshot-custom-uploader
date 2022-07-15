import os 

def get_newest_file(path: str) -> str:
    files = os.listdir(path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    return os.path.join(path, files[-1])