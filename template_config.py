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
            "subreddits": [],
            "local": False,
        },
        "city": 'London',
        "notify": False
    },
    "downloaded-path": os.getcwd() + "\\img\\bg_Downloaded\\",
    "custom-path": os.getcwd() + "\\img\\bg_Custom\\",
    "active-path": os.getcwd() + "\\img\\bg_Active\\",
    "imgur": {
        "client_id": "",
        "client_secret": "",
        "album_max": 25
    }
}

# dont touch this
debug = True
debugNotify = False
debugNight = True
