import urllib.request
import json
import time
import datetime
import os

base_url = "http://localhost:9090"
job_list = ["adarshr-build-war", "adarshr-publish-war"]
recheck_interval = 10

def job_url(job_name):
    return base_url + "/job/" + job_name + "/lastBuild/api/json?tree=result,building,duration,timestamp"


def get_json(job_name):
    request = urllib.request.Request(job_url(job_name))
    request.add_header('Authorization', 'Basic ')
    response = urllib.request.urlopen(request)
    jsonString = response.read().decode(response.headers.get_content_charset())
    return json.loads(jsonString)

"""
  "building" : false,
  "description" : null,
  "duration" : 164875,
  "estimatedDuration" : 201745,
  "executor" : null,
  "fullDisplayName" : "adarshr-build-war #61",
  "id" : "2015-01-15_20-06-04",
  "keepLog" : false,
  "number" : 61,
  "result" : "SUCCESS",
  "timestamp" : 1421352364000,
"""


while True:
    for job in job_list:
        json_object = get_json(job)
        result_ = json_object["result"]
        built_on = datetime.datetime.fromtimestamp(json_object["timestamp"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print("Job name: %s, Result %s, Built on %s" %(job, result_, built_on))

    time.sleep(recheck_interval)
    os.system("cls")




