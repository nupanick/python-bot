from lib import Bot
from ping_bot import PingBot

class MainBot(Bot):

    def main(self):
        self.commands = ['echo', 'exit', 'repeat']
        self.last_printed = None
        self.apps = [PingBot()]
        while True:
            yield from self.idle()

    def idle(self):
        event = yield { 'listen': True }
        command = event.get('command')
        if not command: return
        for app in self.apps:
            if command in app.commands:
                act = app.send(event)
                if 'print' in act:
                    self.last_printed = act['print']
                yield act
                return

        if event['command'] == 'echo':
            act = { 
                'print': ' '.join(event['args'][1:]),
                'in': event['in'],
            }
            self.last_printed = act['print']
            yield act

        if event['command'] == 'exit':
            yield { 'exit': True }

        if event['command'] == 'repeat':
            yield from self.repeat()

    def repeat(self):
        if not self.last_printed:
            self.last_printed = 'Nothing to repeat!'
            yield { 'print': self.last_printed }
            return
        yield { 'print': f"I said, {self.last_printed}" }

def run_console():
    from ping_bot import PingBot
    bot = MainBot()
    while True:
        if 'listen' in bot.act:
            text = input('<user> ')
            args = text.split()
            if len(args) == 0: 
                continue
            bot.send({
                'command': args[0],
                'args': args,
                'text': text,
                'from': 'user',
                'in': 'console',
            })
            continue
        if 'print' in bot.act:
            print(f"<bot> {bot.act['print']}")
            bot.send()
            continue
        if 'exit' in bot.act:
            break
        print(f'unhandled bot action {bot.act}.')
        bot.send()

if __name__ == '__main__': run_console()
