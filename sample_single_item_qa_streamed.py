import logging
from time import sleep

from InquirerPy import inquirer

from app.box_ai import AI, AIItem, QAMode

from app.config import AppConfig

from app.box_client import get_client
from app.prompts import select_file

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """

    client = get_client(conf)

    # user = client.user().get()
    print("\n-------------------------------------")
    print("AI Ask Demo - Single Item QA Streamed")
    print("-------------------------------------")

    file_selection = select_file(client)
    item = AIItem(
        item_id=file_selection.item_id,
        item_type=file_selection.item_type,
    )

    box_ai = AI(client)

    while True:
        prompt = inquirer.text(
            message="What would you like to know about this document?\n"
            + " (type stop to exit or restart to start again)\n:"
        ).execute()

        if prompt == "stop":
            break

        if prompt == "restart":
            main()

        answers = box_ai.ask_item_streamed(
            mode=QAMode.SINGLE_ITEM_QA,
            prompt=prompt,
            items=[item],
        )

        for answer in answers:
            print(f"{answer.answer}", end="")
            sleep(0.1)  # just for effect ;)
            if answer.completion_reason == "done":
                print("\n")


if __name__ == "__main__":
    main()
