
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ValidationTransactionForm(Action):

    def name(self) -> Text:
        return "failed_transfer_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        transaction_id = "transaction_id"
        if tracker.slots.get(transaction_id) is None:
            return [SlotSet('requested_slot', transaction_id)]

        return [SlotSet('requested_slot', None)]
    
class ActionSubmit(Action):
    def name(self) -> Text:
        return "failed_transfer_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        transaction_id = tracker.get_slot("transaction_id")
        response_text = f"Thanks! I've received the transaction ID: {transaction_id}"

        custom_response = {
            "type": "transaction",
            "text": response_text,
            "data": {
                "transaction_id": transaction_id
            }
        }
        print(f"🚀 Custom Action Called. Transaction ID: {transaction_id}")

        print("DISPATCHER OUTPUT:", custom_response)

        dispatcher.utter_message(**custom_response)

        return []

