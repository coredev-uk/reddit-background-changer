import json, urllib.request, os, ctypes, time, random, webbrowser;from datetime import datetime;from astral.sun import sun; from astral import LocationInfo;from win32api import GetSystemMetrics;from win10toast_click import ToastNotifier 

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
    if not x > y:
        return False
    if not x >= GetSystemMetrics(0):
        return False
    if not y >= GetSystemMetrics(1):
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

    # Fetch the image
    urllib.request.urlretrieve(image, name)

    return name, j, current

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Initial Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
if (SETTINGS["night-backgrounds"] and not os.path.exists('night-backgrounds')):
    os.makedirs('night-backgrounds')
    input("Please populate the night-backgrounds directory with images you would like to use at night. Press ENTER to continue...")

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check if its Night
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''

city = LocationInfo(SETTINGS["city"])
s = sun(city.observer, date=datetime.now())

if (SETTINGS["night-backgrounds"] and datetime.now().time() >= s["sunset"].time() or datetime.now().time() <= s["sunrise"].time()):
    # night
    name = random.choice(os.listdir(os.getcwd() + "\\night-backgrounds"))
    print(f"The chosen image was '{name}'.")
    path = os.getcwd() + '\\night-backgrounds\\' + name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
else:
    # day
    name, j, current = FetchImage(SETTINGS["subreddits"]) # Run the function to fetch the image
    print(f"The chosen image was '{name}' | Subreddit: r/{j['data']['children'][current]['data']['subreddit']} | Title: '{j['data']['children'][current]['data']['title']}' | User: u/{j['data']['children'][current]['data']['author']}.")
    path = os.getcwd() + '\\' + name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    def clickCallback():
        try: 
            webbrowser.open_new(f"https://reddit.com{j['data']['children'][current]['data']['permalink']}")
        except: 
            print('Win10Toast Link Open Error')

    # win10toast
    try:
        toaster = ToastNotifier()
        toaster.show_toast(
            f"New Background from {j['data']['children'][current]['data']['subreddit']}", # title
            f"{j['data']['children'][current]['data']['title']}", # message 
            icon_path="reddit.ico", # 'icon_path' 
            duration=None, # for how many seconds toast should be visible; None = leave notification in Notification Center
            threaded=True, # True = run other code in parallel; False = code execution will wait till notification disappears 
            callback_on_click=clickCallback # click notification to run function 
        )
    except:
        print("Win10Toast Creation Error")

    # Delete the File After the background has been set
    time.sleep(2)
    os.remove(path)
