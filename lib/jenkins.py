import json
from urllib.request import Request, urlopen

from lib.arguments import Arguments


def parse_api_response(job):
    request = Request(Arguments.job_url(job))
    if Arguments.needs_authentication:
        request.add_header('Authorization', Arguments.authorization_header())

    response = urlopen(request)
    json_string = response.read().decode(response.headers.get_content_charset())
    return json.loads(json_string)