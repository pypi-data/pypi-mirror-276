import requests, time, re, os, zipfile


class AnneProxy:
    def __init__(self, debug=False):
        self.debug = debug

    def format(self, proxy) -> tuple:
        proxy = str(proxy).strip()
        pattern = re.compile(
            r'(?:(?P<user>[^:@|]+):(?P<pass>[^:@|]+)[:@|])?'
            r'(?P<host>[^:@|/]+)'
            r'[:@|](?P<port>\d+)'
            r'(?:[:@|](?P<user2>[^:@|]+):(?P<pass2>[^:@|]+))?'
            r'|'
            r'(?:(?P<user3>[^:@|]+):(?P<pass3>[^:@|]+)@)?'
            r'(?P<host2>[^:@|/]+)'
            r'@(?P<port2>\d+)'
            r'|'
            r'(?P<host3>[^:@|/]+)@(?P<port3>\d+)'
        )
        match = pattern.match(proxy)
        if match:
            user = match.group('user') or match.group('user2') or match.group('user3')
            passw = match.group('pass') or match.group('pass2') or match.group('pass3')
            host = match.group('host') or match.group('host2') or match.group('host3')
            port = match.group('port') or match.group('port2') or match.group('port3')
            return host, port, user, passw
        else:
            return None, None, None, None

    def tmproxy(self,
                mode='get_proxy',
                api_key=None,
                timeout=60):

        if not api_key:
            print('Please set api key')
            return False

        pass




















