class Wifi:

    def __init__(self, wifi_id, name, password):
        self.id = wifi_id
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Wifi> {}'.format(self.name)
