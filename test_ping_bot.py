import unittest
from ping_bot import PingBot

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
