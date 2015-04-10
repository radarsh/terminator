import time

import terminator.display as display
import terminator.arguments as arguments
import terminator.jenkins as jenkins


def pause():
    time.sleep(arguments.refresh_job_interval)


def loop():
    jobs = []
    refresh_counter = 0

    while True:

        if refresh_counter >= arguments.refresh_view_frequency:
            job_names = jenkins._get_job_names()
            jobs = jenkins.get_jobs(job_names)
            refresh_counter=0
        elif not jobs:
            display.clear_screen()
            job_names = jenkins._get_job_names()
            jobs = jenkins.get_jobs(job_names)
        else:
            jobs = jenkins.refresh_jobs(jobs)

        display.repaint(jobs)

        refresh_counter+=1

        pause()

def main():
    arguments.parse_arguments()
    try:
        loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()