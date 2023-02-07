class PingBot:
    def __init__(self):
        self.commands = {
            'ping': self.ping
        }

    def handle(self, event):
        command = event.get('command')
        func = self.commands.get(command)
        if func:
            return func(event)
        return {
            'err': f'{type(self).__name__} cannot {command}',
            'in': event.get('in'),
        }
        
    def ping(self, event):
        args = event.get('args', [event.get('command')])
        if len(args) is not 1: return {
            'err': f'usage: {args[0]}',
            'in': event.get('in'),
        }
        return {
            'print': 'pong!',
            'in': event.get('in'),
        }

def run_console():
    bot = PingBot()
    while True:
        text = input('> ')
        if not text.startswith('!'): continue
        args = text[1:].split()
        event = {
            'text': text,
            'args': args,
            'command': args[0],
            'from': 'console',
            'in': 'console',
        }
        action = bot.send(event)
        if action.get('print'):
            if action.get('in') == 'console':
                print(f"<bot> ")
        
