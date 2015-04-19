from terminator import arguments as arguments


class State:
    def __init__(self):
        self.current_jobs = []
        self.previous_jobs = []
        self.refresh_counter = 0

    def needs_job_name_refresh(self):
        return self.refresh_counter >= arguments.refresh_view_frequency

    def reset_job_refresh_counter(self):
        self.refresh_counter = 0

