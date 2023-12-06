from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text, Union
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ActiveLoop
import requests
import gc
import random

url = "http://localhost:5000/dssv"


def load_suggest():
    temp_button_lst = []
    temp_button_lst.append(
        {
            "type": "helpEvent",
            "title": "Sự kiện mới nhất",
            "payload": "/ask_new_event",
        }
    )
    temp_button_lst.append(
        {
            "type": "helpEvent",
            "title": "Sự kiện nổi bật",
            "payload": "/ask_most_event",
        }
    )
    temp_button_lst.append(
        {
            "type": "helpEvent",
            "title": "Sự kiện hôm nay",
            "payload": "/ask_today_event",
        }
    )
    temp_button_lst.append(
        {
            "type": "helpEvent",
            "title": "Sự kiện ngày mai",
            "payload": "/ask_next_event",
        }
    )
    temp_button_lst.append(
        {
            "type": "helpEvent",
            "title": "Tổng sự kiện",
            "payload": "/ask_total_event",
        }
    )
    temp_button_lst.append(
        {
            "type": "helpEvent",
            "title": "Sự kiện không giới hạn tham gia",
            "payload": "/ask_event_enable",
        }
    )
    return temp_button_lst


button_lst = load_suggest()


def suggest():
    global button_lst
    return random.sample(button_lst, k=2)


def getEventInfo(
    name: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
) -> Text:
    response = requests.post(
        url + "/getEventByName",
        data={"name": name},
    )
    if len(response.json()) > 1:
        list = []
        for index, obj in enumerate(response.json()):
            list.append(
                "{}. Tên sự kiện: {}\n  Thời gian-{},Ngày {}\n  Số người đăng ký: {}".format(
                    index + 1,
                    obj["name"],
                    obj["time"],
                    obj["date"],
                    len(obj["dsDaDangKy"]),
                )
            )
        name_string = "\n".join(list)
        message = "Sự kiện gồm:\n{}".format(name_string)
        dispatcher.utter_message(message)
    else:
        if len(response.json()) == 1:
            dispatcher.utter_message(
                text=" Tên sự kiện: {}\n Thời gian-{},Ngày {}\n Số người đăng ký: {}".format(
                    response.json()[0]["name"],
                    response.json()[0]["time"],
                    response.json()[0]["date"],
                    len(response.json()[0]["dsDaDangKy"]),
                )
            )
            return response.json()[0]["name"]
        else:
            dispatcher.utter_message("Không trùng khớp với sự kiện nào")
            return None


class EventInfo(FormValidationAction):
    def name(self) -> Text:
        return "validate_event_form"

    def validate_event(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value:
            evet = requests.post(
                url + "/getEventByName",
                data={"name": slot_value},
            )
            if len(evet.json()) != 0:
                return {"event": slot_value}
            else:
                dispatcher.utter_message("Sự kiện không tồn tại")
                return {"event": None}

        else:
            dispatcher.utter_message("Tên sự kiện chưa đúng định dạng")
            return {"event": None}


class ActionTotalEvent(Action):
    def name(self) -> Text:
        return "action_total_event"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        response = requests.get(url + "/getTotal")
        # for item in response.json():
        dispatcher.utter_message("Tổng số sự kiện là: {}".format(response.json()))
        return []


class ActionTodayEvent(Action):
    def name(self) -> Text:
        return "action_today_event"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        response = requests.get(url + "/getToDay")
        # for item in response.json():
        if len(response.json()) != 0:
            list = []
            for index, obj in enumerate(response.json()):
                list.append(
                    "{}. Sự kiện: {} - {} ({} joiner)".format(
                        index + 1,
                        obj["name"],
                        obj["time"],
                        len(obj["dsDaDangKy"]),
                    )
                )
            name_string = "\n".join(list)
            message = "Sự kiện ngày mai là:\n{}".format(name_string)
            dispatcher.utter_message(message)
            del name_string, list, response, message

        else:
            dispatcher.utter_message("Hôm nay không có sự kiện nào diễn ra")
        gc.collect()
        return []


class ActionTomorowEvent(Action):
    def name(self) -> Text:
        return "action_tomorow_event"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        response = requests.get(url + "/getTomorrow")
        # for item in response.json():
        if len(response.json()) != 0:
            list = []
            for index, obj in enumerate(response.json()):
                list.append(
                    "{}. Sự kiện: {} - {} ({} joiner)".format(
                        index + 1,
                        obj["name"],
                        obj["time"],
                        len(obj["dsDaDangKy"]),
                    )
                )
            name_string = "\n".join(list)
            message = "Sự kiện ngày mai là:\n{}".format(name_string)
            dispatcher.utter_message(message)
            del name_string, list, response, message
        else:
            dispatcher.utter_message("Ngày mai không có sự kiện nào diễn ra")
        gc.collect()
        return []


class ActionInfoEvent(Action):
    def name(self) -> Text:
        return "action_info_event"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        eventName = tracker.get_slot("event")
        getEventInfo(
            name=eventName,
            tracker=tracker,
            dispatcher=dispatcher,
        )
        del eventName
        gc.collect()
        return [
            SlotSet("event", None),
        ]


class ActionNewEvent(Action):
    def name(self) -> Text:
        return "action_new_event"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        response = requests.get(url + "/getNewEvent")
        dispatcher.utter_message(
            "Sự kiện mới nhất là : {} - {}, Ngày {}".format(
                response.json()["name"],
                response.json()["time"],
                response.json()["date"],
            )
        )
        del response
        gc.collect()
        return []


class ActionMostEvent(Action):
    def name(self) -> Text:
        return "action_most_event"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        response = requests.get(url + "/getMoodEvent")
        list = [
            "Top {}:\n  Tên sự kiện: {}\n  Thời gian-{},Ngày {}\n  Số người đăng ký: {}".format(
                index + 1,
                obj["name"],
                obj["time"],
                obj["date"],
                len(obj["dsDaDangKy"]),
            )
            for index, obj in enumerate(response.json())
        ]
        list_event = "\n\n".join(list)
        dispatcher.utter_message(list_event)
        del list_event, list, response
        gc.collect()
        return []


class ActionEventEnable(Action):
    def name(self) -> Text:
        return "action_event_enable"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        response = requests.get(url + "/getEnableEvent")
        if response.json():
            list = [
                "- {} ({}, {})".format(obj["name"], obj["time"], obj["date"])
                for obj in response.json()
            ]
            list_event = "\n".join(list)
            dispatcher.utter_message(list_event)
            del list_event, response
        else:
            dispatcher.utter_message("Không tìm thấy sự kiện")
        gc.collect()
        return []


class ActionRegisterSeat(Action):
    def name(self) -> Text:
        return "action_register_seat"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        email = tracker.get_slot("email")
        entityEmail = next(tracker.get_latest_entity_values("user_email"), None)
        event = tracker.get_slot("event")
        if entityEmail and event:
            response = requests.post(
                url + "/registerSeatByRasa", data={"event": event, "email": entityEmail}
            )
            responseEvent = response.json()
            message = responseEvent["message"]
            dispatcher.utter_message(message)
            del message, responseEvent, response
        else:
            dispatcher.utter_message("Dừng form")
        gc.collect()
        return [SlotSet("event", None), SlotSet("email", None)]


class SugestEventHelp(Action):
    def name(self) -> Text:
        return "action_event_help"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        buttons = suggest()
        dispatcher.utter_message(text="Bạn cần giúp gì", buttons=buttons)

        return []
