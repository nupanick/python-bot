class GuessingGame:
    def __init__(self):
        self.phase = 'idle'
        self.commands = { 'start', 'exit' }

    def handle(self, event):
        command = event['args'][0]

        if command == 'exit':
            return [
                { 'print': 'Goodbye!' },
                { 'exit': True },
            ]

        if self.phase == 'idle' and command == 'start':
            self.secret = 69 # nice
            self.phase = 'playing'
            return [{ 'print': "I'm thinking of a number! Try to [guess] it!" }]
        
        if self.phase == 'idle':
            return [{ 'print': 'commands: start, exit' }]

        if self.phase == 'playing' and command == 'guess':
            return self.guess(event)
        
        if self.phase == 'playing' and command == 'giveup':
            self.phase = 'idle'
            return [{ 'print': f'No worries! I was thinking of {self.secret}.' }]
        
        if self.phase == 'playing':
            return [{ 'print': 'commands: guess, giveup, exit' }]

        return [{ 'error': f'unable to handle command {command} in phase {self.phase}.' }]

    def guess(self, event):
        # make sure the user typed a number
        args = event.get('args', [])
        try:
            assert len(args) == 2
            num = int(args[1])
        except:
            return [{ 'print': f'usage: {args[0]} <number>' }]

        if num < self.secret:
            return [{ 'print': 'Too low!' }]
        elif num > self.secret:
            return [{ 'print': 'Too high!' }]
        else:
            self.phase = 'idle'
            return [{ 'print': 'Yep, that was it! Nice.' }]

def run_console():
    bot = GuessingGame()
    actions = []
    while True:
        
        if not actions:
            text = input('<user> ')
            args = text.split()
            event = { 'text': text, 'args': args }
            try:
                actions = bot.handle(event)
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
