import json
from urllib.request import Request, urlopen

from terminator.arguments import Arguments
from terminator.job import Job


def get_job(job_name):
    json_object = __parse_api_response(job_name)
    return Job(job_name, json_object)

def __parse_api_response(job_name):
    request = Request(Arguments.job_url(job_name))
    if Arguments.needs_authentication:
        request.add_header('Authorization', Arguments.authorization_header())
    response = urlopen(request)
    json_string = response.read().decode(response.headers.get_content_charset())
    return json.loads(json_string)