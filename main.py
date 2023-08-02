"""main.py"""

import logging

from InquirerPy import inquirer

from app.box_ai import AI, AIItem

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
    print("==================")
    print("AI Ask Demo")
    print("==================")

    file_selection = select_file(client)
    item = AIItem(item_id=file_selection.item_id, item_type=file_selection.item_type)

    # file_context = extra_context()

    box_ai = AI(client)

    answer_history = []

    while True:
        prompt = inquirer.text(
            message="What would you like to know about this document? (type stop to exit or restart to start again):"
        ).execute()

        if prompt == "stop":
            break

        if prompt == "restart":
            main()

        answer = box_ai.ask(
            prompt=prompt,
            items=[item],
            mode="single_item_qa",
            dialogue_history=answer_history,
            is_streamed=False,
        )
        print(f"\nAnswer:\n{answer.answer}\n")
        answer_history.append(answer)


if __name__ == "__main__":
    main()
