import time

import terminator.display as display
import terminator.arguments as arguments
import terminator.jenkins as jenkins


def pause():
    time.sleep(arguments.polling_interval)


def loop():
    previous_jobs = []

    while True:
        if not previous_jobs:
            display.clear_screen()

        current_jobs = jenkins.parse_jobs()

        if previous_jobs != current_jobs:
            display.repaint(current_jobs)

        previous_jobs = current_jobs

        pause()


def main():
    arguments.parse_arguments()
    try:
        loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()