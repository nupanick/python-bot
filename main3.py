class PingBot:
    def __init__(self):
        self.commands = {
            'ping': self.ping,
            'exit': lambda _: { 'exit': True },
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
        if len(args) != 1: return {
            'err': f'usage: {args[0]}',
            'in': event.get('in'),
        }
        return {
            'print': 'pong!',
            'in': event.get('in'),
        }

class GuessBot:
    def __init__(self):
        self.phase = 'idle'

    def handle(self, event):
        args = event['args']
        command = args[0]
                
        if command == 'exit':
            return [
                { 'print': 'Goodbye!' },
                { 'exit': True },
            ]

        if self.phase == 'idle' and command == 'start':
            self.secret = 69
            self.phase = 'playing'
            return [{ 'print': "I'm thinking of a number! Try to [guess] it!" }]
        if self.phase == 'idle':
            return [{ 'print': 'commands: start, exit' }]

        if self.phase == 'playing' and command == 'guess':
            return self.guess(event)
        if self.phase == 'playing' and command == 'giveup':
            self.phase = 'idle'
            return [{ 'print': 'game over' }]
        if self.phase == 'playing':
            return [{ 'print': 'commands: guess, giveup, exit' }]

    def guess(self, event):
        args = event.get('args', [])
        if len(args) != 2:
            return [{ 'print': f'usage: {args[0]} <number>' }]

def run_console():
    bot = GuessBot()
    actions = []
    while True:
        if not actions:
            text = input('<user> ')
            args = text.split()
            command = args[0]
            event = {
                'text': text,
                'args': args,
                'command': command,
                'from': 'user',
                'room': 'console',
            }
            try:
                actions = bot.handle(event) or []
                continue
            except Exception as e:
                print(f'[ERROR]: {e}')
                continue
        a = actions.pop(0)
        if 'error' in a: 
            print(f"[ERROR]: {a['error']}")
        if 'print' in a:
            print(f"<bot> {a['print']}")     
        if 'exit' in a:
            break   

if __name__ == '__main__': run_console()
