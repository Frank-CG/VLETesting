import time
import pytest
from datetime import date,timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from logger import get_logger

class PortalOperator:
    def __init__(self, driver):
        self.driver = driver
        self.waiter = WebDriverWait(driver, 3)
        self.logger = get_logger()
    
    def get_waiter(self,timeout):
        return WebDriverWait(self.driver, timeout)
        
    def wait_for(self, locator=None, visibable=True, clickable=False, timeout=None):
        if locator is None:
            assert timeout > 0
            time.sleep(timeout)
            return True
        else:
            waiter = WebDriverWait(self.driver, timeout) if (timeout is not None and timeout > 0) else self.waiter
            (fl,el) = self.select(locator, waiter=waiter, visibable=visibable, clickable=clickable)
            return fl


    def wait_for_disapper(self, locator, timeout):
        (fl, el) = self.select(locator)
        temp_count = 0
        while fl:
            time.sleep(0.100)
            temp_count += 1
            if temp_count*0.100 > timeout:
                break
            (fl, el) = self.select(locator)


    def select(self, locator, waiter=None, visibable=True, clickable=False):
        flag = True
        if waiter is None:
            waiter = self.waiter
        try:
            if visibable:
                if clickable:
                    element = waiter.until(EC.element_to_be_clickable(locator))
                else:
                    element = waiter.until(EC.visibility_of_element_located(locator))
            else:
                element = waiter.until(EC.presence_of_element_located(locator))
        except (NoSuchElementException,TimeoutException):
            flag = False
            element = None
        return (flag,element)

    def select_all(self, locator, waiter=None, visibable=True):
        flag = True
        if waiter is None:
            waiter = self.waiter
        try:
            if visibable:
                elements = waiter.until(EC.visibility_of_all_elements_located(locator))
            else:
                elements = waiter.until(EC.presence_of_all_elements_located(locator))
        except (NoSuchElementException,TimeoutException):
            flag = False
            elements = None
        return (flag,elements)
    
    def search(self, locator, keys):
        (fl,el) = self.select(locator)
        if fl:
            el.clear()
            el.send_keys(keys)
            time.sleep(2)
        return fl
    
    def click(self,locator):
        (fl, el) = self.select(locator, clickable=True)
        if fl:
            action = ActionChains(self.driver)
            action.move_to_element(el).click().perform()
            time.sleep(2)
        return fl
    
    def click_and_check(self, locator, check_locator):
        (fl, el) = self.select(locator, clickable=True)
        if fl:
            action = ActionChains(self.driver)
            action.move_to_element(el).click().perform()
            (fl2, el2) = self.select(check_locator)
            time.sleep(1)
        return fl and fl2
    
    def mouseover(self, locator):
        (fl, el) = self.select(locator, clickable=True)
        if fl:
            action = ActionChains(self.driver)
            action.move_to_element(el).perform()
            time.sleep(2)
        return fl
    
    def nav_to_toptab(self, top_tab_name):
        xpath_str = '//a/label[text()="'+top_tab_name+'"]/..'
        locator = (By.XPATH, xpath_str)
        return self.click(locator)

    def nav_to_group(self, group_name):
        xpath_str = '//ul[@class="jstree-container-ul jstree-children"]/li[contains(@class,"jstree-closed")]/i'
        locator = (By.XPATH, xpath_str)
        self.click(locator)
        xpath_str = '//a[text()="'+group_name+'"]'
        locator = (By.XPATH, xpath_str)
        return self.click(locator)
    
    def drag_and_drop_file(self, path):
        JS_DROP_FILE = """
            var target = arguments[0],
                offsetX = arguments[1],
                offsetY = arguments[2],
                document = target.ownerDocument || document,
                window = document.defaultView || window;

            var input = document.createElement('INPUT');
            input.type = 'file';
            input.onchange = function () {
            var rect = target.getBoundingClientRect(),
                x = rect.left + (offsetX || (rect.width >> 1)),
                y = rect.top + (offsetY || (rect.height >> 1)),
                dataTransfer = { files: this.files };

            ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                var evt = document.createEvent('MouseEvent');
                evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
            });

            setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
        """
        locator = (By.XPATH, '//div[@id="file-drop-target"]') 
        (fl, drop_target) = self.select(locator)
        if fl:
            driver = drop_target.parent
            file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
            file_input.send_keys(path)