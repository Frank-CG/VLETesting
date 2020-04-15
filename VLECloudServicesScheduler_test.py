import time
import pytest
from datetime import date,timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from logger import get_logger

@pytest.fixture(scope="module")
def setup_cloud_services():
    global driver, waiter, logger
    logger = get_logger()
    driver = webdriver.Chrome()
    waiter = WebDriverWait(driver, 5)
    driver.get("https://v-admin-qa.videri.com/icanvases")
    element = waiter.until(EC.presence_of_element_located((By.ID, "loginForm:username")))
    element.send_keys("nicole555")
    element = driver.find_element_by_id("loginForm:password")
    element.send_keys("Videri123QA")
    element = driver.find_element_by_id("loginForm:loginButton")
    element.click()
    element = waiter.until(EC.presence_of_element_located((By.ID, "icanvas-selector")))

@pytest.mark.usefixtures("setup_cloud_services")
class TestVLECloudServicesScheduler:
    
    ''' 
    C7182
    Schedule tab 7 Day view - The purpose of this test case is to validate that an iCanvas' schedule can be viewed in a 1 day & 7 day view
        Preconditions
            Be on the "Schedule" tab of an iCanvas: TechOps portal ( ) > Login with valid credentials > Click on the grey bar visible on the left side of the page > Click on the "iCANVASES" button of the Ops Portal's Sidebar menu > Click any online device displaying content > Click the "Schedule" tab.
            Must be logged in as a non-admin user.
        Steps
            1 - From the "Schedule" tab of an online iCanvas displaying content, click the "7 Day View" button at the top right.
            2 - Click the Previous Day button, composed of a leftward arrow, at left of "Week of 'XXXX-XX-XX'".
            3 - Click the Next Day button, composed of a rightward arrow, at right of "Week of 'XXXX-XX-XX'".
            4 - Click the Previous Week button, composed of two leftward arrows, at left of "Week of 'XXXX-XX-XX'".
            5 - Click the Next Week button, composed of two rightward arrows, at right of "Week of 'XXXX-XX-XX'".
        Expected Result
            1 - Verify that the schedule grid changes to a "7 days" view with the days and dates at the top.
            2 - Verify that the 7 days view goes back from one day and that the events & dates update consequently.
            3 - Verify that the 7 days view advance by one day and that the events & dates update consequently.
            4 - Verify that the schedule from the past 7 days shows and that the dates update consequently.
            5 - Verify that the schedule from the next 7 days shows and that the dates update consequently.
    '''
    @pytest.mark.scheduler
    def test_C7182(self):
        logger.info("test case: C7182 begins...")
        element = driver.find_element_by_css_selector('div.search-input input')
        element.send_keys("nicole")
        element = waiter.until(EC.presence_of_element_located((By.XPATH, "//*[text()='QA-nicole-Vmodule']")))
        element.click()
        element = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.slots > div")))
        #Step 1
        element = waiter.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='7 Day View']")))
        element.click()
        flag = True
        error_message = "(7 Day View) button doesn't work."
        try:
            element = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.days")))
        except (NoSuchElementException,TimeoutException):
            flag = False
            logger.error(error_message)
        assert flag, error_message
        elements = element.find_elements_by_tag_name('div')
        assert len(elements) == 7, error_message
        # elements.sort(key=lambda el: el.text)
        d_today = date.today()
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[0].text == str_today, error_message
        d_today = d_today + timedelta(days=6)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[6].text == str_today, error_message
        time.sleep(2)

        #Step 2
        element = waiter.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Previous Day']")))
        element.click()
        flag = True
        error_message = "(Previous Day) button doesn't work."
        try:
            element = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.days")))
        except (NoSuchElementException,TimeoutException):
            flag = False
            logger.error(error_message)
        assert flag, error_message
        elements = element.find_elements_by_tag_name('div')
        assert len(elements) == 7, error_message
        # elements.sort(key=lambda el: el.text)
        d_today = date.today()
        d_today = d_today + timedelta(days=-1)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[0].text == str_today, error_message
        d_today = d_today + timedelta(days=6)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[6].text == str_today, error_message
        time.sleep(2)

        #Step 3
        element = waiter.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Next Day']")))
        element.click()
        flag = True
        error_message = "(Next Day) button doesn't work."
        try:
            element = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.days")))
        except (NoSuchElementException,TimeoutException):
            flag = False
            logger.error(error_message)
        assert flag, error_message
        elements = element.find_elements_by_tag_name('div')
        assert len(elements) == 7, error_message
        # elements.sort(key=lambda el: el.text)
        d_today = date.today()
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[0].text == str_today, error_message
        d_today = d_today + timedelta(days=6)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[6].text == str_today, error_message
        time.sleep(2)

        #Step 4
        element = waiter.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Previous Week']")))
        element.click()
        flag = True
        error_message = "(Next Day) button doesn't work."
        try:
            element = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.days")))
        except (NoSuchElementException,TimeoutException):
            flag = False
            logger.error(error_message)
        assert flag, error_message
        elements = element.find_elements_by_tag_name('div')
        assert len(elements) == 7, error_message
        # elements.sort(key=lambda el: el.text)
        d_today = date.today()
        d_today = d_today + timedelta(days=-7)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[0].text == str_today, error_message
        d_today = d_today + timedelta(days=6)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[6].text == str_today, error_message
        time.sleep(2)

        #Step 5
        element = waiter.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Next Week']")))
        element.click()
        flag = True
        error_message = "(Next Day) button doesn't work."
        try:
            element = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.days")))
        except (NoSuchElementException,TimeoutException):
            flag = False
            logger.error(error_message)
        assert flag, error_message
        elements = element.find_elements_by_tag_name('div')
        assert len(elements) == 7, error_message
        # elements.sort(key=lambda el: el.text)
        d_today = date.today()
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[0].text == str_today, error_message
        d_today = d_today + timedelta(days=6)
        str_today = d_today.strftime("%a (%m/%d)")
        assert elements[6].text == str_today, error_message
                
        value = input("Please confirm testing result (Empty as pass):\n")
        assert value in ["","y","yes","Y","YES"]

    '''
    C7183
    Schedule legend - The purpose of this test case is to validate that all type of events display according to the legend's colors on the schedule's grid.
        Preconditions
            Be on the "Assets" tab of a project: TechOps portal ( ) > Login with valid credentials > Click on the grey bar visible on the left side of the page > Click on the "PROJECTS" button of the Ops Portal's Sidebar menu > Click any project > Click the "Assets" tab.
            Must be logged in as a non-admin user.
        Steps
            1 - Schedule the following events on an iCanvas and open its "Schedule" tab:
                An asset;
                A Playlist;
                A Domination event;
                A Critical Alert event.
        Expected Result
            1 - Verify that the events show according to the legend's colors on the grid:
                The asset shows in red; (in 1.9/legacy UI it is blue)
                The Playlist shows blue; (in 1.9/legacy UI it is purple)
                The Domination event shows grey; (in 1.9/legacy UI it is yellow)
                The Critical Alert event shows red.
    '''
    @pytest.mark.scheduler
    def test_C7183(self):
        logger.info("test case: C7183 begins...")
    


    '''
    C7185
        Preconditions
        Steps
        Expected Result
    '''
    @pytest.mark.scheduler
    def test_C7185(self):
        logger.info("test case: C7184 begins...")
        
    
    @pytest.mark.scheduler
    def test_finial(self):
        driver.close()