import json, urllib.request, os, ctypes, time, random
from datetime import datetime; from astral import Astral
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SETTINGS = {
    "blacklist": [],
    "subreddits": ['earthporn'],
    "night-backgrounds": True,
    "city": 'London'
}

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Image Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
def ImageFilter(x, y, url):
    if x < y:
        return False
    if x <= 2560:
        return False
    if y <= 1440:
        return False
    for v in SETTINGS["blacklist"]:
        if url.includes(v):
            return False
    return True

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Find the image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
def FetchImage(subreddits):
    searchLimit = 5
    subreddit = random.choice(subreddits)

    # Fetch the JSON
    req = urllib.request.Request(f'https://www.reddit.com/r/{subreddit}/top.json', headers = {'User-agent': 'Reddit Background Setter (Created by u/Core_UK and u/Member87)'})
    res = urllib.request.urlopen(req)
    j = json.load(res)

    # Assign the search limit by getting the length of the JSON
    searchLimit = len(j['data']['children'])

    current = 0
    image = None

    while not image:
        data = j['data']['children'][current]['data']

        try:
            img = data['preview']['images'][0]['source']
            url = data['url_overridden_by_dest']
            if ImageFilter(img['width'], img['height'], url):
                image = url
            else:
                current += 1
        except:
            current += 1

        if current >= searchLimit:
            image = j['data']['children'][0]['data']['url_overridden_by_dest']

    name = image.split('/')[-1]
    j = j['data']['children'][current]['data']

    # Fetch the image
    urllib.request.urlretrieve(image, name)

    return name, j

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Initial Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
if (SETTINGS["night-backgrounds"] and not os.path.exists('night-backgrounds')):
    os.makedirs('night-backgrounds')
    input("Please populate the night-backgrounds directory with images you would like to use at night. Press ENTER to continue...")

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check if its Night
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''

a = Astral()
a.solar_depression = 'civil'
city = a[SETTINGS["city"]]
s = city.sun(date=datetime.now(), local=True)

if (SETTINGS["night-backgrounds"] and datetime.now().time() >= s["sunset"].time() or datetime.now().time() <= s["sunrise"].time()):
    ''' ~~~~~~~~~~~~~~~~~~~~~~~~~
    Sets the Night Background
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
    name = random.choice(os.listdir(os.getcwd() + "\\night-backgrounds"))
    print(f"The chosen image was '{name}'.")
    path = os.getcwd() + '\\night-backgrounds\\' + name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
else:
    ''' ~~~~~~~~~~~~~~~~~~~~~~~~~
    Sets the Day Background
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
    name, json = FetchImage(SETTINGS["subreddits"]) # Run the function to fetch the image
    print(f"The chosen image was '{name}' | Subreddit: r/{json['subreddit']} | Title: '{json['title']}' | User: u/{json['author']}.")
    path = os.getcwd() + '\\' + name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    # Delete the File After the background has been set
    time.sleep(2)
    os.remove(path)
