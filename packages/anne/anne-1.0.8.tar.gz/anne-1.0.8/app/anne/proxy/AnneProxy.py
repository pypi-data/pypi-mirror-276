
import requests, time, re
from .utils import *




class AnneProxy:
    def __init__(self, debug=False):
        self.debug = debug
        
    def format(self, proxy)->tuple:
        proxy = str(proxy).strip()
        pattern = re.compile(
            r'(?:(?P<user>[^:@]+):(?P<pass>[^:@]+)[:@])?'
            r'(?P<host>[^:@/]+)'
            r':(?P<port>\d+)'
            r'(?:[:@](?P<user2>[^:@]+):(?P<pass2>[^:@]+))?'
        )
        match = pattern.match(proxy)
        if match:
            user = match.group('user') if match.group('user') else match.group('user2')
            passw = match.group('pass') if match.group('pass') else match.group('pass2')
            return match.group('host'), match.group('port'), user, passw
        else:
            return None, None, None, None































