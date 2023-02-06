from lib import Bot
from ping_bot import PingBot

class MainBot(Bot):
    commands = ['echo', 'exit', 'repeat']
    last_printed = None
    apps = []

    def start(self):
        self.apps.append(PingBot())
        yield from self.idle()

    def idle(self):
        event = yield { 'listen': True }
        command = event.get('command')
        if not command:
            yield from self.idle()
        # if command == 'echo': return self.echo(event)
        # if command == 'exit': return self.exit()
        # if command == 'repeat': return self.repeat()
        for app in self.apps:
            if command in app.commands:
                app.send(event)
                if 'print' in app.act:
                    self.last_printed = app.act['print']
                yield app.act
                yield from self.idle()

        if event['command'] == 'echo':
            response = { 'print': event['text'] }
            self.last_printed = response['print']
            yield response
            yield from self.idle()

        if event['command'] == 'exit':
            yield { 'exit': True }
            yield from self.idle()

        if event['command'] == 'repeat':
            yield from self.repeat()
            yield from self.idle()

        yield from self.idle()

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
