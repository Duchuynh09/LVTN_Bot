from rasa.shared.core.slots import Slot


class ObjectOfEventSlot(Slot):
    def feature_dimensionality(self):
        return 1

    def as_feature(self):
        return [1.0] if self.value else [0.0]
