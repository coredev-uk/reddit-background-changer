# config.py
import os
SETTINGS = {
    "blacklist": [],
    "subreddits": ['EarthPorn'],
    "notify": True,
    "diff-bg": False,

    "res": {
      "monitor-x": "",
      "monitor-y": ""
    },

    "night-backgrounds": {
        "toggle": True,
        "diff-bg": True,
        "methods": {
            "chosen-method": "Link", # Link / Local / SubReddit / All
            "links": [""],
            "subreddits": ["SpacePorn"],
            "local": True,
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
debugNight = False
