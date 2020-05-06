class Communication:

    def __init__(self, communication_id, port, baudrate, timeout, preamble):
        self.id = communication_id
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.preamble = preamble

    def __repr__(self):
        return '<Communication> {}:{}'.format(self.port, self.baudrate)
