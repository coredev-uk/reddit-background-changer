# func.py

import json
import urllib.request
import webbrowser
import os
import random
import logging
import shutil
from datetime import datetime
from config import SETTINGS as s, debug, debugNight, debugNotify
from imgurpython import ImgurClient

def calculate_aspect(width: int, height: int) -> str:
    def gcd(a, b):
        """The GCD (greatest common divisor) is the highest number that evenly divides both width and height."""
        return a if b == 0 else gcd(b, a % b)

    r = gcd(width, height)
    x = int(width / r)
    y = int(height / r)

    return f"{x}:{y}"


def logging_init():
    if debug:
        logging.basicConfig(filename='console.log', level=logging.DEBUG)  # Setup logging
        file = open("console.log", "r+")
        file.truncate(0)
        file.close()
        log('[Init] RedditBackgroundChanger Log Initialised.')
    if not debug and os.path.exists('console.log'):
        os.remove('console.log')


def log(message):
    if not debug: return
    now = datetime.now()
    print(f'{now.strftime("%H:%M:%S [%d.%m.%Y]")} | {message}')
    logging.debug(f'{now.strftime("%H:%M:%S [%d.%m.%Y]")} | {message}')


def jsonFetch(subreddit):
    log(f'[jsonFetch] Running')
    log(f'[jsonFetch] Subreddit: {subreddit}')
    req = urllib.request.Request(f'https://www.reddit.com/r/{subreddit}/top.json', headers={
        'User-agent': 'Reddit Background Setter (Created by u/Core_UK and u/Member87)'})
    res = urllib.request.urlopen(req)
    j = json.load(res)
    return j


def Notify(msg, title, link, icon, path):
    def linkOpen():
        if not link:
            from PIL import Image
            img = Image.open(path)
            img.show()
        else:
            webbrowser.open_new(link)

    from win10toast_click import ToastNotifier
    log(f'[Notify] -------------------------------------NEW NOTIFICATION------------------------------------')
    log(f'[Notify] Running')
    log(f'[Notify] Message: {msg}')
    log(f'[Notify] Title: {title}')
    log(f'[Notify] Link: {link}')
    log(f'[Notify] Icon: {icon}')
    log(f'[Notify] Path: {path}')
    log(f'[Notify] -----------------------------------------------------------------------------------------')
    toaster = ToastNotifier()
    toaster.show_toast(msg, title, icon_path=icon,
                       duration=None, threaded=True, callback_on_click=linkOpen)


def IsNight(city):
    if not s['night-backgrounds']['toggle']: return False
    from astral.sun import sun
    from astral import LocationInfo
    log(f'[IsNight] ----------------------------------------------------------------------------------------')
    log('[IsNight] Running')
    city = LocationInfo(city)
    sunTime = sun(city.observer, date=datetime.now())
    sunset = sunTime['sunset'].time()
    sunrise = sunTime['sunrise'].time()
    currentTime = datetime.now().time()
    log(f'[IsNight] The current time is {currentTime}')
    log(f'[IsNight] Sunset is at {sunset}')
    log(f'[IsNight] Sunrise is at {sunrise}')
    if debugNight:
        log(f'[IsNight] Debug Override')
        log(f'[IsNight] Output: {True}')
        log(f'[IsNight] ----------------------------------------------------------------------------------------')
        return True
    if currentTime >= sunset or currentTime <= sunrise:
        log(f'[IsNight] Output: {True}')
        log(f'[IsNight] ----------------------------------------------------------------------------------------')
        return True
    log(f'[IsNight] ----------------------------------------------------------------------------------------')
    log(f'[IsNight] Output: {False}')
    return False


