#!/usr/bin/python3

class Bot:
    def __init__(self):
        self.last_printed = None
        self.playing = None
        self.commands = {
            'exit': self.exit,
            'ping': self.ping,
            'echo': lambda args: self.say(' '.join(args[1:]))
        }

    def say(self, text):
        self.last_printed = text
        return 'say', text

    def exit(self, args):
        if len(args) == 1: return 'exit',
        return self.say(f"Command '{args[0]}' takes no arguments.")

    def ping(self, args):
        if len(args) == 1: return self.say('pong!')
        return self.say(f"Command '{args[0]}' takes no arguments.")

    def handle(self, text):
        args = text.split()
        if args[0] in self.commands:
            return self.commands[args[0]](args)
            
        if text == 'repeat' and self.last_printed:
            return 'print', f"I said, {self.last_printed}"
        
        if text == 'repeat':
            self.last_printed = 'Nothing to repeat!'
            return 'print', self.last_printed

        if args[0] == 'play' and self.playing is not None:
            self.last_printed = f'Already playing {self.playing}!'
            return 'print', self.last_printed

        if args[0] == 'play' and args[1] == 'guess':
            self.playing = 'guess'
            self.guess_number = 69
            self.last_printed = "Okay! I'm thinking of a number, guess with 'guess', or type 'give up'!"
            return 'print', self.last_printed

        # game-specific commands
        if self.playing == 'guess' and args[0] == 'guess':
            guess = int(args[1])
            if guess == self.guess_number:
                self.playing = None
                self.last_printed = 'You got it! Good game!'
                return 'print', self.last_printed
            else:
                self.last_printed = 'Nope, try again!'
                return 'print', self.last_printed

        if self.playing == 'guess' and text == 'give up':
            self.playing = None
            self.last_printed = f"No worries! I was thinking of the number {self.guess_number}."
            return 'print', self.last_printed

        # bad command
        return 'error', f"Unknown command {text}"

def run_console():
    bot = Bot()
    while True:
        text = input('bot> ')
        try:
            action, *args = bot.handle(text)
        except Exception as e:
            print('[ERROR]', e)
            continue
        print('[ACTION]', action, *args)
        if action == 'print':
            print(*args)
        if action == 'error':
            print('[ERROR]', *args)
        if action == 'exit':
            break 

if __name__ == '__main__': run_console()