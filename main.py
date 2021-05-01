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


def main():
    Custom = False
    if f.IsNight(s["night-backgrounds"]["city"]):
        # Night Background Fetch
        Method = f.FetchMethod(s["night-backgrounds"]["methods"]["chosen-method"])
        if Method.lower() == 'local':
            Custom = True
        Path, Exists, Data = f.NightImageFetch(Method)
    else:
        # Reddit Background Fetch
        Path, Exists, Data = f.FetchImageFromReddit(f.jsonFetch(random.choice(s['subreddits'])))
        if debugNotify or not Exists:
            f.Notify(f"New Background from {Data['subreddit']}", f"{Data['title']}", Data['url_overridden_by_dest'],
                     "bin/reddit.ico", False)

    if not Custom:
        Path = f.IsCurrentBackground(Path)
    else:
        f.IsCurrentBackground(False)
    f.log(f'[main] Setting background as {Path}')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, Path, 0)


if __name__ == "__main__":
    f.logging_init()
    setup()
    main()
