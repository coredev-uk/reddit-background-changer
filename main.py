# main.py

import ctypes
import os
import random
import funcs as f
from win32api import GetSystemMetrics
from config import SETTINGS as s


def setup():
    if not os.path.exists(s['downloaded-path']):
        os.makedirs(s['downloaded-path'])
    if not os.path.exists(s['custom-path']):
        os.makedirs(s['custom-path'])
    if not os.path.exists(s['active-path']):
        os.makedirs(s['active-path'])
    if not s['night-backgrounds']['methods']['links'] and not os.path.exists(s['custom-path']):
        os.makedirs(s['custom-path'])
    if not s['res']['monitor-x']:
        s['res']['monitor-x'] = GetSystemMetrics(0)
    if not s['res']['monitor-y']:
        s['res']['monitor-y'] = GetSystemMetrics(1)
    if not s['res']['aspect-ratio']:
        s['res']['aspect-ratio'] = f.calculate_aspect(int(s['res']['monitor-x']), int(s['res']['monitor-y']))
    if not s['res']['max-x']:
        s['res']['max-x'] = str(int(s['res']['monitor-x']) + 1000)
    if not s['res']['max-y']:
        s['res']['max-y'] = str(int(s['res']['monitor-y']) + 1000)
    for file in os.listdir(s['custom-path']):
        FileTable = file.split('_')
        if "custom" not in FileTable:
            path = s['custom-path'] + file
            newPath = s['custom-path'] + 'custom_' + file
            os.rename(path, newPath)

def main():
    Current_Background = f.GetCurrentBackground(s['active-path'])
    if f.IsNight(s['night-backgrounds']['city']):
        Path = f.NightImageFetch(f.FetchMethod(s['night-backgrounds']['methods']['chosen-method'])) # Night Background Fetch
    else:
        Path = f.FetchImageFromReddit(f.jsonFetch(random.choice(s['subreddits'])), False) # Reddit Background Fetch

    Path = f.IsCurrentBackground(Path)
    FileName = Path.split('\\')[-1]
    f.log(f'[main] Old Background: {Current_Background}')
    f.log(f'[main] New Background: {FileName}')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, Path, 0)


if __name__ == "__main__":
    f.logging_init()
    setup()
    main()
