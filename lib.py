class Bot:
    def __init__(self):
        self.generator = self.main()
        self.send()
    
    def send(self, event=None):
        self.act = self.generator.send(event)
        return self.act
    
    def main(self):
        return NotImplemented
