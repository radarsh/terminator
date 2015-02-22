import base64
from getpass import getpass


class Arguments:
    base_url = None
    job_list = []
    polling_interval = 10
    username = None
    password = None
    needs_authentication = False
    font = 'cybermedium'
    
    def __init__(self, args):
        Arguments.base_url = args.base_url
        Arguments.job_list = args.job_list.split()
        Arguments.needs_authentication = args.password or args.username
        
        if args.interval:
            Arguments.polling_interval = args.interval
            
        if args.username:
            Arguments.username = args.username
            Arguments.password = getpass('Password: ')
            
        if args.font:
            Arguments.font = args.font

    @staticmethod
    def job_url(job_name):
        return "%s/job/%s/lastBuild/api/json?tree=result,building,duration,timestamp,estimatedDuration" % (Arguments.base_url, job_name)
    
    @staticmethod
    def authorization_header():
        base64_bytes = base64.encodebytes(bytes('%s:%s' % (Arguments.username, Arguments.password), 'utf-8'))[:-1]
        base64_string = str(base64_bytes, 'utf-8')
        return 'Basic %s' % base64_string