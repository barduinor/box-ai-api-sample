import logging

from InquirerPy import inquirer

from app.box_ai import AI, AIItem

from app.config import AppConfig

from app.box_client import get_client
from app.prompts import get_manual_context, select_file

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
    print("\n------------")
    print("AI Ask Demo - Text Gen")
    print("------------")

    box_ai = AI(client)

    dialogue_history = []

    file_selection = select_file(client)

    context = get_manual_context("Enter additional file description if any:")

    item = AIItem(
        item_id=file_selection.item_id,
        item_type=file_selection.item_type,
        optional_document_content=context,
    )

    while True:
        prompt = inquirer.text(
            message="What would you like to talk about?\n" + " (type stop to exit or restart to start again)\n:"
        ).execute()

        if prompt == "stop":
            break

        if prompt == "restart":
            main()

        answer = box_ai.ask_text_gen(
            prompt=prompt,
            item=item,
            dialogue_history=dialogue_history,
        )

        print(f"\nAnswer:\n{answer.answer}\n")

        dialogue_history.append(answer)


if __name__ == "__main__":
    main()
