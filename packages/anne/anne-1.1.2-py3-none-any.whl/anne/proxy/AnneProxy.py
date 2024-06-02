import requests, time, re, os, zipfile
from .utils import *

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
                api_key=None,
                mode='get_proxy',
                timeout=60):

        if not api_key: print('Vui lòng đặt api key'); return False

        api_url = "https://tmproxy.com/api/proxy"

        if mode == 'get_proxy':
            try:
                url = f"{api_url}/get-new-proxy"
                payload = {"api_key": api_key}
                headers = {"Content-Type": "application/json"}
                proxy_https = None
                start_time = time.time()
                while not proxy_https:
                    if time.time() - start_time > timeout: break
                    response = requests.post(url, json=payload, headers=headers)
                    if not response.status_code == 200: return None
                    data = response.json()
                    proxy_https = data['data'].get('https')
                    if not proxy_https: time.sleep(1); continue
                    return None
                return proxy_https
            except Exception as e:
                if self.debug: print(f"Lỗi: {e}")
                return False

        elif mode == 'check-key':
            try:
                url = f"{api_url}/stats"

                payload = {"api_key": api_key}

                response = requests.post(url, json=payload)
                if not response.status_code == 200: return False
                if response.json()['message'] == 'API không tồn tại': return False
                return True
            except Exception as e:
                if self.debug: print(f"Lỗi: {e}")
                return False

    def tinsoftproxy(self,
                     api_key=None,
                     mode='get_proxy',
                     timeout=60):

        if not api_key:
            print('Vui lòng đặt api key')
            return False

        if mode == 'get_proxy':
            try:
                start_time = time.time()
                while True:
                    if time.time() - start_time > timeout:
                        break
                    try:
                        response = requests.get(f"http://proxy.tinsoftsv.com/api/changeProxy.php?key={api_key}")
                        if not response.status_code == 200: return None
                        data = response.json()
                        if data['success']: return data['proxy']
                        else:
                            if 'next_change' in data:
                                wait_time = int(data['next_change']) + 1
                                time.sleep(wait_time)
                            else: return None
                    except requests.exceptions.RequestException:
                        time.sleep(10)
            except Exception as e:
                if self.debug: print(f"Lỗi: {e}"); return False

        elif mode == 'check-key':
            try:
                response = requests.get(f"http://proxy.tinsoftsv.com/api/getKeyInfo.php?key={api_key}")
                if not response.status_code == 200: return False
                if response.json()['success']: return True
                else: return False
            except Exception as e:
                if self.debug: print(f"Lỗi: {e}"); return False

    def wwproxy(self,
                api_key=None,
                mode='get_proxy',
                timeout=60):

        if not api_key: print('Vui lòng đặt api key'); return False

        if mode == 'get_proxy':
            try:
                start_time = time.time()
                while True:
                    if time.time() - start_time > timeout: break
                    response = requests.get(f"https://wwproxy.com/api/client/proxy/available?key={api_key}&provinceId=-1")
                    if not response.status_code == 200: return None
                    if response.json()['status'] == 'OK': return response.json()['data']['proxy']
                    time.sleep(1)
                return None
            except Exception as e:
                if self.debug: print(f"Lỗi: {e}"); return False

        elif mode == 'check-key': print('Chưa hỗ trợ chức năng này'); return False








