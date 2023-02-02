#!/usr/bin/python3

class Bot:
    last_printed = None
    playing = None

    def handle(self, text):
        # single-word commands

        if text == 'exit':
            return 'exit',

        if text == 'repeat' and self.last_printed:
            return 'print', f"I said, {self.last_printed}"
        
        if text == 'repeat':
            self.last_printed = 'Nothing to repeat!'
            return 'print', self.last_printed

        if text == 'ping':
            self.last_printed = 'pong!'
            return 'print', self.last_printed

        # multi-word commands
        [command, *args] = text.split()

        if command == 'echo':
            self.last_printed = ' '.join(args)
            return 'print', self.last_printed

        if command == 'play' and self.playing is not None:
            self.last_printed = f'Already playing {self.playing}!'
            return 'print', self.last_printed

        if command == 'play' and args[0] == 'guess':
            self.playing = 'guess'
            self.guess_number = 69
            self.last_printed = "Okay! I'm thinking of a number, guess with 'guess', or type 'give up'!"
            return 'print', self.last_printed

        # game-specific commands
        if self.playing == 'guess' and command == 'guess':
            guess = int(args[0])
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
        if action == 'print':
            print(*args)
        if action == 'error':
            print('[ERROR]', *args)
        if action == 'exit':
            break 

if __name__ == '__main__': run_console()