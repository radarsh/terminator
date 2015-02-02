#!/usr/bin/env bash

declare jenkins_host="$1"
declare jobs="$2"

echo Jenkins host $jenkins_host
echo Job list $jobs

for job in $jobs; do toilet -f standard -t $job; echo $jenkins_host/job/$job/adfdsaf ;curl $jenkins_host/job/$job/lastBuild/api/json 2> /dev/null | python -m json.tool | grep result | awk '{print $2}' | sed 's/[",]//g' | toilet -t -f mini -F gay ; echo; done
