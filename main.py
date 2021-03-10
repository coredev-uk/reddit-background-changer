import json, urllib.request, os, ctypes, time, sys
from datetime import datetime
from astral.sun import sun
from astral import LocationInfo

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SETTINGS = {
    "searhLimit": 5,
    "blacklist": [],
    "subreddit": 'earthporn',
    "dark-background-at-night": False,
    "dark-background": 'grey.png'
}

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Image Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
def Filter(x, y, url):
    if not x > y:
        return False
    if not x >= 2560:
        return False
    if not y >= 1440:
        return False
    for x in SETTINGS["blacklist"]:
        if url.includes(x):
            return False
    return True

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Find the image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
req = urllib.request.Request(f'https://www.reddit.com/r/{SETTINGS["subreddit"]}/top.json', headers = {'User-agent': 'Backgound Setter'})
res = urllib.request.urlopen(req)
j = json.load(res)
SETTINGS['searhLimit'] = len(j['data']['children'])
current = 0
image = None

while not image:
    data = j['data']['children'][current]['data']

    try:
        img = data['preview']['images'][0]['source']
        url = data['url_overridden_by_dest']
        if Filter(img['width'], img['height'], url):
            image = url
        else:
            current += 1
    except:
        current += 1

    if current >= SETTINGS["searhLimit"]:
        image = j['data']['children'][0]['data']['url_overridden_by_dest']

name = image.split('/')[-1]
urllib.request.urlretrieve(image, name)

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check if its Night
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SPI_SETDESKWALLPAPER = 20

if (SETTINGS["dark-background-at-night"]): 
    now = datetime.now()
    now_time = datetime.now().time()
    city = LocationInfo("Dover", "England", "Europe/London", 51.154323, 1.290054)
    s = sun(city.observer, date=now)

    if now_time >= s["sunset"].time() or now_time <= s["sunrise"].time():
        name = SETTINGS["dark-background"]
        print(f"The chosen image was '{name}'")
        path = os.getcwd() + '\\' + name
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
    else:
        print(f"The chosen image was '{name}' | Subreddit: r/{SETTINGS['subreddit']} | Title: '{j['data']['children'][current]['data']['title']}' | User: u/{j['data']['children'][current]['data']['author']}.")
        path = os.getcwd() + '\\' + name
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
        os.remove(os.path.join(os.getcwd(), name))

else:
    print(f"The chosen image was '{name}' | Subreddit: r/{SETTINGS['subreddit']} | Title: '{j['data']['children'][current]['data']['title']}' | User: u/{j['data']['children'][current]['data']['author']}.")
    path = os.getcwd() + '\\' + name
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
    os.remove(os.path.join(os.getcwd(), name))