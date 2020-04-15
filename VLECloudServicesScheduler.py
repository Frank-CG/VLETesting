import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class VLECloudServicesScheduler(unittest.TestCase):

    def setUp(self):
        driver = webdriver.Chrome()
        self.driver = driver
        wait = WebDriverWait(self.driver, 5)
        self.wait = wait
        driver.get("https://v-admin-qa.videri.com/icanvases")
        element = wait.until(EC.presence_of_element_located((By.ID, "loginForm:username")))
        element.send_keys("nicole555")
        element = driver.find_element_by_id("loginForm:password")
        element.send_keys("Videri123QA")
        element = driver.find_element_by_id("loginForm:loginButton")
        element.click()
        element = wait.until(EC.presence_of_element_located((By.ID, "icanvas-selector")))

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
    def test_C7182(self):
        driver = self.driver
        wait = self.wait
        element = driver.find_element_by_css_selector('div.search-input input')
        element.send_keys("nicole")
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='QA-nicole-Vmodule']")))
        element.click()
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.slots > div")))
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='7 Day View']")))
        element.click()
        try:
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.days")))
        except (NoSuchElementException,TimeoutException):
            print("(7 Day View) button doesn't work.")
        value = input("Please enter a string:\n")
        print(f'You entered {value}')
        assert value == "Y"
    

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()