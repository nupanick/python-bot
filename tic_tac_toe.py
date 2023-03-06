class TicTacToeBot:
    def start(self):
        return []

    def send(self, event):
        args = event['text'].split()
        command = args[0]

        if command == 'exit' and len(args) == 1:
            return [
                { 'print': 'Goodbye!' },
                { 'exit': True },
            ]

        if command == 'start' and len(args) == 1:
            self.board = [' '] * 9
            return [
                { 'draw': draw_board(self.board) }
            ]

def draw_board(board):
    t = '\n'.join([
        ' 0 | 1 | 2 ',
        '---|---|---',
        ' 3 | 4 | 5 ',
        '---|---|---',
        ' 6 | 7 | 8 ',
    ])
    for i, v in enumerate(board):
        t = t.replace(str(i), v)
    return t

def console_main(bot):
    actions = bot.start()
    while True:
        if not actions:
            text = input('<user> ')
            try:
                actions = bot.send({ 'text': text })
            except Exception as e:
                actions = [{ 'error': e }]
            continue
        a = actions.pop(0)
        if 'error' in a:
            print(f'[ERROR]: {a["error"]}')
        if 'print' in a:
            print(f'<bot> {a["print"]}')
        if 'draw' in a:
            print(f'<bot> ```\n{a["draw"]}\n```')
        if 'exit' in a:
            break

if __name__ == '__main__':
    bot = TicTacToeBot()
    console_main(bot)
        



