"""handle box content management to list files and navigate folders"""
from typing import Iterable

from boxsdk import Client
from boxsdk.object.item import Item


def get_folder_items(client: Client, folder_id: str = "0") -> Iterable[Item]:
    """get folder items"""

    items = client.folder(folder_id=folder_id).get_items()

    files_folders = []

    for item in items:
        if item.type == "web_link":
            continue
        files_folders.append(item)

    return files_folders
