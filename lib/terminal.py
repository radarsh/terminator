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
    parser = argparse.ArgumentParser(usage='%(prog)s [options] base_url job_list', description='An extremely lightweight terminal based Jenkins build monitor')

    parser.add_argument('base_url', help='Jenkins base URL without the trailing slash')
    parser.add_argument('job_list', help='space-separated list of Jenkins job names')
    parser.add_argument('-i', metavar='SECONDS', dest='interval', help='polling interval in seconds', type=int)
    parser.add_argument('-u', metavar='USERNAME', dest='username', help='username if Jenkins needs authentication')
    parser.add_argument('-p', dest='password', action='store_true', help='prompt for password')
    parser.add_argument('-f', metavar='FONT', dest='font', help='font used for rendering the job name')

    args = parser.parse_args()

    Arguments(args)
