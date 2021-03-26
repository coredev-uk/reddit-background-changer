# Reddit Background Changer
A simple python script that fetches an image from your desired subreddit and sets it to your background.

## Task Scheduler Setup
1. Open Task Scheduler and click `New Task`.
2. Fill out the name and description with whatever you'd like and leave all other settings default.
3. On `Triggers` set it to `One Time` and set `Repeat Every` to however long you'd like between wallpaper refreshes, then add `At Logon` for any user as well.
4. On `Actions`, set program/script to your `pythonw.exe` path with "" around it. Set Start In to directory of python file and argument to `main.py`.
5. In the `Settings` tab tick `Allow task to be run on demand`, `Run task as soon as possible after a scheduled start is missed` and `If the running task does not end when requested, force it to stop` then set `Stop the task if it runs longer than:` to 1 hour.

## Features
- Pick your favourite subreddits
- Custom background to use at night
- Notification when you get a new background 

## Credits
[Member87](https://github.com/member87)

## Configuration
```python
SETTINGS = {
    "blacklist": [], # Add the image id of what you'd not like to see in the future
    "subreddits": ['cool-subreddit1', 'cool-subreddit2'], # Add your subreddit's here, its randomised each time its ran, so it'll be one from the list (it can just be one subreddit if you'd just like that)
    "night-backgrounds": True, # Set background to an image found in the night-backgrounds folder. Only happens at night (Easier for your eyes)
    "city": 'London' # Put your local city here if you decide to use night-backgrounds
}```

## Required Modules
- [Astral](https://pypi.org/project/astral/)
- [Win32Api](https://pypi.org/project/pywin32/)
- [Win10Toast-Click](https://pypi.org/project/win10toast-click/)