from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text, Union
import random

DATABASE = [
    "bún đậu mắm tôm",
    "bún đậu nước mắm",
    "bún cá",
    "bún hải sản",
    "cơm văn phòng",
    "cơm sườn",
    "xôi",
    "bún ốc",
    "mì vằn thắn",
    "hủ tiếu",
    "bún chả",
    "bún ngan",
    "ngan xào tỏi",
    "bún bò huế",
    "mì tôm hải sản",
    "bánh mì trứng xúc xích rắc thêm ít ngải cứu",
    "bánh mì trứng",
    "bánh mì xúc xích",
    "bánh mì pate",
    "miếng gà",
]


class ActionRecommend(Action):
    def name(self) -> Text:
        return "action_recommend"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # thử coi cái này là gì
        time = tracker.get_slot("time")
        food = []
        for i in range(2):
            food_number = random.randrange(len(DATABASE))
            food.append(DATABASE[food_number])

        dispatcher.utter_message(
            text="Em nghĩ {} nay anh chị có thể thử món '{}' hoặc bên cạnh đó cũng có thể là món '{}' ạ".format(
                time, food[0], food[1]
            )
        )
        food.clear()

        return []
