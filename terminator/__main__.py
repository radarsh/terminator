import time

from terminator.jenkins import get_job
from terminator.arguments import Arguments
from terminator.terminal import parse_arguments, clear
from terminator.formatter import Formatter


def pause():
    time.sleep(Arguments.polling_interval)


def print_jobs(jobs):
    for job in jobs:
        formatter = Formatter(job)
        print(formatter.job_display())


def parse_jobs(jobs):
    for job_name in Arguments.job_list:
        try:
            job = get_job(job_name)
            jobs.append(job)
        except Exception as e:
            print(e)
            pass


def loop():
    previous_jobs = []
    current_jobs = []

    while True:
        if not previous_jobs:
            clear()

        parse_jobs(current_jobs)

        if previous_jobs != current_jobs:
            clear()
            print_jobs(current_jobs)

        previous_jobs = current_jobs
        current_jobs = []

        pause()


def main():
    parse_arguments()
    try:
        loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()