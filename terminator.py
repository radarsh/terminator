import base64
import urllib.request
import json
import time
import datetime
import os
import re
import argparse
from ago import human
from termcolor import colored
from pyfiglet import Figlet

base_url = None
job_list = []
polling_interval = 10
username = None
password = None

def parse_arguments():
    global base_url, job_list, polling_interval, username, password

    parser = argparse.ArgumentParser(description='An extremely lightweight terminal based Jenkins build monitor')

    parser.add_argument('base_url', help='Jenkins base URL without the trailing slash')
    parser.add_argument('job_list', help='comma-separated list of Jenkins jobs that needs monitoring')
    parser.add_argument('--interval', metavar='seconds', help='polling interval in seconds', type=int)
    parser.add_argument('--username', metavar='u', help='username if Jenkins needs authentication')
    parser.add_argument('--password', metavar='p', help='password if Jenkins needs authentication')

    args = parser.parse_args()

    base_url = args.base_url
    job_list = args.job_list.split()

    if args.interval:
        polling_interval = args.interval

    if args.username:
        username = args.username
        password = args.password


def job_url(job):
    return "%s/job/%s/lastBuild/api/json?tree=result,building,duration,timestamp" %(base_url, job)


def parse_json(job):
    request = urllib.request.Request(job_url(job))
    add_auth_header(request)
    response = urllib.request.urlopen(request)
    json_string = response.read().decode(response.headers.get_content_charset())
    return json.loads(json_string)


def add_auth_header(request):
    if username:
        base64_bytes = base64.encodebytes(bytes('%s:%s' % (username, password), 'utf-8'))[:-1]
        base64_string = str(base64_bytes, 'utf-8')
        request.add_header('Authorization', 'Basic %s' %(base64_string))


"""
asc_____
banner
charact2
clb8x8
clb8x10
clr6x6
computer
cybermedium
cyberlarge
doom
puffy
sansb
standard
straight
thick
"""

def format_job_name(job, success, building, duration, built_on):
    term_width = os.get_terminal_size().columns
    figlet = Figlet(font='cybermedium', width=term_width, justify='center')

    figlet_text = figlet.renderText(text=job)

    formatted_text = ''
    for line in figlet_text.splitlines():
        line = line.ljust(term_width)
        formatted_text = formatted_text + line + '\n'

    return formatted_text[:-1]


def refresh_loop():
    while True:
        for job in job_list:
            json_object = parse_json(job)
            success = json_object["result"] == 'SUCCESS'
            building = json_object["building"] == True
            duration = json_object["duration"]
            built_on = datetime.datetime.fromtimestamp(json_object["timestamp"] / 1000)

            formatted_job_name = format_job_name(job, success, building, duration, built_on)

            term_width = os.get_terminal_size().columns

            duration_human = 'negligible'
            if duration >= 1000:
                duration_human = human(datetime.timedelta(milliseconds=duration), precision=1, past_tense='{}', future_tense='{}')

            built_on_human = human(built_on)
            built_on_string = ('Built %s' %built_on_human).ljust(int(term_width / 2))
            duration_string = ('Took %s' %duration_human).rjust(int(term_width / 2))

            if success:
                print(colored(formatted_job_name, color='white', on_color='on_green', attrs=['bold']))
                print(colored(built_on_string + duration_string, 'grey', 'on_green'))

            elif building:
                print(colored(formatted_job_name, 'grey', 'on_yellow'))
                print(colored(built_on_string + duration_string, 'grey', 'on_yellow'))

            else:
                print(colored(formatted_job_name, 'grey', 'on_red'))
                print(colored(built_on_string + duration_string, 'grey', 'on_red'))

            print('\n')

        time.sleep(polling_interval)

        os.system("clear")


parse_arguments()
refresh_loop()
