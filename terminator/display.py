import os
from platform import system
from terminator.formatter import Formatter


def term_width():
    return os.get_terminal_size().columns


def clear_screen():
    if system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def repaint(jobs):
    clear_screen()
    for job in jobs:
        formatter = Formatter(job)
        print(formatter.job_display())