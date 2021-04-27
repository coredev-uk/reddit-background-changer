import json, urllib.request, os, ctypes, time, random, webbrowser, functools
from datetime import datetime
from astral.sun import sun
from astral import LocationInfo
from win32api import GetSystemMetrics
from win10toast_click import ToastNotifier

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Settings - Here is where you can configure the script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SETTINGS = {
    "blacklist": [],
    "subreddits": ['EarthPorn'],
    "use-cache": False,
    "night-backgrounds": True, # this should be a list ["https://image.com/img.png", "https://image.com/img.jpg"] just using this as i use custom backgrounds
    "city": 'London'
}

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Functions - Do not Touch Anything Below Here - Do not Touch Anything Below Here - Do not Touch Anything Below Here - 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''


@functools.lru_cache(maxsize=len(SETTINGS['subreddits']))
def jsonFetch(subreddit):
    req = urllib.request.Request(f'https://www.reddit.com/r/{subreddit}/top.json', headers={
        'User-agent': 'Reddit Background Setter (Created by u/Core_UK and u/Member87)'})
    res = urllib.request.urlopen(req)
    j = json.load(res)
    return j


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
    link = None

    if not night:
        searchLimit = len(j['data']['children'])
        current = 0
        while not link:
            data = j['data']['children'][current]['data']
            try:
                img = data['preview']['images'][0]['source']
                url = data['url_overridden_by_dest']
                if ImageFilter(img['width'], img['height'], data):
                    link = url
                else:
                    current += 1
            except:
                current += 1

            if current >= searchLimit:
                link = j['data']['children'][0]['data']['url_overridden_by_dest']
    else:
        if SETTINGS["night-backgrounds"] and not os.path.exists('Custom-Backgrounds'):
            link = random.choice(SETTINGS["night-backgrounds"])

    if link:
        name = link.split('/')[-1]
        urllib.request.urlretrieve(link, name)
    else:
        name = random.choice(os.listdir("Custom-Backgrounds"))

    path = os.getcwd() + '\\Downloaded-Images\\' + name
    if not link: path = os.getcwd() + '\\Custom-Backgrounds\\' + name

    if night: return path, link
    return path, data


''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
if not os.path.exists('Downloaded-Images'):
    os.makedirs('Downloaded-Images')



city = LocationInfo(SETTINGS["city"]);
s = sun(city.observer, date=datetime.now())
path, data = None, None

if (SETTINGS["night-backgrounds"] and datetime.now().time() >= s["sunset"].time() or datetime.now().time() <= s["sunrise"].time()):  # night
    path, link = FetchImage(True, None)
    link_extension = (path.split('\\')[-1]).split(".", 1)[0]
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
else:
    cached_hits = jsonFetch.cache_info().hits
    SETTINGS['subreddit'] = random.choice(SETTINGS['subreddits'])
    j = jsonFetch(SETTINGS['subreddit'])
    if SETTINGS["use-cache"] and jsonFetch.cache_info().hits > cached_hits:
        path, data = FetchImage(False, j)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    else:
        path, data = FetchImage(False, j)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

if data:
    toaster = ToastNotifier()


    def toasterCallback():
        webbrowser.open_new(f"https://reddit.com{data['permalink']}")


    toaster.show_toast(f"New Background from {data['subreddit']}", f"{data['title']}", icon_path="reddit.ico",
                       duration=None, threaded=True, callback_on_click=toasterCallback)
