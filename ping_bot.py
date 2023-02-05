import unittest
from lib import Bot

class PingBot(Bot):
    commands = ['ping']

    def start(self):
        event = yield { 'listen': True }
        if event.get('command') == 'ping':
            yield from self.ping(event)
        yield from self.start()

    def ping(self, event):
        if len(event.get('args')) != 1:
            yield { 
                'print': 'ping does not take arguments!',
                'in': event['in'],
            }
            return
        yield {
            'print': 'pong!',
            'in': event['in'],
        }

class TestPingBot(unittest.TestCase):

    def test_list_commands(self):
        bot = PingBot()
        self.assertEqual(bot.commands, ['ping'])

    def test_do_nothing(self):
        bot = PingBot()
        self.assertEqual(bot.act, { 'listen': True })
        bot.send({
            'from': 'alice',
            'room': 'general',
            'text': 'irrelevant chatter',
        })
        self.assertEqual(bot.act, { 'listen': True })

    def test_reply(self):
        bot = PingBot()
        self.assertEqual(bot.act, { 'listen': True })
        bot.send({
            'from': 'alice',
            'in': 'general',
            'command': 'ping',
            'args': ['ping'],
        })
        self.assertEqual(bot.act, {
            'print': 'pong!',
            'in': 'general',
        })
        bot.send()
        self.assertEqual(bot.act, { 'listen': True })
