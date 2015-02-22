from datetime import datetime, timedelta

from ago import human


class Job:
    def __init__(self, name, response):
        self.name = name
        self.is_successful = response['result'] == 'SUCCESS'
        self.is_building = response['building'] == True
        self.duration = Job.__friendly_duration(response['duration'])
        self.built_on = Job.__friendly_built_on(response['timestamp'])

    @staticmethod
    def __friendly_duration(duration_millis):
        if duration_millis < 1000:
            return 'negligible'

        time_delta = timedelta(milliseconds=duration_millis)
        return human(time_delta, precision=1, past_tense='{}', future_tense='{}')

    @staticmethod
    def __friendly_built_on(timestamp_millis):
        timestamp = timestamp_millis / 1000
        date = datetime.fromtimestamp(timestamp)
        return human(date)