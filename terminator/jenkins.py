import base64
import json
from urllib.request import Request, urlopen

from terminator.arguments import *
from terminator.arguments import job_list
from terminator.job import Job


def parse_jobs():
    jobs = []
    for job_name in job_list:
        try:
            job = get_job(job_name)
            jobs.append(job)
        except Exception as e:
            print(e)
            pass
    return jobs


def get_job(job_name):
    json_object = _parse_api_response(job_name)
    return Job(job_name, json_object)


def _parse_api_response(job_name):
    request = Request(_job_url(job_name))
    if needs_authentication:
        request.add_header('Authorization', _authorization_header())
    response = urlopen(request)
    json_string = response.read().decode(response.headers.get_content_charset())
    return json.loads(json_string)


def _job_url(job_name):
    return "%s/job/%s/lastBuild/api/json?tree=result,building,duration,timestamp,estimatedDuration" % (
        base_url, job_name)


def _authorization_header():
    base64_bytes = base64.encodebytes(bytes('%s:%s' % (username, password), 'utf-8'))[:-1]
    base64_string = str(base64_bytes, 'utf-8')
    return 'Basic %s' % base64_string
