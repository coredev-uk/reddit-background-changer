# func.py

import json
import urllib.request
import webbrowser
import os
import random
from config import SETTINGS as s
from PIL import Image


def jsonFetch(subreddit):
    req = urllib.request.Request(f'https://www.reddit.com/r/{subreddit}/top.json', headers={
        'User-agent': 'Reddit Background Setter (Created by u/Core_UK and u/Member87)'})
    res = urllib.request.urlopen(req)
    j = json.load(res)
    return j


def Notify(msg, title, link, icon, path):
    def linkOpen():
        if not link:
            img = Image.open(path)
            img.show()
        else:
            webbrowser.open_new(link)

    from win10toast_click import ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast(msg, title, icon_path=icon,
                       duration=None, threaded=True, callback_on_click=linkOpen)


def IsNight():
    from astral.sun import sun
    from astral import LocationInfo
    from datetime import datetime

    # wipes downloaded images folder for the 'caching' method
    if os.listdir("Downloaded-Images"):
        for f in os.listdir("Downloaded-Images"):
            os.remove(os.path.join("Downloaded-Images", f))

    city = LocationInfo(s["night-backgrounds"]["city"])
    sunTime = sun(city.observer, date=datetime.now())
    if datetime.now().time() >= sunTime["sunset"].time() or datetime.now().time() <= sunTime["sunrise"].time():
        return True


def ImageFilter(x, y, data):
    if not x > y:
        return False
    if not x >= s["monitor-x"]:
        return False
    if not y >= s["monitor-y"]:
        return False
    for v in s["blacklist"]:
        if v in data['id'] or v in data['url_overridden_by_dest']:
            return False
    if s["diff-bg"] and os.path.exists(os.getcwd() + "\\Downloaded-Images\\" + data['url_overridden_by_dest'].split('/')[-1]):
        return False

    return True


def FetchRedditImage(j):
    url = None
    current = 0
    searchLimit = len(j['data']['children'])

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

    Path = os.getcwd() + '\\Downloaded-Images\\' + url.split('/')[-1]
    if os.path.exists(Path):
        return Path, Data, True
    urllib.request.urlretrieve(url, Path)
    try:
        image = Image.open(Path)
        image.format
    except:
        return "No Image Found in the Correct Format. - Recommended to use a difference subreddit.", Data, False
    return Path, Data, False


def FetchImage():
    if os.path.exists('Custom-Backgrounds') and not s["night-backgrounds"]["links"]:
        FileName = random.choice(os.listdir("Custom-Backgrounds"))
        Path = os.getcwd() + '\\Custom-Backgrounds\\' + FileName
        url = False
    else:
        url = random.choice(s["night-backgrounds"]["links"])
        Path = os.getcwd() + '\\Downloaded-Images\\' + url.split('/')[-1]
        if os.path.exists(Path):
            return Path, url
        urllib.request.urlretrieve(url, Path)

    try:
        image = Image.open(Path)
        image.format
    except:
        return "No Image Found in the Correct Format - Please check your links or your Custom-Backgrounds directory.", url
    return Path, url