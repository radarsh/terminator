import math
from datetime import datetime, timedelta

from ago import human


class Job:
    def __init__(self, name, response):
        self.name = name
        self.is_successful = response['result'] == 'SUCCESS'
        self.is_building = response['building'] == True
        self.duration_millis = response['duration']
        self.estimated_duration_millis = response['estimatedDuration']
        self.timestamp_millis = response['timestamp']
        self.duration = self._friendly_duration()
        self.estimated_duration = self._friendly_estimated_duration()
        self.built_on = self._friendly_built_on()

    def _friendly_duration(self):
        if self.duration_millis < 1000:
            return 'negligible'

        time_delta = timedelta(milliseconds=self.duration_millis)
        return human(time_delta, precision=1, past_tense='{}', future_tense='{}')
    
    def _friendly_estimated_duration(self):
        time_delta = timedelta(milliseconds=self.estimated_duration_millis)
        return human(time_delta, precision=1, past_tense='{}', future_tense='{}')

    def _friendly_built_on(self):
        timestamp = math.floor(self.timestamp_millis / 1000)

        if datetime.now().timestamp() - timestamp < 10:
            return 'moments ago'

        date = datetime.fromtimestamp(timestamp)

        return human(date, precision=1)

    def __eq__(self, other):
        return (self.name == other.name
                and self.timestamp_millis == other.timestamp_millis
                and self.duration_millis == other.duration_millis
                and self.is_successful == other.is_successful
                and self.is_building == other.is_building)