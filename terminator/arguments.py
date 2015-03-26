import argparse
from getpass import getpass

base_url = None
jobs = []
polling_interval = 10
username = None
password = None
needs_authentication = False
font = 'cybermedium'
terminal_width = None
view = None


def parse_arguments():
    parser = argparse.ArgumentParser(prog='terminator', usage='%(prog)s [options] base_url',
                                     description='An extremely lightweight terminal based Jenkins build monitor')

    parser.add_argument('base_url', help='Jenkins base URL without the trailing slash')
    parser.add_argument('-j', metavar='JOBS', dest='jobs', help='space-separated list of Jenkins job names')
    parser.add_argument('-i', metavar='SECONDS', dest='interval', help='polling interval in seconds', type=int)
    parser.add_argument('-u', metavar='USERNAME', dest='username', help='username if Jenkins needs authentication')
    parser.add_argument('-v', metavar='VIEW', dest='view', help='which view you want termintor to display the jobs for')
    parser.add_argument('-p', dest='password', action='store_true', help='prompt for password')
    parser.add_argument('-f', metavar='FONT', dest='font', help='font used for rendering the job name')
    parser.add_argument('-w', metavar='WIDTH', dest='terminal_width', help='terminal width override', type=int)

    args = parser.parse_args()

    _init(args)


def _init(args):
    global base_url
    base_url = args.base_url
   
    global needs_authentication
    needs_authentication = args.password or args.username

    if args.view:
        global view
        view = args.view

    if args.jobs:
        global jobs
        jobs = args.jobs.split()
	
    if args.interval:
        global polling_interval
        polling_interval = args.interval

    if args.username:
        global username, password
        username = args.username
        password = getpass('Password: ')

    if args.font:
        global font
        font = args.font

    if args.terminal_width:
        global terminal_width
        terminal_width = args.terminal_width
