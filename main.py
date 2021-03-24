import json, urllib.request, os, ctypes, time, random
from datetime import datetime; from astral.sun import sun; from astral import LocationInfo
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
SETTINGS = {
    "blacklist": [],
    "subreddits": ['earthporn'],
    "night-backgrounds": True
}

if SETTINGS["night-backgrounds"] and not os.path.exists('night-backgrounds'):
    os.makedirs('night-backgrounds')
    input("Please populate the night-backgrounds directory with images you would like to use at night. Press ENTER to continue...")

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Image Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
def ImageFilter(x, y, url):
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
def FetchImage(subreddits):
    searchLimit = 5
    subreddit = random.choice(subreddits)
    req = urllib.request.Request(f'https://www.reddit.com/r/{subreddit}/top.json', headers = {'User-agent': 'Backgound Setter'})
    res = urllib.request.urlopen(req)
    j = json.load(res)
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
    return image, name, j, current

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check if its Night
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
current_time = datetime.now().time()
s = sun(LocationInfo("London", "England", "Europe/London", 51.5, -0.116).observer, date=datetime.now())

if (SETTINGS["night-backgrounds"] and current_time >= s["sunset"].time() or current_time <= s["sunrise"].time()):
    ''' ~~~~~~~~~~~~~~~~~~~~~~~~~
    Sets the Night Background
    ~~~~~~~~~~~~~~~~~~~~~~~~~ '''
    name = random.choice(os.listdir(os.getcwd() + "\\night-backgrounds"))
    print(f"The chosen image was '{name}'.")
    path = os.getcwd() + '\\night-backgrounds\\' + name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
else:
    ''' ~~~~~~~~~~~~~~~~~~~~~~~~~
    Sets the Day Background
    ~~~~~~~~~~~~~~~~~~~~~~~~~ '''
    image, name, j, current = FetchImage(SETTINGS["subreddit"], SETTINGS['searchLimit']) # Run the function to fetch the image
    urllib.request.urlretrieve(image, name)
    print(f"The chosen image was '{name}' | Subreddit: r/{SETTINGS['subreddit']} | Title: '{j['data']['children'][current]['data']['title']}' | User: u/{j['data']['children'][current]['data']['author']}.")
    path = os.getcwd() + '\\' + name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    time.sleep(2)
    os.remove(path)