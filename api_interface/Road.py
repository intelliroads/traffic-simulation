class Road(object):
    """
    Road information provided by the api
    """

    def __init__(self, roadJSON):
        self.id = roadJSON["id"]
        self.kilometer = roadJSON["kilometer"]

    def __str__(self):
        return "Road - Id {0}, Km {1}".format(self.id, self.kilometer)
