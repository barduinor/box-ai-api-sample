""" prompts presented to user for interactive demo """
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from boxsdk import Client

from app.box_content import get_folder_items


class SimpleItem:
    """simple item to hold id and type"""

    def __init__(self, item_id: str, item_type: str, item_name: str, parent_folder_id: str) -> None:
        self.item_id = item_id
        self.item_type = item_type
        self.item_name = item_name
        self.parent_folder_id = parent_folder_id

    def __str__(self):
        return f"{self.item_type} {self.item_id} {self.item_name} {self.parent_folder_id}"


def get_choices_by_folder(client: Client, folder_id: str) -> [Choice]:
    """build choices from folder items"""
    items = get_folder_items(client, folder_id)
    current_folder = client.folder(folder_id=folder_id).get()
    if current_folder.parent is not None:
        parent_folder_id = current_folder.parent.id
    else:
        parent_folder_id = "0"

    choices = []

    if folder_id != "0":
        choices.append(
            Choice(
                SimpleItem(parent_folder_id, "folder", "..", parent_folder_id),
                name="../",
            )
        )

    for item in items:
        if item.type == "folder":
            choices.append(
                Choice(
                    SimpleItem(item.id, item.type, item.name, parent_folder_id),
                    name=f"{item.name}/",
                )
            )
        else:
            choices.append(
                Choice(
                    SimpleItem(item.id, item.type, item.name, parent_folder_id),
                    name=f"{item.name}",
                )
            )

    choices.append(Choice(SimpleItem("-9", "folder", "Exit", parent_folder_id), name="Exit"))
    return choices


def select_file(client: Client, current_folder: str = "0") -> SimpleItem:
    """main menu"""

    while True:
        choices = get_choices_by_folder(client, current_folder)

        selection = inquirer.select(
            message="Select a file or folder:",
            choices=choices,
            default=None,
        ).execute()

        # print(f"Selection: {selection}")

        if selection.item_id == "-9":
            exit(0)

        if selection.item_type == "folder":
            current_folder = selection.item_id

        if selection.item_type == "file":
            # print(f"File: {selection.item_name}")
            return selection


def get_manual_context(prompt: str) -> str:
    """file context prompt"""
    return inquirer.text(message=prompt).execute()
