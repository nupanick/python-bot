from lib import Bot

class PingBot(Bot):
    def main(self):
        self.commands = {
            'ping': self.ping
        }
        while True: 
            yield from self.idle()
        
    def idle(self):
        event = yield { 'listen': True }
        if event.get('command') == 'ping':
            yield from self.ping(event)

    def ping(self, event):
        if len(event.get('args')) == 1:
            yield {
                'print': 'pong!',
                'in': event['in'],
            }
        else:
            yield { 
                'print': 'ping does not take arguments!',
                'in': event['in'],
            }
