import base64
import json
from urllib.request import Request, urlopen

import terminator.arguments as arguments
import terminator.job as job


def parse_jobs():
    jobs = []
    jobNames = []

    if arguments.jobs:
        jobNames = arguments.jobs
    elif arguments.view:
        json_object = _parse_view_response(arguments.view)
        for job in json_object['jobs']:
                jobNames.append(job['name'])
    else:
        json_object = _parse_default_view_response()
        for job in json_object['jobs']:
                jobNames.append(job['name'])

    for job_name in jobNames:
        try:
            job = get_job(job_name)
            jobs.append(job)
        except Exception as e:
            print(e)
            pass
    return jobs


def get_job(job_name):
    json_object = _parse_job_response(job_name)
    return job.Job(job_name, json_object)

def _parse_job_response(job_name):
    request = Request(_job_url(job_name))
    return _parse_api_response(request)

def _parse_view_response(view_name):
    request = Request(_view_url(view_name))
    return _parse_api_response(request)

def _parse_default_view_response():
    request = Request(_default_view_url())
    return _parse_api_response(request)

def _parse_api_response(request):
    if arguments.needs_authentication:
        request.add_header('Authorization', _authorization_header())
    response = urlopen(request)
    json_string = response.read().decode(response.headers.get_content_charset())
    return json.loads(json_string)


def _job_url(job_name):
    return "%s/job/%s/lastBuild/api/json?tree=result,building,duration,timestamp,estimatedDuration" % (
        arguments.base_url, job_name)

def _view_url(view_name):
    return "%s/view/%s/api/json?tree=jobs[name]" % (arguments.base_url, view_name)

def _default_view_url():
    return "%s/api/json?tree=jobs[name]" % (arguments.base_url)

def _authorization_header():
    base64_bytes = base64.encodebytes(bytes('%s:%s' % (arguments.username, arguments.password), 'utf-8'))[:-1]
    base64_string = str(base64_bytes, 'utf-8')
    return 'Basic %s' % base64_string
