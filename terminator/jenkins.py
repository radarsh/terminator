import base64
import json
from urllib.request import Request, urlopen

import terminator.arguments as arguments
import terminator.job as job


def parse_jobs():
    jobs = []
    for job_name in arguments.job_list:
        try:
            job = get_job(job_name)
            jobs.append(job)
        except Exception as e:
            print(e)
            pass
    return jobs


def get_job(job_name):
    json_object = _parse_api_response(job_name)
    return job.Job(job_name, json_object)


def _parse_api_response(job_name):
    request = Request(_job_url(job_name))
    if arguments.needs_authentication:
        request.add_header('Authorization', _authorization_header())
    response = urlopen(request)
    json_string = response.read().decode(response.headers.get_content_charset())
    return json.loads(json_string)


def _job_url(job_name):
    return "%s/job/%s/lastBuild/api/json?tree=result,building,duration,timestamp,estimatedDuration" % (
        arguments.base_url, job_name)


def _authorization_header():
    base64_bytes = base64.encodebytes(bytes('%s:%s' % (arguments.username, arguments.password), 'utf-8'))[:-1]
    base64_string = str(base64_bytes, 'utf-8')
    return 'Basic %s' % base64_string
