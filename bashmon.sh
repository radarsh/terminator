#!/usr/bin/env bash

declare username=""
declare password=""
declare base_url=""
declare job_list=""

get_api_response() {
    local query="lastBuild/api/json?pretty=true&tree=result,building,duration,estimatedDuration"
    local job="$1"

    if [ "$username" ]; then
        curl -s -u "$username:$password" "$base_url/job/$job/$query" 
    else
        curl -s "$base_url/job/$job/$query"
    fi 
}

get_build_result() {
    local response="$1"
    echo "$response" | grep result | awk '{print $3}' | sed 's/[",]//g'
}

get_last_duration() {
    local response="$1"
    echo "$response" | grep duration | awk '{print $3}' | sed 's/[",]//g' 
}

get_estimated_duration() {
    local response="$1"
    echo "$response" | grep estimatedDuration | awk '{print $3}' | sed 's/[",]//g' 
}

set_print_colour() {
    local build_result="$1"
    tput bold

    if [ "$build_result" == "SUCCESS" ]; then
        tput setaf 2
    elif [ "$build_result" == "FAILURE" ]; then
        tput setaf 1
    else
        tput setaf 3
    fi
}

print_time() {
    local time_millis="$1"
    ((actual_seconds=$time_millis/1000))
    ((hours=$actual_seconds/3600))
    ((minutes=($actual_seconds%3600)/60))
    ((seconds=$actual_seconds%60))

    local formatted_time=""

    if [ "$hours" != "0" ]; then
        formatted_time="$hours hours"
    fi
    if [ "$minutes" != "0" ]; then
        formatted_time="$formatted_time $minutes minutes"
    fi
    formatted_time="$formatted_time $seconds seconds"

    echo $formatted_time
}

reset_print_colour() {
   tput setaf 7
   tput sgr0 
}

refresh_status() {
    for job in $job_list; do
        local response="$(get_api_response "$job")"
        local build_result="$(get_build_result "$response")"
        local last_duration="$(get_last_duration "$response")"
        local estimated_duration="$(get_estimated_duration "$response")"
        set_print_colour $build_result

        toilet -f banner -t $job
        tput setaf 7
        echo "Last duration $(print_time "$last_duration")"
        echo "Estimated duration $(print_time "$estimated_duration")"

        echo 
    done
    
    reset_print_colour
}

show_help() {
    echo "Usage: ./bashmon.sh -u <username> -p <password> -b <baseurl> -j <jobs>"
}

OPTIND=1

if [ -z "$1" ]; then
    show_help
    exit 0
fi

while getopts "h?u:p:b:j:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    u)  username=$OPTARG
        ;;
    p)  password=$OPTARG
        ;;
    b)  base_url=$OPTARG
        ;;
    j)  job_list=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

refresh_status
