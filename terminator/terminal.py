import time

from terminator import jenkins
import terminator.arguments as arguments
import terminator.display as display
from terminator.state import State


state = State()


def repaint():
    if not state.current_jobs:
        display.clear_screen()

    if state.needs_job_name_refresh() or not state.current_jobs:
        job_names = jenkins.get_job_names()
        state.current_jobs = jenkins.get_jobs(job_names)
        state.reset_job_refresh_counter()

    state.current_jobs = jenkins.refresh_jobs(state.current_jobs)

    if state.previous_jobs != state.current_jobs:
        display.repaint(state.current_jobs)
        state.previous_jobs = state.current_jobs

    state.refresh_counter += 1

    pause()


def pause():
    time.sleep(arguments.refresh_job_interval)