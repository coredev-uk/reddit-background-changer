import json
import urllib.request
import os
import ctypes
import random
from datetime import datetime
from astral.sun import sun
from astral import LocationInfo

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SETTINGS = {
    "searhLimit": 5,
    "subreddits-night": ['spaceporn'], #sunset
    "subreddits-day": ['earthporn'] #skyporn
}

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check if its Night
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
now = datetime.now() 
now_time = now.time()
city = LocationInfo("Dover", "England", "Europe/London", 51.154323, 1.290054)
s = sun(city.observer, date=now)

if now_time >= s["sunset"].time() or now_time <= s["sunrise"].time():
    SETTINGS["subreddit"] = random.choice(SETTINGS["subreddits-night"])
else:
    SETTINGS["subreddit"] = random.choice(SETTINGS["subreddits-day"])

print(f'The chosen category is {SETTINGS["subreddit"]}.')

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
req = urllib.request.Request(f'https://www.reddit.com/r/{SETTINGS["subreddit"]}/top.json', headers = {'User-agent': 'Backgound Setter'})
res = urllib.request.urlopen(req)
j = json.load(res)
SETTINGS['searhLimit'] = len(j['data']['children'])
image = None
current = 0

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Image Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
def Filter(x, y, url):
    if not x > y:
        return False
    if not x >= 1920:
        return False
    if not y >= 1080:
        return False
    # if not url.includes('.png') or not url.includes('.jpg') or not url.includes('.jpeg'):
        # return False
    return True

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Find the image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
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

if not os.path.exists('images'):
    os.makedirs('images')

name = 'images\\' + image.split('/')[-1]
urllib.request.urlretrieve(image, name)

path = os.getcwd() + '\\' + name
SPI_SETDESKWALLPAPER = 20

ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

print(f"The chosen image is {j['data']['children'][current]['data']['title']} by the user u/{j['data']['children'][current]['data']['author']}.")