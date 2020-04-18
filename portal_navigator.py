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

class Navigator:
    def __init__(self, driver):
        self.driver = driver
        self.waiter = WebDriverWait(driver, 3)
        self.logger = get_logger()
    
    def get_waiter(self,timeout):
        return WebDriverWait(self.driver, timeout)
    
    def select_by_xpath(self, xpath_str, waiter=None, clickable=False):
        flag = True
        if waiter is None:
            waiter = self.waiter
        try:
            if clickable:
                element = waiter.until(EC.element_to_be_clickable((By.XPATH, xpath_str)))
            else:
                element = waiter.until(EC.visibility_of_element_located((By.XPATH, xpath_str)))
        except (NoSuchElementException,TimeoutException):
            flag = False
            element = None
            self.logger.error("XPATH not found: " + xpath_str)
        return (flag,element)
    
    def select_group(self, group_name):
        xpath_str = '//ul/li//i[@class="jstree-icon jstree-ocl"]'
        self.nav_to_by_xpath(xpath_str)
        xpath_str = '//a[text()="'+group_name+'"]'
        return self.nav_to_by_xpath(xpath_str)
    
    def nav_to(self, tab_name):
        xpath_str = '//a/label[text()="'+tab_name+'"]/..'
        return self.nav_to_by_xpath(xpath_str)
    
    def nav_to_by_xpath(self, xpath_str):
        (fl, el) = self.select_by_xpath(xpath_str, waiter=self.waiter, clickable=True)
        if fl:
            action = ActionChains(self.driver)
            action.move_to_element(el).click().perform()
            time.sleep(1)
        return fl
    
    def nav_search(self, xpath_str, search_keys):
        (fl,el) = self.select_by_xpath(xpath_str)
        flag = True
        if fl:
            el.clear()
            el.send_keys(search_keys)
            time.sleep(2)
            # waiter = self.get_waiter(10)
            # xpath_str = '//*[@id="search-results"]/table/tbody/tr'
            # try:
            #     elements = waiter.until(EC.visibility_of_all_elements_located((By.XPATH, xpath_str)))
            # except (NoSuchElementException,TimeoutException):
            #     flag = False
            #     elements = None
            #     self.logger.error("XPATH not found: " + xpath_str)
            # if flag:
            #     flag = len(elements) > 0
        return fl and flag
    
    def opr_mouseover(self,xpath_str):
        (fl, el) = self.select_by_xpath(xpath_str, waiter=self.waiter, clickable=True)
        if fl:
            action = ActionChains(self.driver)
            action.move_to_element(el).perform()

