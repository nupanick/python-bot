#!/usr/bin/python3

class Bot:
    last_printed = None

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

        # bad command

        return 'error', f"Unknown command {command}"

def run_console():
    bot = Bot()
    while True:
        text = input('bot> ')
        action, *args = bot.handle(text)
        if action == 'print':
            print(*args)
        if action == 'error':
            print('[ERROR]', *args)
        if action == 'exit':
            break 

if __name__ == '__main__': run_console()