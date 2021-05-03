# config.py
import os
SETTINGS = {
    "blacklist": [],
    "subreddits": ['EarthPorn'],
    "diff-bg": False,
    "monitor-x": "",
    "monitor-y": "",
    "night-backgrounds": {
        "toggle": True,
        "diff-bg": False,
        "methods": {
            "chosen-method": "All", # Link / Local / SubReddit / All
            "links": [],
            "subreddits": ['SpacePorn'],
            "local": True,
        },
        "city": 'London',
        "notify": False
    },
    "downloaded-path": os.getcwd() + "\\img\\bg_Downloaded\\",
    "custom-path": os.getcwd() + "\\img\\bg_Custom\\",
    "active-path": os.getcwd() + "\\img\\bg_Active\\"
}

# dont touch this
debug = False
debugNotify = False
debugNight = False
