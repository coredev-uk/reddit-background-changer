# _directory_clear.py

import os

from config import SETTINGS as s

DirectoryToClear = s['downloaded-path']

for file in os.listdir(DirectoryToClear):
    os.remove(os.path.join(DirectoryToClear, file))
    print(f"Removing File {file}")
