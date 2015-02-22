import argparse
import os
from platform import system

from lib.arguments import Arguments


def term_width():
    return os.get_terminal_size().columns


def clear():
    if system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def parse_arguments():
    parser = argparse.ArgumentParser(description='An extremely lightweight terminal based Jenkins build monitor')

    parser.add_argument('base_url', help='Jenkins base URL without the trailing slash')
    parser.add_argument('job_list', help='space-separated list of Jenkins job names')
    parser.add_argument('-i', '--interval', metavar='s', help='polling interval in seconds', type=int)
    parser.add_argument('-u', '--username', metavar='u', help='username if Jenkins needs authentication')
    parser.add_argument('-p', '--password', action='store_true', help='password if Jenkins needs authentication')
    parser.add_argument('-f', '--font', help='font used for rendering the job name')

    args = parser.parse_args()

    Arguments(args)
