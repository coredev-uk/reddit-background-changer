import ctypes
import json
import os
import random
import urllib.request
import webbrowser
from win32api import GetSystemMetrics
from PIL import Image

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Settings - Here is where you can configure the script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SETTINGS = {
    "blacklist": [],
    "subreddits": ['EarthPorn'],
    "night-backgrounds": {
        "toggle": True,
        "links": [],
        "city": 'London'
    }
}
s = SETTINGS
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Functions - Do not Touch Anything Below Here - Do not Touch Anything Below Here - Do not Touch Anything Below Here - 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''


def jsonFetch(subreddit):
    req = urllib.request.Request(f'https://www.reddit.com/r/{subreddit}/top.json', headers={
        'User-agent': 'Reddit Background Setter (Created by u/Core_UK and u/Member87)'})
    res = urllib.request.urlopen(req)
    j = json.load(res)
    return j


def Notify(msg, title, link, icon, filename):
    def linkOpen():
        if filename:
            img = Image.open("Custom-Backgrounds\\" + filename)
            img.show()
        else:
            webbrowser.open_new(link)

    from win10toast_click import ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast(msg, title, icon_path=icon,
                       duration=None, threaded=True, callback_on_click=linkOpen)


def ImageFilter(x, y, data):
    if not x > y:
        return False
    if not x >= GetSystemMetrics(0):
        return False
    if not y >= GetSystemMetrics(1):
        return False
    for v in SETTINGS["blacklist"]:
        if v in data['id'] or v in data['url_overridden_by_dest']:
            return False
    return True


def FetchImage(night, j):
    url = None

    if not night:
        searchLimit = len(j['data']['children'])
        current = 0
        while not url:
            Data = j['data']['children'][current]['data']
            try:
                img = Data['preview']['images'][0]['source']
                FoundURL = Data['url_overridden_by_dest']
                if ImageFilter(img['width'], img['height'], Data):
                    url = FoundURL
                else:
                    current += 1
            except:
                current += 1

            if current >= searchLimit:
                url = j['data']['children'][0]['data']['url_overridden_by_dest']
    else:
        if os.path.exists('Custom-Backgrounds') and not s["night-backgrounds"]["links"]:
            FileName = random.choice(os.listdir("Custom-Backgrounds"))
        else:
            url = random.choice(s["night-backgrounds"]["links"])

    if url:
        Path = os.getcwd() + '\\Downloaded-Images\\' + url.split('/')[-1]
        urllib.request.urlretrieve(url, Path)
    else:
        Path = os.getcwd() + '\\Custom-Backgrounds\\' + FileName

    if night:
        try:
            image = Image.open(Path)
            image.format
        except:
            return "No Image Found - Please Populate Custom-Backgrounds", None
        return Path, url
    return Path, Data


def IsNight():
    from astral.sun import sun
    from astral import LocationInfo
    from datetime import datetime

    city = LocationInfo(s["night-backgrounds"]["city"])
    sunTime = sun(city.observer, date=datetime.now())
    if datetime.now().time() >= sunTime["sunset"].time() or datetime.now().time() <= sunTime["sunrise"].time():
        return True


def main():
    if not os.path.exists('Downloaded-Images'):
        os.makedirs('Downloaded-Images')
    if not s["night-backgrounds"]["links"] and not os.path.exists('Custom-Backgrounds'):
        os.makedirs('Custom-Backgrounds')
        f = open("Custom-Backgrounds\\PUT CUSTOM IMAGES IN HERE (CAN BE ANY NORMAL IMAGE TYPE)", "x")

    Night = False
    if s["night-backgrounds"]["city"] and s["night-backgrounds"]["toggle"]:
        Night = IsNight()

    if Night:
        path, link = FetchImage(True, None)
        FileName = (path.split('\\')[-1])
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        Notify("New Background from Custom-Backgrounds", FileName, False, None, FileName)
    else:
        path, data = FetchImage(False, jsonFetch(random.choice(SETTINGS['subreddits'])))
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        Notify(f"New Background from {data['subreddit']}", f"{data['title']}", f"https://reddit.com{data['permalink']}",
               "reddit.ico", False)


if __name__ == "__main__":
    main()
