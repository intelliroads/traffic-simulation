class RedLight(object):
    """
    Red light information of a traffic light provided by the api
    """

    def __init__(self, tlJSON):
        self.duration = tlJSON["duration"]
        self.frequency = tlJSON["frequency"]