def ImageFilter(x, y, data, night):
    FileType = (data['url_overridden_by_dest'].split('/')[-1]).split('.')[-1]
    FileID = (data['url_overridden_by_dest'].split('/')[-1]).split('.')[-2]
    ExistCheckActive = os.path.join(s['active-path'], data['url_overridden_by_dest'].split('/')[-1])
    ExistCheckDownload = os.path.join(s['downloaded-path'], data['url_overridden_by_dest'].split('/')[-1])
    log(f'[ImageFilter] ----------------------------------------NEW IMAGE-----------------------------------')
    log(f'[ImageFilter][New Filter] FileType: {FileType}')
    log(f'[ImageFilter][New Filter] FileID: {FileID}')

    if not x > y:
        log(f'[ImageFilter][Landscape Check] Failed for {FileID}')
        log(f'[ImageFilter][Landscape Check] Got {x}x{y}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    if not x >= s['res']['monitor-x']:
        log(f'[ImageFilter][Resolution Check - X] Failed for {FileID}')
        log(f'[ImageFilter][Resolution Check - X] Got {x} | Needed {s["res"]["monitor-x"]}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    if not y >= s['res']['monitor-y']:
        log(f'[ImageFilter][Resolution Check - Y] Failed for {FileID}')
        log(f'[ImageFilter][Resolution Check - Y] Got {y} | Needed {s["res"]["monitor-y"]}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    if calculate_aspect(x, y) != s['res']['aspect-ratio']:
        log(f'[ImageFilter][Aspect Ratio Check] Failed for {FileID}')
        log(f'[ImageFilter][Aspect Ratio Check] Got {calculate_aspect(x, y)} | Needed {s["res"]["aspect-ratio"]}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    if x >= s['res']['max-x']:
        log(f'[ImageFilter][Max Resolution Check - X] Failed for {FileID}')
        log(f'[ImageFilter][Max Resolution Check - X] Got {x} | Needed {s["res"]["max-x"]}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    if y >= s['res']['max-y']:
      log(f'[ImageFilter][Max Resolution Check - Y] Failed for {FileID}')
      log(f'[ImageFilter][Max Resolution Check - Y] Got {y} | Needed {s["res"]["max-y"]}')
      log(f'[ImageFilter] ------------------------------------------------------------------------------------')
      return False
    if FileType != 'jpeg' and FileType != 'png' and FileType != 'jpg':
        log(f'[ImageFilter][File Type Check] Failed for {FileID}')
        log(f'[ImageFilter][File Type Check] Got {FileType}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    if (s['diff-bg'] or (night and s['night-backgrounds']['diff-bg'])) and (os.path.exists(ExistCheckActive) or os.path.exists(ExistCheckDownload)):
        log(f'[ImageFilter][File Exists Check] Failed for {FileID}')
        log(f'[ImageFilter] ------------------------------------------------------------------------------------')
        return False
    for v in s['blacklist']:
        if FileID == v:
            log(f'[ImageFilter] Blacklist Check Failed for {FileID}')
            log(f'[ImageFilter] ------------------------------------------------------------------------------------')
            return False
    log(f'[ImageFilter][Filter Passed] {FileID} Passed Checks.')
    log(f'[ImageFilter] ------------------------------------------------------------------------------------')
    return True


def DownloadImage(url, FileName):
    PathDownloaded = os.path.join(s['downloaded-path'], FileName)
    PathActive = os.path.join(s['active-path'], FileName)
    log(f'[DownloadImage] ---------------------------------------NEW IMAGE----------------------------------')
    log('[DownloadImage] Running')
    if os.path.exists(PathDownloaded):
        log(f'[DownloadImage] Output: {PathDownloaded}')
        log(f'[DownloadImage] Exists: {True}')
        log(f'[DownloadImage] ----------------------------------------------------------------------------------')
        return PathDownloaded, True
    if os.path.exists(PathActive):
        log(f'[DownloadImage] Output: {PathActive}')
        log(f'[DownloadImage] Exists: {True}')
        log(f'[DownloadImage] ----------------------------------------------------------------------------------')
        return PathActive, True
    log(f'[DownloadImage] Action: Downloading Image from {url}')
    urllib.request.urlretrieve(url, PathDownloaded)
    log(f'[DownloadImage] Output: {PathDownloaded}')
    log(f'[DownloadImage] Exists: {False}')
    log(f'[DownloadImage] ----------------------------------------------------------------------------------')
    return PathDownloaded, False


def FetchImageFromDirectory():
    log('[FetchImageFromDirectory] Running')
    FileName = random.choice(os.listdir(s['custom-path']))
    Path = s['custom-path'] + FileName
    log(f'[FetchImageFromDirectory] Output: {Path}')
    return Path


def FetchImageFromLink():
    log('[FetchImageFromLink] Running')
    linkList = s['night-backgrounds']['methods']['links']
    if (s['imgur']['client_id'] and s['imgur']['client_secret']):
        client = ImgurClient(s['imgur']['client_id'], s['imgur']['client_secret'])
        imgurAlbum = []
        for value in linkList:
            val = value.split(':')
            if val[0] != 'http' or val[0] != 'https':
                try:
                    a = client.get_album(value)
                    log(f'[FetchImageFromLink][ImgurAlbum] Found Album: {a.title}')
                    imgurAlbum.append(a.id)
                    linkList.remove(value)
                except:
                    continue
        current = 0
        for v in imgurAlbum:
            for image in client.get_album_images(v):
                log(f'[FetchImageFromLink][ImgurAlbum] Adding {image.link} to Links list.')
                linkList.append(image.link)
                current = current + 1
                if current >= s['imgur']['album_max']:
                    break
    ChosenLink = random.choice(linkList)
    FileName = ChosenLink.split('/')[-1]
    Path, Exists = DownloadImage(ChosenLink, FileName)
    log(f'[FetchImageFromLink] Output: {Path} [{ChosenLink}]')
    log(f'[FetchImageFromLink] Exists: {Exists}')
    return Path, Exists, ChosenLink


def FetchImageFromReddit(j, Night):
    log('[FetchImageFromReddit] Running')
    url = None
    current = 0
    searchLimit = len(j['data']['children'])

    log(f'[FetchImageFromReddit] Starting File Search for Image with Correct Parameters. SearchLimit: {searchLimit}')
    while not url:
        Data = j['data']['children'][current]['data']
        try:
            img = Data['preview']['images'][0]['source']
            FoundURL = Data['url_overridden_by_dest']
            if ImageFilter(img['width'], img['height'], Data, Night):
                url = FoundURL
            else:
                current = current + 1
        except:
            current = current + 1

        log(f'[FetchImageFromReddit] Current: {current}')
        if current >= searchLimit:
            log('[FetchImageFromReddit] Exceeded searchLimit - 1st Image being set as background.')
            url = j['data']['children'][0]['data']['url_overridden_by_dest']

    FileName = url.split('/')[-1]

    Path, Exists = DownloadImage(url, FileName)

    if debugNotify or (not Exists and s['notify']):
        Notify(f"New Background from {Data['subreddit']}", f"{Data['title']}", f'https://reddit.com{Data["permalink"]}',
                "bin/reddit.ico", False)
    
    log(f'[FetchImageFromReddit] ---------------------------IMAGE DETAILS-----------------------------------')
    log(f'[FetchImageFromReddit] FileName: {FileName}')
    log(f'[FetchImageFromReddit] Path: {Path}')
    log(f'[FetchImageFromReddit] Link: {url} | Permanent: https://reddit.com{Data["permalink"]}')
    log(f'[FetchImageFromReddit] Output: Image Path ({Path}), File Exists ({Exists}), ImageData')
    log(f'[FetchImageFromReddit] ---------------------------------------------------------------------------')
    return Path


def FetchMethod(method):
    method = method.lower()
    if method == 'all':
        methodList = []
        if s['night-backgrounds']['methods']['links']: methodList.append('link')
        if s['night-backgrounds']['methods']['subreddits']: methodList.append('subreddit')
        if s['night-backgrounds']['methods']['local'] and os.listdir(s['custom-path']): methodList.append('local')
        method = random.choice(methodList)
    return method


def NightImageFetch(method):
    log(f'[NightImageFetch] --------------------------------NIGHT IMAGE FETCH-------------------------------')
    log('[NightImageFetch] Running')
    log(f'[NightImageFetch] Method: {method}')
    Path, Exists, Data, Title, Source, Link = False, False, False, False, False, False

    if method == 'local':
        Path = FetchImageFromDirectory()
        Source = 'Custom Backgrounds'
        Title = Path.split('\\')[-1]

    if method == 'subreddit':
        Path, Exists, Data = FetchImageFromReddit(jsonFetch(random.choice(s['night-backgrounds']['methods']['subreddits'])), True)
        Source = Data['subreddit']
        Title = Data['title']
        Link = Data['url_overridden_by_dest']

    if method == 'link':
        Path, Exists, Data = FetchImageFromLink()
        Source = (((Data.split('//')[-1]).split('/')[-2])[2:])
        Title = Path.split('\\')[-1]
        Link = Data

    if debugNotify or (not Exists and s['night-backgrounds']['notify']):
        Notify(f"New Background from {Source}", Title, Link, None, Path)

    log(f'[NightImageFetch] --------------------------------------------------------------------------------')
    log(f'[NightImageFetch] Output: {Path} [{Link}]')
    log(f'[NightImageFetch] Exists: {Exists}')
    log(f'[NightImageFetch] --------------------------------------------------------------------------------')
    return Path


def IsCurrentBackground(Path):
    log(f'[IsCurrentBackground] ----------------------------------NEW CHECK---------------------------------')
    log(f'[IsCurrentBackground] Running')
    FileName = Path.split('\\')[-1]
    for file in os.listdir(s['active-path']):
        log(f'[IsCurrentBackground] Current File: {file}')
        log(f'[IsCurrentBackground] Searching For: {FileName}')
        if file != FileName:
            if "custom" in file.split('_'):
                shutil.move(os.path.join(s['active-path'], file), os.path.join(s['custom-path'], file))
                log(f"[IsCurrentBackground] Moved {file} to Custom-Path from Active-Path")
            else:
                shutil.move(os.path.join(s['active-path'], file), os.path.join(s['downloaded-path'], file))
                log(f"[IsCurrentBackground] Moved {file} to Downloaded-Path from Active-Path")
        else:
            log(f"[IsCurrentBackground] {file} is the current active background.")
            log(f'[IsCurrentBackground] ----------------------------------------------------------------------------')
            return os.path.join(s['active-path'], file)

    NewPath = os.path.join(s['active-path'], FileName)
    shutil.move(Path, NewPath)
    if "custom" in FileName.split('_'):
        log(f"[IsCurrentBackground] Moved {FileName} to Active-Path from Custom-Path")
    else:
        log(f"[IsCurrentBackground] Moved {FileName} to Active-Path from Downloaded-Path")
    log(f'[IsCurrentBackground] ----------------------------------------------------------------------------')
    return NewPath


def GetCurrentBackground(activePath):
    Files = []
    for f in os.listdir(activePath):
        Files.append(f)
    if len(Files) == 1:
        return Files[0]