from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time, random
from .utils import *



"""
    
Version: 28/05/2024
Developer: AnneHouman

"""


class AnneBrowser:
    # DEBUG = True
    
    def __init__(self, driver=None, debug=False):
        self.driver = driver
        self.DEBUG = debug
    
    def createDriver(self, browser='chrome', data=None): # Tạo driver
        """ Giá trị của các tham số:
        
        browser: 'chrome', 'firefox'
        
        data: {
            "headless": True,  # True hoặc False
            "proxy": {
                "mode": 0,  # 0: Không sử dụng proxy, 1: Sử dụng proxy
                "host": None,  # None hoặc str
                "port": None,  # None hoặc int
                "username": None,  # None hoặc str
                "password": None  # None hoặc str
            },
            "user_agent": 0,  # 0: Không sử dụng user agent, 1: Sử dụng user agent ngẫu nhiên, 2: Sử dụng user agent cố định
            "window_size": None,  # None hoặc (width, height) - tuple | Ví dụ: (1920, 1080)
            "antibot": False,  # True hoặc False
        """
        if browser == 'chrome': return self._chrome_driver(data)
     
    def _chrome_driver(self, data=None): # Tạo driver cho Chrome
        if not data: return webdriver.Chrome(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        
        if data.get('headless', False) is True: chrome_options.add_argument("--headless")
        
        if data.get('proxy', None) is not None:
            proxy = data['proxy']
            if proxy['mode'] == 1:
                chrome_options.add_argument(f"--proxy-server={proxy['host']}:{proxy['port']}")
                if proxy['username'] and proxy['password']:
                    chrome_options.add_argument(f"--proxy-auth={proxy['username']}:{proxy['password']}")
            else: pass
        
        if data.get('user_agent', 0) == 0: pass
        elif data['user_agent'] == 1: chrome_options.add_argument(f"user-agent={get_ua()}")
        else: chrome_options.add_argument(f"user-agent={data['user_agent']}")
        
        if data.get('window_size', None) is not None: chrome_options.add_argument(f"--window-size={data['window_size'][0]},{data['window_size'][1]}")
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        return driver
         
    
    def _locator_type(self, locator): # Định dạng loại locator
        """Định dạng loại locator

        Args:
            locator (str): 'xpath', 'css', 'id', 'name', 'linktext1', 'linktext2', 'class', 'tag'

        Raises:
            ValueError: Nếu locator không hợp lệ thì sẽ báo lỗi

        Returns:
            str: Trả về loại locator
        """
        locator_mapping = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'name': By.NAME,
            'linktext1': By.LINK_TEXT,
            'linktext2': By.PARTIAL_LINK_TEXT,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME
        }
        if locator in locator_mapping: return locator_mapping[locator]
        else: raise ValueError(f"Locator không hợp lệ: {locator}")

    def _wait_mode(self, wait_mode): # Định dạng loại chờ
        """Định dạng loại chờ

        Args:
            wait_mode (str): 'hienthi', 'tontai', 'cotheclick', 'cothechon', 'dachon', 'khonghienthi', 'khongtontai', 'frameok'

        Raises:
            ValueError: Nếu wait_mode không hợp lệ thì sẽ báo lỗi

        Returns:
            _type_: Trả về loại chờ
        """
        condition_mapping = {
            'hienthi': EC.visibility_of_element_located,
            'tontai': EC.presence_of_element_located,
            'cotheclick': EC.element_to_be_clickable,
            'cothechon': EC.element_located_to_be_selected,
            'dachon': EC.element_selection_state_to_be,
            'khonghienthi': EC.invisibility_of_element_located,
            'khongtontai': EC.staleness_of,
            'frameok': EC.frame_to_be_available_and_switch_to_it
        }
        if wait_mode in condition_mapping:
            return condition_mapping[wait_mode]
        else: raise ValueError(f"Waitmode không hợp lệ: {wait_mode}")

    def _keys_type(self, keys): # Định dạng loại phím
        """Định dạng loại phím

        Args:
            keys (str): 'enter', 'space', 'tab', 'esc', 'up', 'down', 'left', 'right', 'backspace', 'delete', 'shift', 'ctrl', 'alt', 'pause', 'escape', 'page_up', 'page_down', 'end', 'home', 'insert', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'command', 'num_lock', 'scroll_lock', 'caps_lock', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'multiply', 'add', 'separator', 'subtract', 'decimal', 'divide'

        Returns:
            keys: Trả về loại phím
        """
        keys_mapping = {
            'enter': Keys.ENTER,
            'space': Keys.SPACE,
            'tab': Keys.TAB,
            'esc': Keys.ESCAPE,
            'up': Keys.ARROW_UP,
            'down': Keys.ARROW_DOWN,
            'left': Keys.ARROW_LEFT,
            'right': Keys.ARROW_RIGHT,
            'backspace': Keys.BACK_SPACE,
            'delete': Keys.DELETE,
            'shift': Keys.SHIFT,
            'ctrl': Keys.CONTROL,
            'alt': Keys.ALT,
            'pause': Keys.PAUSE,
            'escape': Keys.ESCAPE,
            'page_up': Keys.PAGE_UP,
            'page_down': Keys.PAGE_DOWN,
            'end': Keys.END,
            'home': Keys.HOME,
            'insert': Keys.INSERT,
            'f1': Keys.F1,
            'f2': Keys.F2,
            'f3': Keys.F3,
            'f4': Keys.F4,
            'f5': Keys.F5,
            'f6': Keys.F6,
            'f7': Keys.F7,
            'f8': Keys.F8,
            'f9': Keys.F9,
            'f10': Keys.F10,
            'f11': Keys.F11,
            'f12': Keys.F12,
            'command': Keys.COMMAND,
            'num0': Keys.NUMPAD0,
            'num1': Keys.NUMPAD1,
            'num2': Keys.NUMPAD2,
            'num3': Keys.NUMPAD3,
            'num4': Keys.NUMPAD4,
            'num5': Keys.NUMPAD5,
            'num6': Keys.NUMPAD6,
            'num7': Keys.NUMPAD7,
            'num8': Keys.NUMPAD8,
            'num9': Keys.NUMPAD9,
            'multiply': Keys.MULTIPLY,
            'add': Keys.ADD,
            'separator': Keys.SEPARATOR,
            'subtract': Keys.SUBTRACT,
            'decimal': Keys.DECIMAL,
            'divide': Keys.DIVIDE
        }
        return keys_mapping.get(keys, None)

    def waitPageLoad(self, wait_mode='full', timeout=30): # Chờ trang load
        """Chờ trang load

        Args:
            wait_mode (str, optional): Waitmode. Defaults to 'full'.
            timeout (int, optional): Timeout. Defaults to 30.

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        try:
            if wait_mode == 'full': WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            elif wait_mode == 'content': WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            elif wait_mode == 'net0': WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_script('return window.performance.getEntriesByType("resource").length') == 0)
            elif wait_mode == 'net2': WebDriverWait(self.driver, timeout).until(lambda driver: len(driver.execute_script('return window.performance.getEntriesByType("resource")')) < 2)
            else: raise ValueError(f"Invalid mode: {wait_mode}")
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [WaitPageLoad]: {e}")
            return False

    def waitElementLoad(self, element, locator, wait_mode='hienthi', timeout=30): # Chờ 1 element
        try:
            condition = self._wait_mode(wait_mode)
            element_locator = (self._locator_type(locator), element)
            WebDriverWait(self.driver, timeout).until(condition(element_locator))
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [waitElementLoad]: {e}"); return False
        
    def waitElementsLoad(self, elements_locators, wait_mode='tontai', timeout=30): # Chờ nhiều element
        """
        Ví dụ:
        elements_locators = {
            'element1': 'xpath',
            'element2': 'css',
            'element3': 'id'
        }
        """
        try:
            end_time = time.time() + timeout
            while time.time() < end_time:
                for selector, format in elements_locators.items():
                    locator_method = self._locator_type(format)
                    condition = self._wait_mode(wait_mode)
                    element_locator = (locator_method, selector)
                    try:
                        element = WebDriverWait(self.driver, timeout).until(condition(element_locator))
                        if element: return element
                    except NoSuchElementException: continue
                    except TimeoutException: continue
            raise TimeoutException("Hết thời gian chờ cho tất cả các element")
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [waitElementsLoad]: {e}"); return None

    def runJs(self, code): # Chạy code js
        try:
            return self.driver.execute_script(code)
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [runJs]: {e}"); return False

    def newTab(self, url): # Mở tab mới
        try:
            self.runJs(f"window.open('{url}', '_blank')"); return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [newTab]: {e}"); return False

    def selectTab(self, index): # Chọn tab
        try:
            self.driver.switch_to.window(self.driver.window_handles[index]); return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [selectTab]: {e}"); return False

    def closeTab(self, index): # Đóng tab
        try:
            self.driver.switch_to.window(self.driver.window_handles[index])
            self.driver.close()
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [closeTab]: {e}"); return False

    def openUrl(self, url, wait_mode=None, timeout=30): # Mở url
        try:
            self.driver.get(url)
            if wait_mode: self.waitPageLoad(wait_mode, timeout)
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [openUrl]: {e}"); return False

    def goBack(self): # Quay lại trang trước
        try:
            self.driver.back(); return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [goBack]: {e}"); return False

    def reload(self): # Tải lại trang
        try:
            self.driver.refresh(); return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [reload]: {e}"); return False
        
    def click(self, element, locator, wait_mode='cotheclick', timeout=30, anti=False): # Click vào 1 element
        try:
            if not self.waitElementLoad(element, locator, wait_mode, timeout): raise Exception("Không tìm thấy element")
            locator_method = self._locator_type(locator)
            element_locator = (locator_method, element)
            web_element = self.driver.find_element(locator_method, element)
            if anti:
                actions = ActionChains(self.driver)
                actions.move_to_element(web_element).click().perform()
            else:
                web_element.click()
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [click]: {e}"); return False

    def sendText(self, element, locator, content, wait_mode='cotheclick', timeout=30, anti=False, write_time_min=0.01, write_time_max=0.3): # Nhập vào 1 element
        try:
            if not self.waitElementLoad(element, locator, wait_mode, timeout):
                raise Exception("Không tìm thấy element")
            locator_method = self._locator_type(locator)
            element_locator = (locator_method, element)
            web_element = self.driver.find_element(locator_method, element)
            if anti:
                actions = ActionChains(self.driver)
                actions.move_to_element(web_element).click().perform()
                for char in content:
                    actions.send_keys(char)
                    actions.pause(random.uniform(write_time_min, write_time_max))
                actions.perform()
            else:
                for char in content:
                    web_element.send_keys(char)
                    time.sleep(random.uniform(write_time_min, write_time_max))
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [type]: {e}"); return False
    
    def selectDropdown(self, element, locator, value, select_mode='value', wait_mode='cotheclick', timeout=30): # Chọn dropdown
        try:
            if not self.waitElementLoad(element, locator, wait_mode, timeout):
                raise Exception("Không tìm thấy dropdown")
            locator_method = self._locator_type(locator)
            dropdown_element = self.driver.find_element(locator_method, element)
            select = Select(dropdown_element)
            if select_mode == 'value': select.select_by_value(str(value))
            elif select_mode == 'index': select.select_by_index(int(value))
            elif select_mode == 'text': select.select_by_visible_text(str(value))
            else: raise ValueError(f"Không có mode: {select_mode}")
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [selectDropdown]: {e}"); return False
    
    def getCookie(self): # Lấy cookie
        try:
            return self.driver.get_cookies()
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [getCookie]: {e}"); return False
            
    def sendKeys(self, keys, element=None, locator=None, wait_mode='cotheclick', timeout=30): # Gửi phím vào một element hoặc trình duyệt
        """
        Ví dụ:
        sendKeys('enter')  # Gửi phím Enter vào trình duyệt
        sendKeys('enter', 'element1', 'xpath')  # Gửi phím Enter vào element có locator là xpath
        """
        try:
            keys_to_send = self._keys_type(keys)
            if keys_to_send is None: raise ValueError(f"Phím không hợp lệ: {keys}")
            if element and locator:
                if not self.waitElementLoad(element, locator, wait_mode, timeout):
                    raise Exception("Không tìm thấy element để gửi phím")
                locator_method = self._locator_type(locator)
                element_locator = (locator_method, element)
                web_element = self.driver.find_element(*element_locator)
                web_element.send_keys(keys_to_send)
            else:
                actions = ActionChains(self.driver)
                actions.send_keys(keys_to_send).perform()
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [sendKeys]: {e}")
            return False

    def exit(self): # Thoát
        try:
            self.driver.quit(); return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [exit]: {e}"); return False

    def screenshot(self): # Chụp ảnh màn hình
        try:
            screenshot_data = self.driver.get_screenshot_as_base64()
            return screenshot_data
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [screenshot_base64]: {e}"); return None
    
    def switchToFrame(self, element, locator, timeout=30): # Chuyển đến frame
        try:
            locator_method = self._locator_type(locator)
            element_locator = (locator_method, element)
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(element_locator)
            )
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [switchToFrame]: {e}"); return False

    def switchToDefault(self): # Chuyển đến nội dung mặc định
        try:
            self.driver.switch_to.default_content(); return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [switchToDefault]: {e}"); return False

    def scroll(self, element=None, locator=None, wait_mode='cotheclick', timeout=30, x=None, y=None, top=False, bottom=False): # Cuộn trang
        try:
            if element and locator:
                if not self.waitElementLoad(element, locator, wait_mode, timeout):
                    raise Exception("Không tìm thấy element để cuộn đến")
                locator_method = self._locator_type(locator)
                element_locator = (locator_method, element)
                web_element = self.driver.find_element(*element_locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", web_element)
            elif top: self.driver.execute_script("window.scrollTo(0, 0);")
            elif bottom: self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elif x is not None or y is not None: self.driver.execute_script(f"window.scrollBy({x or 0}, {y or 0});")
            return True
        except Exception as e:
            if self.DEBUG: print(f"Lỗi [scroll]: {e}"); return False







