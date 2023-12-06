from typing import Any, Coroutine, Optional, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class RegisterEventForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_register_event_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        if tracker.get_intent_of_latest_message() == "stop_form":
            if len(domain_slots) != 0:
                domain_slots.remove("event")
                domain_slots.remove("email")
        return domain_slots

    def validate_event(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"event": slot_value}
        return {"event": None}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        validate_email = next(tracker.get_latest_entity_values("user_email"), None)
        if validate_email:
            return {"email": validate_email}
        else:
            dispatcher.utter_message("Email phải đúng định dạng")
            return {"email": None}
