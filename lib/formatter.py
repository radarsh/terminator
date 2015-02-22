import math

from colorama import Back, Fore, init
from pyfiglet import Figlet

from lib.arguments import Arguments
from lib.terminal import term_width


class Formatter:
    figlet = None
    init(autoreset=True)
    terminal_width = -1

    def __init__(self, job):
        self.job = job
        Formatter.__init_formatter()

    @classmethod
    def __init_formatter(cls):
        cls.terminal_width = term_width()
        cls.figlet = Figlet(font=Arguments.font, width=Formatter.terminal_width, justify='center')

    def job_display(self):
        job_bar = self.__job_bar_display()
        job_info_strip = self.__job_info_strip_display()

        return self.__colourise_job_display(job_bar, job_info_strip)

    def __job_bar_display(self):
        rendered_text = Formatter.figlet.renderText(text=self.job.name)

        job_bar = ''
        for line in rendered_text.splitlines():
            line = line.ljust(Formatter.terminal_width)
            job_bar = job_bar + line + '\n'

        return job_bar[:-1]

    def __job_info_strip_display(self):
        return ('Built %s' % self.job.built_on).ljust(math.floor(Formatter.terminal_width / 2)) + \
               ('Took %s' % self.job.duration).rjust(math.ceil(Formatter.terminal_width / 2))

    def __colourise_job_display(self, job_bar, job_info_strip):
        colours = self.__colours()
        return '%s%s\n%s%s\n' % (colours[0], job_bar, colours[1], job_info_strip)

    def __colours(self):
        if self.job.is_successful:
            return Back.GREEN + Fore.WHITE, Back.GREEN + Fore.BLACK
        elif self.job.is_building:
            return Back.YELLOW + Fore.WHITE, Back.YELLOW + Fore.BLACK
        else:
            return Back.RED + Fore.WHITE, Back.RED + Fore.BLACK