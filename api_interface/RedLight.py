class RedLight(object):
    def __init__(self, tlJSON):
        self.duration = tlJSON["duration"]
        self.frequency = tlJSON["frequency"]
