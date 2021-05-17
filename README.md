# Reddit Background Changer
A simple python script that fetches an image from your desired subreddit and sets it to your background.

## Features
- Pick your favourite subreddits
- Custom background to use at night (Either from an image on the internet or from your PC)
- Notification when you get a new background.
- Blacklist images you dont like
- Get images tailored to your resolution
- Many more features are shown in the config below, so take a look at that if you want some more insight into what this script can do.

## Required Modules
- [PyWin32](https://pypi.org/project/pywin32/)
- [Win10Toast-Click](https://pypi.org/project/win10toast-click/)
- [Astral](https://pypi.org/project/astral/) - Optional if you want to use the night backgrounds (Remove it from the imports if you don't want to use it)

## Configuration
*Create a file called `config.py` and copy all the contents of [template_config.py](https://github.com/coredev-uk/reddit-background-changer/blob/main/template_config.py#L3) then edit all you want.*
```python
SETTINGS = {
    "blacklist": [], # Add the image ID or if you use save-images you can use the file name of what you'd not like to see in the future
    "subreddits": ['EarthPorn'], # Add your subreddit's here, its randomised each time its ran, so it'll be one from the list (it can just be one subreddit if you'd just like that)
    "diff-bg": False, # This just gives you a different background from reddit everytime it checks, I suggest not turning it on if you run the script very often as it will run out of images and default to the first one after.
    "monitor-x": "", # This is your monitor x resolution of your highest resolution monitor (I.e. 1920 for a 1920x1080 (1080p) display) - Leave this empty if you would like it to auto-detect your primary display resolution. (and if you have a single monitor)
    "monitor-y": "", # This is your monitor y resolution of your highest resolution monitor (I.e. 1080 for a 1920x1080 (1080p) display) - Leave this empty if you would like it to auto-detect your primary display resolution. (and if you have a single monitor)
    "night-backgrounds": {
        "toggle": True, # Do you want to enable different backgrounds at night (Sunset to Sunrise using Astral)
        "diff-bg": False,
        "methods": {
            "chosen-method": "All", # Link / Local / Subreddit / All | Do you want night backgrounds to be fetched from Local (Your custom path), Link (From links below), Subreddit (Also below) or all where it just randomises.
            "links": [], # This pretty much is the options you have for where you get your backgrounds at night
            "subreddits": [], # This is the method you chose to use, this can be either Link, Local, Subreddit or All. These will be explained below.
            "local": False, # This enables the use of custom images, that you can store in your own custom directory, or the one already made in `img/bg_custom`. Images need to be PNG/JPG/JPEG format, and it picks a random one from the file, so only put one in there if you just want one being used.
        },
        "city": 'London', # If you are using night-backgrounds, you will need to put your local large city in here. Check https://astral.readthedocs.io/en/latest/#cities list to find the closest one to you.
        "notify": False # This is if you would like to be notified if you got a new background at night. This occurs every time you run the script if you use custom method.
    },
    "downloaded-path": os.getcwd() + "\\img\\bg_Downloaded\\", # This is for the directory where you would like images to be downloaded to and stored.
    "custom-path": os.getcwd() + "\\img\\bg_Custom\\", # This is where you can put your custom images that is used for night backgrounds, if you're not using night backgrounds just leave this default.
    "active-path": os.getcwd() + "\\img\\bg_Active\\", # I also suggest leaving this default. This is where your active background images is stored (aside from if you use custom backgrounds).
    "imgur": { # This feature allows you to put imgur albums in your links table, you need to go to https://api.imgur.com/oauth2/addclient and create an application if you'd like to use this feature.
        "client_id": "", 
        "client_secret": "",
        "album_max": 25
    }
}
```

## Task Scheduler Setup
1. Open `taskschd.msc` and on the right panel there is an option to **Import Task**, click that.
2. Navigate to your Reddit-Background-Changer install and go into the bin folder.
3. Click on `Reddit Background Changer.xml` and this should open a prompt in Task Scheduler.
4. In this prompt you need to go to **Actions** and edit the 'Start a program' action.
5. All you need to do is change the 'Start in' box to the path of your reddit-background-changer install (I.e. C:\Users\%LOCALUSER%\Downloads)
*You can repeat all the previous if you wish to use the directory cleaner (this just wipes the images daily to optimise storage) as well.*

## Final Notes
With the blacklist, to get the image ID you just look at the link of the post.

![Reddit Image ID](https://i.imgur.com/E2AQYv0.png "Reddit Image ID")

You can open the page of your background by clicking on the notification of when your wallpaper changes, or you can find it on your chosen subreddit.
- [Link to some good subreddits](https://www.reddit.com/r/sfwpornnetwork/wiki/network)

## Credits
[Member87](https://github.com/member87) - Made the base script and helped out with additions I made

## Alternatives
I highly recommend [Reddit-Wallpaper](https://github.com/Mamiglia/Reddit-Wallpaper) by Mamaiglia is you are looking for a UI based Reddit Wallpaper Changer.