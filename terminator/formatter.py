import math

from colorama import Back, Fore, Style, init
from pyfiglet import Figlet

import terminator.display
import terminator.arguments as arguments


class Formatter:
    figlet = None
    init(autoreset=True)

    def __init__(self, job):
        self.job = job
        self.term_width = terminator.display.term_width() # TODO I don't know why display needs to be qualified
        Formatter.figlet = Figlet(font=arguments.font, width=self.term_width, justify='center')

    def job_display(self):
        job_bar = self._job_bar_display()
        job_info_strip = self._job_info_strip_display()

        return self._colourise_job_display(job_bar, job_info_strip)

    def _job_bar_display(self):
        rendered_text = Formatter.figlet.renderText(text=self.job.name)

        job_bar = ''
        for line in rendered_text.splitlines():
            line = line.ljust(self.term_width)
            job_bar = job_bar + line + '\n'

        return job_bar[:-1]

    def _job_info_strip_display(self):
        left_width = math.floor(self.term_width / 2)
        right_width = math.ceil(self.term_width / 2)

        if self.job.is_building:
            return ('Started %s' % self.job.built_on).ljust(left_width) + \
                   ('Estimated %s' % self.job.estimated_duration).rjust(right_width)
        else:
            return ('Started %s' % self.job.built_on).ljust(left_width) + \
                   ('Took %s' % self.job.duration).rjust(right_width)

    def _colourise_job_display(self, job_bar, job_info_strip):
        colours = self._colours()
        return '%s%s\n%s%s\n' % (colours[0], job_bar, colours[1], job_info_strip)

    def _colours(self):
        if self.job.is_missing:
            return Back.WHITE + Fore.BLACK + Style.DIM, Back.WHITE + Fore.BLACK + Style.DIM
        elif self.job.is_building:
            return Back.YELLOW + Fore.BLACK + Style.DIM, Back.YELLOW + Fore.BLACK + Style.DIM
        elif self.job.is_successful:
            return Back.GREEN + Fore.BLACK + Style.DIM, Back.GREEN + Fore.BLACK + Style.DIM
        else:
            return Back.RED + Fore.WHITE + Style.BRIGHT, Back.RED + Fore.BLACK + Style.DIM