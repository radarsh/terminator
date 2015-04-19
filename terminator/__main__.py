from terminator import terminal
import terminator.arguments as arguments


def loop():
    while True:
        terminal.repaint()


def main():
    arguments.parse_arguments()
    try:
        loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()