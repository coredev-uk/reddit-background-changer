# Reddit Background Changer
A simple python script that fetches an image from your desired subreddit and sets it to your background.

## Features
- Pick your favourite subreddits
- Custom background to use at night
- Notification when you get a new background
- Blacklist images you dont like
- Get images tailored to your resolution
- Optional efficient on storage as images are removed after background being set
- Caches the JSON so you dont get notified if your background is the same (experimental option)

## Required Modules
- [PyWin32](https://pypi.org/project/pywin32/)
- [Win10Toast-Click](https://pypi.org/project/win10toast-click/)
- [Astral](https://pypi.org/project/astral/) - Optional if you want to use the night backgrounds (Remove it from the imports if you dont want to use it)

## Configuration
*Edit this at the top of [main.py](https://github.com/coredev-uk/reddit-background-changer/blob/main/main.py#L5).*
```python
SETTINGS = {
    "blacklist": ['7t0swm'], # Add the image id or if you use save-images you can use the file name of what you'd not like to see in the future
    "subreddits": ['EarthPorn', 'SkyPorn'], # Add your subreddit's here, its randomised each time its ran, so it'll be one from the list (it can just be one subreddit if you'd just like that)
    "night-backgrounds": {
        "toggle": False, # Here you can toggle night-backgrounds - If you leave links empty '[]' then it will attempt to use images found in the Custom-Backgrounds folder
        "links": ["https://acoolimage/img.jpg"], # Set background to an you found on the internet.
        "city": 'London' # Put your local city here if you decide to use night-backgrounds, just leave it default if you dont want to use the night-backgrounds
    }
}
```

## Night Backgrounds
Just a note about the night-backgrounds, if you prefer to have a wide array of images stored locally for the night backgrounds, you can create a folder called `Custom-Backgrounds` and place your images in here, make sure the night-backgrounds list is also empty and it will pick a random image from that directory.

## Task Scheduler Setup
1. Open Task Scheduler and click **New Task**.
2. Fill out the name and description with whatever you'd like and leave all other settings default.
3. On Triggers set it to **One Time** and set **Repeat Every** to however long you'd like between wallpaper refreshes, then add **At Logon** for any user as well.
4. On Actions, set program/script to your `pythonw.exe` path with "" around it. Set Start In to directory of python file and argument to `main.py`.
5. In the Settings tab tick **Allow task to be run on demand**, **Run task as soon as possible after a scheduled start is missed** and **If the running task does not end when requested, force it to stop** then set **Stop the task if it runs longer than:** to 1 hour.

## Final Notes
With the blacklist, to get the image id you just look at the link of the post.

![Reddit Image ID](https://i.imgur.com/E2AQYv0.png "Reddit Image ID")

You can open the page of your background by clicking on the notification of when your wallpaper changes, or you can find it on your chosen subreddit.
- [Link to some good subreddits](https://www.reddit.com/r/sfwpornnetwork/wiki/network)

## Credits
[Member87](https://github.com/member87) - Made the base script and helped out with additions I made

## Alternatives
I highly recommend [Reddit-Wallpaper](https://github.com/Mamiglia/Reddit-Wallpaper) by Mamaiglia is you are looking for a UI based Wallpaper Change.