class Toll(object):
    def __init__(self, tollJSON):
        self.service_rate = tollJSON["serviceRate"]
        self.number_of_servers = tollJSON["numberOfServers"]

