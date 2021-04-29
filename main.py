# main.py

import ctypes
import os
import random
import funcs
from win32api import GetSystemMetrics
from config import SETTINGS as s


def setup():
    if not os.path.exists('Downloaded-Images'):
        os.makedirs('Downloaded-Images')
    if not s["night-backgrounds"]["links"] and not os.path.exists('Custom-Backgrounds'):
        os.makedirs('Custom-Backgrounds')
        f = open("Custom-Backgrounds\\PUT CUSTOM IMAGES IN HERE (CAN BE ANY NORMAL IMAGE TYPE)", "x")
    if not s["monitor-x"]:
        s["monitor-x"] = GetSystemMetrics(0)
    if not s["monitor-y"]:
        s["monitor-y"] = GetSystemMetrics(1)


def main():
    if s["night-backgrounds"]["toggle"] and funcs.IsNight():
        # Night Background Fetch
        path, link = funcs.FetchImage()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        if s["night-backgrounds"]["notify"]:
            funcs.Notify("New Background from Custom-Backgrounds", path.split('\\')[-1], link, None, path)
    else:
        # Reddit Background Fetch
        path, data, exists = funcs.FetchRedditImage(funcs.jsonFetch(random.choice(s['subreddits'])))
        if path and data:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            if not exists:
                funcs.Notify(f"New Background from {data['subreddit']}", f"{data['title']}", f"https://reddit.com{data['permalink']}", "bin/reddit.ico", False)
        else:
            funcs.Notify(path, "Error", False, "reddit.ico", False)


if __name__ == "__main__":
    setup()
    main()
