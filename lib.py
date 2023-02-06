class Bot:
    commands = []

    def __init__(self):
        self.generator = self.start() or self.idle()
        self.send()
    
    def send(self, event=None):
        self.act = self.generator.send(event)
    
    def start(self):
        yield from self.idle()
    
    def idle(self):
        yield from self.idle()
