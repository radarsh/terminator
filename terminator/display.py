import os
from platform import system

import terminator.formatter as formatter
import terminator.arguments as arguments


def term_width():
    return arguments.terminal_width or os.get_terminal_size().columns


def clear_screen():
    if system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def repaint(jobs):
    clear_screen()
    for job in jobs:
        _formatter = formatter.Formatter(job)
        print(_formatter.job_display())