#!/usr/bin/env bash

declare jenkins_host="$1"
declare jobs="$2"
declare query="lastBuild/api/json?pretty=true&tree=result,building"

for job in $jobs; do
	toilet -f standard -t $job
	tput setaf 2
	curl -s "$jenkins_host/job/$job/$query" | grep result | awk '{print $3}' | sed 's/[",]//g' | toilet -t -f mini
	tput sgr0
	echo 
done

