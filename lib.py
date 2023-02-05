class Bot:
    def __init__(self):
        self._gen = self.start()
        self.send()
    def send(self, event=None):
        self.act = self._gen.send(event)
        return self.act
    def start(self):
        return NotImplemented
    commands = NotImplemented
