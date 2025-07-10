from typing import Text, Dict, Any, Callable, Awaitable
from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from sanic import Blueprint, response
from sanic.request import Request


class CustomOutputChannel(OutputChannel):
    def __init__(self):
        self.messages = []

    async def send_text_message(self, recipient_id: Text, text: Text, **kwargs: Any) -> None:
        custom_message = {
            "recipient_id": recipient_id,
            "text": text,
            "type": kwargs.get("type", "default"),
            "data": kwargs.get("data", {})
        }
        self.messages.append(custom_message)


class CustomRestInput(InputChannel):
    def name(self) -> Text:
        return "custom_rest"

    def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[None]]) -> Blueprint:
        custom_webhook = Blueprint("custom_webhook", __name__)

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request):
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            sender = request.json.get("sender")
            message = request.json.get("message")

            output_channel = CustomOutputChannel()
            user_msg = UserMessage(message, output_channel, sender, input_channel=self.name())

            await on_new_message(user_msg)

            return response.json(output_channel.messages)

        return custom_webhook