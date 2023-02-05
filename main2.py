from lib import Bot
from ping_bot import PingBot

class MainBot(Bot):
    commands = ['echo', 'exit', 'repeat']

    def start(self):
        self.last_printed = None
        self.ping_bot = PingBot()
        while True: yield from self.idle()

    def idle(self):
        event = yield { 'listen': True }
        if 'command' not in event: 
            return
        if event['command'] in self.ping_bot.commands:
            self.ping_bot.send(event)
            if 'print' in self.ping_bot.act:
                self.last_printed = self.ping_bot.act['print']
            yield self.ping_bot.act
            return
        if event['command'] == 'echo':
            response = { 'print': event['text'] }
            self.last_printed = response['print']
            yield response
            return
        if event['command'] == 'exit':
            yield { 'exit': True }
            return
        if event['command'] == 'repeat':
            yield from self.repeat()
            return

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
