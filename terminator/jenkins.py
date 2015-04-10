import base64
import json
from urllib.request import Request, urlopen

import terminator.arguments as arguments
import terminator.job as job


def refresh_jobs(jobs):
    for job in jobs:
        try:
            _job = _get_job(job.name)
        except Exception as e:
            job.is_missing = True
            pass
    return jobs

def get_jobs(job_list):
    jobs = []

    for job_name in job_list:
        try:
            _job = _get_job(job_name)
            jobs.append(_job)
        except Exception as e:
            print(e)
            pass
    return jobs


def _get_job_names():
    if arguments.jobs:
        return arguments.jobs
    elif arguments.view:
        return _get_job_names_from_view(arguments.view)
    else:
        return _get_job_names_from_default_view()


def _get_job(job_name):
    request = Request(_job_url(job_name))
    json_object = _get_json(request)
    return job.Job(job_name, json_object)


def _get_job_names_from_view(view_name):
    request = Request(_view_url(view_name))
    json_object = _get_json(request)
    return [_job['name'] for _job in json_object['jobs']]


def _get_job_names_from_default_view():
    request = Request(_default_view_url())
    json_object = _get_json(request)
    return [_job['name'] for _job in json_object['jobs']]


def _get_json(request):
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
    return "%s/api/json?tree=jobs[name]" % arguments.base_url


def _authorization_header():
    base64_bytes = base64.encodebytes(bytes('%s:%s' % (arguments.username, arguments.password), 'utf-8'))[:-1]
    base64_string = str(base64_bytes, 'utf-8')
    return 'Basic %s' % base64_string
