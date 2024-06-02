import requests


class AnneCaptcha:
    def __init__(self, debug=False):
        self.debug = debug

    def submitCaptcha(self, driver, token):
        try:
            driver.execute_script(f'parent.postMessage(JSON.stringify({{"eventId": "challenge-complete", "payload": {{"sessionToken": "{token}"}}}}), "*");')
            return True
        except Exception as e:
            if self.debug: print(f"Lỗi [submitCaptcha]: {e}"); return False

    def rockcaptcha(self, api_key=None, mode='microsoft', timeout=60):
        try:
            if not api_key: print('Vui lòng đặt api key'); return False

            if mode == 'check':
                url = f"https://api.rockcaptcha.com/user/balance"
                params = {"apikey": api_key}
                result = requests.get(url, params=params)
                if result.status_code != 200: return False
                result = result.json()
                if self.debug: print(result)
                if result['code'] != 0: return False
                elif result['code'] == 0: return result['Balance']

            elif mode == 'microsoft':
                url = 'https://api.rockcaptcha.com/FunCaptchaTokenTask'
                params = {'apikey': api_key, 'sitekey': 'B7D8911C-5CC8-A9A3-35B0-554ACEE604DA', 'siteurl': 'https://signup.live.com', 'affiliateid': '37007'}
                response = requests.get(url, params=params)
                if not response.status_code == 200: return False
                data = response.json()
                url = f"https://api.rockcaptcha.com/getresult"
                params = {'apikey': api_key, 'taskId': data['TaskId']}
                start_time = time.time()
                while True:
                    if time.time() - start_time > timeout: return False
                    response = requests.get(url, params=params)
                    if not response.status_code == 200: return False
                    result = response.json()
                    if result['Status'] == 'SUCCESS': return result['Data']['Token']
                    elif result['Status'] == 'ERROR': return False
                    elif result['Status'] == 'PENDING': continue
                    elif result['Status'] == 'PROCESSING': continue

            else: print(f'Không hỗ trợ mode: {mode}'); return False

        except Exception as e:
            if self.debug: print(f"Lỗi [rockcaptcha]: {e}");
            return False

    def ezcaptcha(self, api_key=None, mode='microsoft', timeout=60):
        try:

            if not api_key: print('Vui lòng đặt api key'); return False

            if mode == 'check':
                url = f"https://api.ez-captcha.com/getBalance"
                params = {"clientKey": api_key}
                result = requests.post(url, json=params)
                if result.status_code != 200: return False
                result = result.json()
                if result['errorId'] != 0: return False
                return result['balance']

            elif mode == 'microsoft':
                url = 'https://api.ez-captcha.com/createTask'
                params = {'clientKey': api_key, 'appId': '40523', 'task': {'websiteURL': 'https://signup.live.com', 'websiteKey': 'B7D8911C-5CC8-A9A3-35B0-554ACEE604DA', 'type': 'FuncaptchaTaskProxyless'}}
                response = requests.post(url, json=params)
                if not response.status_code == 200: return False
                data = response.json()
                taskId = data['taskId']
                url = f"https://api.ez-captcha.com/getTaskResult"
                params = {'clientKey': self.api_key, 'taskId': taskId}
                time_start = time.time()
                while True:
                    if time.time() - time_start > timeout: return False
                    result = requests.post(url, json=params)
                    if result.status_code != 200: return False
                    result = result.json()
                    if result['errorId'] != 0: return False
                    if result['status'] != 'ready': continue
                    elif result['status'] == 'ready': return result['solution']['token']

            else: print(f'Không hỗ trợ mode: {mode}'); return False

        except Exception as e:
            if self.debug: print(f"Lỗi [ezcaptcha]: {e}");
            return False








