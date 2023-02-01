#!/usr/bin/python3

def run_console():
    while True:
        text = input('> ')
        if not text.startswith('!'): continue
        [command, *args] = text[1:].split()

        if command == 'help':
            print('Commands: help, echo, exit')
            continue

        if command == 'echo':
            print(' '.join(args))
            continue

        if command == 'exit':
            return

if __name__ == '__main__': run_console()