import base64
import urllib.request
import json
import time
import datetime
import os
import re
import argparse
import ago
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
    job_list = args.job_list.split(',')

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


def refresh_loop():
    while True:
        for job in job_list:
            json_object = parse_json(job)
            success = json_object["result"] == 'SUCCESS'
            building = json_object["building"] == True
            duration = json_object["duration"]
            built_on = datetime.datetime.fromtimestamp(json_object["timestamp"] / 1000) #.strftime('%d-%m-%Y %H:%M:%S')
            term_width = os.get_terminal_size().columns
            figlet = Figlet(font='cybermedium', width=term_width)

            text = figlet.renderText(job)

            padding_length = int((term_width - len(text) / 4) / 2)
            padding = ' ' * padding_length

            text = re.sub('\n', padding + '\n' + padding, text)
            text = padding + text
            text = text[:-(padding_length + 1)]
            # text = re.sub('', padding, text)

            # text = padding + text + padding

            if success:
                print(colored(text, color='white', on_color='on_green', attrs=['bold']), end='\r')
                print(colored(('Last build: %s, Took: %s' %(
                    ago.human(built_on),
                    ago.human(datetime.timedelta(milliseconds=duration), precision=1, past_tense='{}', future_tense='{}'))
                ).center(term_width), 'grey', 'on_green'))

            elif building:
                print(colored(text, 'grey', 'on_yellow'))
            else:
                print(colored(text, 'grey', 'on_red'))

            print('\n')

        time.sleep(polling_interval)

        os.system("clear")


parse_arguments()
refresh_loop()
