import urllib.request
import json

baseUrl = "http://localhost:9090"
jobList = ["adarshr-build-war", "adarshr-publish-war"]


def job_url(job_name):
    return baseUrl + "/job/" + job_name + "/lastBuild/api/json?tree=result,building,duration,estimatedDuration"


def get_json(job_name):
    request = urllib.request.Request(job_url(job_name))
    request.add_header('Authorization', 'Basic ')
    response = urllib.request.urlopen(request)
    jsonString = response.read().decode(response.headers.get_content_charset())
    return json.loads(jsonString)


for job in jobList:
    json_object = get_json(job)
    print(json_object['result'])

