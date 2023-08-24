""" box ai class"""

from datetime import datetime
import json
from typing import Any
from enum import Enum
from boxsdk import Client
from boxsdk.util.api_call_decorator import api_call
from boxsdk.util.translator import Translator
from boxsdk.object.cloneable import Cloneable


class QAMode(Enum):
    """box ai item mode enum"""

    SINGLE_ITEM_QA = "single_item_qa"
    MULTIPLE_ITEM_QA = "multiple_item_qa"
    # TEXT_GEN = "text_gen"


class TextGenMode(Enum):
    """box ai item mode enum"""

    TEXT_GEN = "text_gen"


class AIQuestionMode(Enum):
    """box ai item mode enum"""

    SINGLE_ITEM_QA = "single_item_qa"
    MULTIPLE_ITEM_QA = "multiple_item_qa"
    TEXT_GEN = "text_gen"


class AIItem:
    """box ai item class"""

    def __init__(self, item_id: str, item_type: str, optional_document_content: str = None):
        self.item_id = item_id
        self.item_type = item_type
        self.optional_document_content = optional_document_content

    def to_json(self):
        # if self.optional_document_content is not None:
        #     return {"content": self.optional_document_content}

        return {
            "type": self.item_type,
            "id": self.item_id,
            "content": self.optional_document_content if self.optional_document_content is not None else "",
        }


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

    def to_json(self):
        return {
            "answer": self.answer,
            "created_at": self.created_at,
            "completion_reason": self.completion_reason,
            "prompt": self.prompt,
        }


class AIQuestion:
    """box ai question class"""

    def __init__(
        self,
        prompt: str,
        items: [AIItem],
        mode: AIQuestionMode = AIQuestionMode.SINGLE_ITEM_QA,
        dialogue_history: [AIAnswer] = [],
    ):
        self.prompt = prompt
        self.items = items
        self.mode = mode
        self.dialogue_history = dialogue_history

    def to_json(self):
        items_json = []
        for item in self.items:
            items_json.append(item.to_json())

        dialogue_history_json = []
        for dialogue in self.dialogue_history:
            dialogue_history_json.append(dialogue.to_json())

        return {
            "prompt": self.prompt,
            "items": items_json,
            "mode": self.mode.value,
            "dialogue_history": dialogue_history_json,
        }


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

    def _get_ai_api_response(self, prompt: str, ai_question: AIQuestion) -> AIAnswer:
        ai_question_json = ai_question.to_json()
        ai_question_json["config"] = {"is_streamed": False}
        data = json.dumps(ai_question_json)
        print(data)

        url = self.get_url("ai/ask")
        box_response = self._session.post(url, data=data, expect_json_response=True)

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

    def _get_ai_api_response_streamed(self, prompt: str, ai_question: AIQuestion) -> AIAnswer:
        ai_question_json = ai_question.to_json()
        ai_question_json["config"] = {"is_streamed": True}
        data = json.dumps(ai_question_json)
        print(data)

        url = self.get_url("ai/ask")
        box_response = self._session.post(url, data=data, expect_json_response=False)

        for chunk in box_response.network_response.request_response.iter_lines():
            if chunk:
                response_object = self.translator.translate(
                    session=self._session,
                    response_object=json.loads(chunk),
                )

                yield AIAnswer(
                    answer=response_object["answer"],
                    created_at=response_object["created_at"],
                    completion_reason=response_object.get("completion_reason"),
                    prompt=prompt,
                )

    @api_call
    def ask_item(self, mode: QAMode, prompt: str, items: [AIItem]) -> AIAnswer:
        """
        Ask the AI a question.

        :param mode:
            This tells Box AI what type of request you will be making
            “single_item_qa” - Ask a question about a single document
            “multiple_item_qa” - Ask a question about a group of items.
            This is not yet fully implemented, so you may experience issues.
        :param prompt:
            The question you wish to ask about your document or content.
        :param items:
            This is an array of AIItem objects that describe the file
            or content you wish to add to your context.

        :returns:
            An AIAnswer object containing the answer to your question.
        """

        # build the ai question object
        ai_question = AIQuestion(
            prompt=prompt,
            items=items,
            mode=mode,
        )

        return self._get_ai_api_response(prompt, ai_question)

    @api_call
    def ask_item_streamed(self, mode: QAMode, prompt: str, items: [AIItem]) -> AIAnswer:
        """
        Ask the AI a question.

        :param mode:
            This tells Box AI what type of request you will be making
            “single_item_qa” - Ask a question about a single document
            “multiple_item_qa” - Ask a question about a group of items.
            This is not yet fully implemented, so you may experience issues.
        :param prompt:
            The question you wish to ask about your document or content.
        :param items:
            This is an array of AIItem objects that describe the file
            or content you wish to add to your context.

        :returns:
            An AIAnswer object containing the answer to your question.
        """

        # build the ai question object
        ai_question = AIQuestion(
            prompt=prompt,
            items=items,
            mode=mode,
        )

        return self._get_ai_api_response_streamed(prompt, ai_question)

    @api_call
    def ask_text_gen(
        self,
        prompt: str,
        item: AIItem,
        dialogue_history: [AIAnswer] = None,
    ) -> AIAnswer:
        """
        Ask the AI a question.

        :param prompt:
            The question you wish to ask about your document or content.
        :param dialogue_history:
            Dialogue history contains the previous prompts
            and answers from the same item(s)

        :returns:
            An AIAnswer object containing the answer to your question.
        """

        # build the ai question object

        ai_question = AIQuestion(
            prompt=prompt,
            items=[item],
            mode=TextGenMode.TEXT_GEN,
            dialogue_history=dialogue_history,
        )

        return self._get_ai_api_response(prompt, ai_question)

    @api_call
    def ask_text_gen_streamed(
        self,
        prompt: str,
        item: AIItem,
        dialogue_history: [AIAnswer] = None,
    ) -> AIAnswer:
        """
        Ask the AI a question.

        :param prompt:
            The question you wish to ask about your document or content.
        :param dialogue_history:
            Dialogue history contains the previous prompts
            and answers from the same item(s)

        :returns:
            An AIAnswer object containing the answer to your question.
        """

        # build the ai question object

        ai_question = AIQuestion(
            prompt=prompt,
            items=[item],
            mode=TextGenMode.TEXT_GEN,
            dialogue_history=dialogue_history,
        )

        return self._get_ai_api_response_streamed(prompt, ai_question)
