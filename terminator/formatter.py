import math

from colorama import Back, Fore, Style, init
from pyfiglet import Figlet

from terminator.arguments import *
from terminator.display import term_width


class Formatter:
    figlet = None
    init(autoreset=True)
    terminal_width = -1

    def __init__(self, job):
        self.job = job
        Formatter._init_formatter()

    @classmethod
    def _init_formatter(cls):
        cls.terminal_width = term_width()
        cls.figlet = Figlet(font=font, width=Formatter.terminal_width, justify='center')

    def job_display(self):
        job_bar = self._job_bar_display()
        job_info_strip = self._job_info_strip_display()

        return self._colourise_job_display(job_bar, job_info_strip)

    def _job_bar_display(self):
        rendered_text = Formatter.figlet.renderText(text=self.job.name)

        job_bar = ''
        for line in rendered_text.splitlines():
            line = line.ljust(Formatter.terminal_width)
            job_bar = job_bar + line + '\n'

        return job_bar[:-1]

    def _job_info_strip_display(self):
        if self.job.is_building:
            return ('Started %s' % self.job.built_on).ljust(math.floor(Formatter.terminal_width / 2)) + \
               ('Estimated %s' % self.job.estimated_duration).rjust(math.ceil(Formatter.terminal_width / 2))
        else:
            return ('Started %s' % self.job.built_on).ljust(math.floor(Formatter.terminal_width / 2)) + \
                   ('Took %s' % self.job.duration).rjust(math.ceil(Formatter.terminal_width / 2))

    def _colourise_job_display(self, job_bar, job_info_strip):
        colours = self._colours()
        return '%s%s\n%s%s\n' % (colours[0], job_bar, colours[1], job_info_strip)

    def _colours(self):
        if self.job.is_building:
            return Back.YELLOW + Fore.BLACK, Back.YELLOW + Fore.BLACK
        elif self.job.is_successful:
            return Back.GREEN + Fore.WHITE + Style.BRIGHT, Back.GREEN + Fore.BLACK + Style.DIM
        else:
            return Back.RED + Fore.BLACK, Back.RED + Fore.BLACK