""" box ai class"""

from datetime import datetime
import json
from typing import Any
from boxsdk import Client
from boxsdk.util.api_call_decorator import api_call
from boxsdk.util.translator import Translator
from boxsdk.object.cloneable import Cloneable


class AIItem:
    """box ai item class"""

    def __init__(self, item_id: str, item_type: str, content: str = None):
        self.item_id = item_id
        self.item_type = item_type
        self.content = content


class AIAnswer:
    """box ai answer class"""

    def __init__(
        self,
        answer: str,
        created_at: datetime,
        completion_reason: str = None,
        prompt: str = None,
    ):
        self.answer = answer
        self.created_at = created_at
        self.completion_reason = completion_reason
        self.prompt = prompt


class AI(Cloneable):
    """box ai class"""

    def __init__(self, client: Client):
        self.client = client
        self._session = client._session

    @property
    def translator(self) -> "Translator":
        """The translator used for translating Box API JSON responses
        into `BaseAPIJSONObject` smart objects."""
        return self._session.translator

    def get_url(self, endpoint: str, *args: Any) -> str:
        """
        Return the URL for the given Box API endpoint.

        :param endpoint:
            The name of the endpoint.
        :param args:
            Additional parts of the endpoint URL.
        """
        # pylint:disable=no-self-use
        return self._session.get_url(endpoint, *args)

    @api_call
    def ask(
        self,
        prompt: str,
        items: [AIItem],
        mode: str = "single_item_qa",
        dialogue_history: [AIAnswer] = None,
        is_streamed: bool = False,
    ) -> AIAnswer:
        """
        Ask the AI a question.

        :param prompt:
            The question you wish to ask about your document or content.
        :param items:
            This is an array of AIItem objects that describe the file
            or content you wish to add to your context.
        :param mode:
            This tells Box AI what type of request you will be making
            “single_item_qa” - Ask a question about a single document
            “text_gen” - generate text based on a single item
            “multiple_item_qa” - Ask a question about a group of items.
            This is not yet fully implemented, so you may experience issues.
        :param dialogue_history:
            Dialogue history contains the previous prompts
            and answers from the same item(s)
        :param is_streamed:
            Whether or not to return the entire answer at once (false)
            or by token (true). Default is false.

        :returns:
            An AIAnswer object containing the answer to your question.
        """
        url = self.get_url("ai/ask")

        # build the ai question object
        ai_question = {}
        ai_question["prompt"] = prompt
        ai_question["items"] = []
        for item in items:
            ai_question["items"].append(
                {
                    "type": item.item_type,
                    "id": item.item_id,
                }  # , "content": item.content}
            )
        ai_question["mode"] = mode
        if dialogue_history is not None:
            ai_question["dialogue_history"] = []
            for dialogue in dialogue_history:
                ai_question["dialogue_history"].append(
                    {
                        "answer": dialogue.answer,
                        "created_at": dialogue.created_at,
                        "prompt": dialogue.prompt,
                    }
                )
        ai_question["config"] = {"is_streamed": is_streamed}

        data = json.dumps(ai_question)
        # print(data)

        box_response = self._session.post(url, data=data)
        response = box_response.json()
        response_object = self.translator.translate(
            session=self._session,
            response_object=response,
        )

        return AIAnswer(
            answer=response_object["answer"],
            created_at=response_object["created_at"],
            completion_reason=response_object["completion_reason"],
            prompt=prompt,
        )
