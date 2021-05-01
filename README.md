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
*Edit this in [config.py](https://github.com/coredev-uk/reddit-background-changer/blob/main/config.py#L3).*
```python
SETTINGS = {
    "blacklist": ['7t0swm'],
    "subreddits": ['EarthPorn', 'SkyPorn'],
    "diff-bg": False,
    "monitor-x": "",
    "monitor-y": "",
    "night-backgrounds": {
        "toggle": True,
        "methods": {
            "chosen-method": "All", # Link / Local / SubReddit / All
            "links": ["https://linktocoolthing"],
            "subreddits": ['SpacePorn'],
            "local": True,
        },
        "city": 'London',
        "notify": True
    },
    "downloaded-path": os.getcwd() + "\\img\\bg_Downloaded\\",
    "custom-path": os.getcwd() + "\\img\\bg_Custom\\",
    "active-path": os.getcwd() + "\\img\\bg_Active\\"
}
```

## Explanation of Configuration ["SETTINGS"]
- Blacklist [`blacklist`] -  Add the image ID or if you use save-images you can use the file name of what you'd not like to see in the future
- Subreddits [`subreddits`] - Add your subreddit's here, its randomised each time its ran, so it'll be one from the list (it can just be one subreddit if you'd just like that)
- Difference Backgrounds [`diff-bg`] - This just gives you a different background from reddit everytime it checks, I suggest not turning it on if you run the script very often as it will run out of images and default to the first one after.
- Monitor X Resolution [`monitor-x`] - This is your monitor x resolution of your highest resolution monitor (I.e. 1920 for a 1920x1080 (1080p) display) - Leave this empty if you would like it to auto-detect your primary display resolution. (and if you have a single monitor)
- Monitor Y Resolution [`monitor-y`] - This is your monitor y resolution of your highest resolution monitor (I.e. 1080 for a 1920x1080 (1080p) display) - Leave this empty if you would like it to auto-detect your primary display resolution. (and if you have a single monitor)

### Night Backgrounds Explanation ["night-backgrounds"]
- Toggle [`toggle`] - Do you want to enable different backgrounds at night (Sunset to Sunrise using Astral)
- Methods: - This pretty much is the options you have for where you get your backgrounds at night
    - Chosen Method [`chosen-method`] - This is the method you chose to use, this can be either `Link`, `Local`, `Subreddit` or `All`. These will be explained below.
    - Links [`links`] - Here you can set links that you can set as your background at night, some links may not work and will need to be PNG/JPG/JPEG. Leave it empty if you don't want links to be used when using the `All` option above.
    - Subreddits [`subreddits`] - Just as with the day subreddits, you can set your own ones for night. Leave it empty if you don't want subreddit images to be used when using the `All` option for method.
    - Local [`local`] - This enables the use of custom images, that you can store in your own custom directory, or the one already made in `img/bg_custom`. Images need to be PNG/JPG/JPEG format, and it picks a random one from the file, so only put one in there if you just want one being used.
- City [`city`] - If you are using night-backgrounds, you will need to put your local large city in here. Check [this](https://astral.readthedocs.io/en/latest/#cities) list to find the closest one to you.
- Notify [`notify`] - This is if you would like to be notified if you got a new background at night. This occurs every time you run the script if you use `custom` method.

### Directory Configuration
- Downloaded Path [`downloaded-path`] - This is for the directory where you would like images to be downloaded to and stored.
- Custom Path [`custom-path`] - This is where you can put your custom images that is used for night backgrounds, if you're not using night backgrounds just leave this default.
- Active Path [`active-path`] - I also suggest leaving this default. This is where your active background images is stored (aside from if you use custom backgrounds).

## Task Scheduler Setup (Default Script)
1. Open Task Scheduler either through typing `taskschd.msc` in run or in your start menu or through finding the application.
2. Click on Task Scheduler Library and on the right it should say import task, click that.
3. Navigate to your install of `reddit-background-changer` and open the `bin` folder. Click on the `rbc.xml` file and this should start the import process.
4. In this you will need to edit the action and set program/script to your `pythonw.exe` path. This would usually be somewhere like this `C:\Users\user\AppData\Local\Programs\Python\Python39\pythonw.exe` if you have a default installation. Copy that and paste it in the Program/script field making sure you keep the surrounding quotation.
5. Then set the Start in field to where you have `reddit-background-changer` installed, and then you're pretty much done unless you'd like to change the default timing.
6. If you want to change the timing then go to Triggers and edit the One time trigger and change the Repeat task every to however much you'd like.

## Task Scheduler Setup (Directory Cleaner)
This is just a script that cleans the downloaded image's directory. I added this as it means if an image is used twice across the week, there is a chance you could see it again. It also helps save space, instead of following below you could just run the script if you'd prefer. Its called `_Directory_Clear.py`.
1. Open Task Scheduler either through typing `taskschd.msc` in run or in your start menu or through finding the application.
2. Click on Task Scheduler Library and on the right it should say import task, click that.
3. Navigate to your install of `reddit-background-changer` and open the `bin` folder. Click on the `rbc-dir-clean.xml` file and this should start the import process.
4. Put your `pythonw.exe` path into the program/script, you can get this from the original script.
5. Then change your Start in field to your install path of `reddit-background-changer` then you could adjust the timing again if you'd like but cleaning the directory once a day is my personal preference.


## Final Notes
With the blacklist, to get the image ID you just look at the link of the post.

![Reddit Image ID](https://i.imgur.com/E2AQYv0.png "Reddit Image ID")

You can open the page of your background by clicking on the notification of when your wallpaper changes, or you can find it on your chosen subreddit.
- [Link to some good subreddits](https://www.reddit.com/r/sfwpornnetwork/wiki/network)

## Credits
[Member87](https://github.com/member87) - Made the base script and helped out with additions I made

## Alternatives
I highly recommend [Reddit-Wallpaper](https://github.com/Mamiglia/Reddit-Wallpaper) by Mamaiglia is you are looking for a UI based Reddit Wallpaper Changer.