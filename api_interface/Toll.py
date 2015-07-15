class Toll(object):
    """
    Toll information provided by the api
    """

    def __init__(self, tollJSON):
        self.service_rate = tollJSON["serviceRate"]
        self.number_of_servers = tollJSON["numberOfServers"]

