import time

from terminator.jenkins import parse_jobs
from terminator.arguments import *
from terminator.display import clear_screen, repaint


def pause():
    time.sleep(polling_interval)


def loop():
    previous_jobs = []

    while True:
        if not previous_jobs:
            clear_screen()

        current_jobs = parse_jobs()

        if previous_jobs != current_jobs:
            repaint(current_jobs)

        previous_jobs = current_jobs

        pause()


def main():
    parse_arguments()
    try:
        loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()