# main.py

import ctypes
import os
import random
import funcs as f
from win32api import GetSystemMetrics
from config import SETTINGS as s, debugNotify


def setup():
    if not os.path.exists(s['downloaded-path']):
        os.makedirs(s['downloaded-path'])
    if not os.path.exists(s['custom-path']):
        os.makedirs(s['custom-path'])
    if not os.path.exists(s['active-path']):
        os.makedirs(s['active-path'])
    if not s["night-backgrounds"]["methods"]["links"] and not os.path.exists(s['custom-path']):
        os.makedirs(s['custom-path'])
    if not s["monitor-x"]:
        s["monitor-x"] = GetSystemMetrics(0)
    if not s["monitor-y"]:
        s["monitor-y"] = GetSystemMetrics(1)
    for file in os.listdir(s['custom-path']):
        FileTable = file.split('_')
        if "custom" not in FileTable:
            path = s['custom-path'] + file
            newPath = s['custom-path'] + 'custom_' + file
            os.rename(path, newPath)

def main():
    Files = []
    Current_Background = None
    for file in os.listdir(s['active-path']):
        Files.append(file)
    if len(Files) == 1:
        Current_Background = Files[0]
    Custom = False
    if f.IsNight(s["night-backgrounds"]["city"]):
        # Night Background Fetch
        Method = f.FetchMethod(s["night-backgrounds"]["methods"]["chosen-method"])
        if Method.lower() == 'local':
            Custom = True
        Path, Exists, Data = f.NightImageFetch(Method)
    else:
        # Reddit Background Fetch
        Path, Exists, Data = f.FetchImageFromReddit(f.jsonFetch(random.choice(s['subreddits'])), False)
        if debugNotify or not Exists:
            f.Notify(f"New Background from {Data['subreddit']}", f"{Data['title']}", f'https://reddit.com{Data["permalink"]}',
                     "bin/reddit.ico", False)

    Path = f.IsCurrentBackground(Path)
    FileName = Path.split('\\')[-1]
    f.log(f'[main] Old Background: {Current_Background}')
    f.log(f'[main] New Background: {FileName}')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, Path, 0)


if __name__ == "__main__":
    f.logging_init()
    setup()
    main()
