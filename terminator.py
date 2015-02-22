import time

from lib.jenkins import parse_api_response
from lib.arguments import Arguments
from lib.terminal import parse_arguments, clear
from lib.formatter import Formatter
from lib.job import Job


def pause():
    time.sleep(Arguments.polling_interval)


def loop():
    while True:
        for job_name in Arguments.job_list:
            response = parse_api_response(job_name)
            job = Job(job_name, response)
            formatter = Formatter(job)

            print(formatter.job_display())

        pause()
        clear()


def main():
    parse_arguments()
    try:
        loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()