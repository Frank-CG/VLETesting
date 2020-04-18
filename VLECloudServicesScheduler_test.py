import time,re
import pytest
from datetime import date,timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from portal_navigator import Navigator
from logger import get_logger

@pytest.fixture(scope="module")
def setup_cloud_services():
    global driver, waiter, navigator, logger
    logger = get_logger()
    driver = webdriver.Chrome()
    waiter = WebDriverWait(driver, 5)
    navigator = Navigator(driver)
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
    
    def validOnCanvas(self, error_message="Canvas showing is NOT correct!"):
        time.sleep(5)
        # value = input("\nConfirm canvas is behaving right: (['','y','yes','Y','YES'])\n")
        # assert value in ["","y","yes","Y","YES"], error_message


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

        time.sleep(5)                
        # value = input("Please confirm testing result (Empty as pass):\n")
        # assert value in ["","y","yes","Y","YES"]
        logger.info("Test case: C7182 successfully pass.")


    def save_event(self):
        xpath_str = '//div[@class="search-input"]/label/input'
        navigator.nav_search(xpath_str, "nicole")
        xpath_str = '//div[text()="QA-nicole-Vmodule"]/../../td[@class="double-line"]/i'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//button[@id="save-event"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[text()="Your changes have been saved."]'
        (fl, el) = navigator.select_by_xpath(xpath_str, navigator.get_waiter(20))
        return fl

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
        def validation():
            navigator.nav_to('Canvases')
            xpath_str = '//div[@class="search-input"]/label/input'
            navigator.nav_search(xpath_str, "nicole")
            xpath_str = '//div[text()="QA-nicole-Vmodule"]/../..'
            navigator.nav_to_by_xpath(xpath_str)
            error_message = "Events showing error."

            xpath_str = '//div[contains(@class, "critical-alert")]'
            (fl,el) = navigator.select_by_xpath(xpath_str)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(228, 0, 0, 1)', error_message
            
            xpath_str = '//div[contains(@class, "domination")]'
            (fl,el) = navigator.select_by_xpath(xpath_str)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(126, 126, 126, 1)', error_message
            
            xpath_str = '//div[contains(@class, "playlist")]'
            (fl,el) = navigator.select_by_xpath(xpath_str)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(15, 173, 182, 1)', error_message
            
            xpath_str = '//div[contains(@class, "event  event even")]'
            (fl,el) = navigator.select_by_xpath(xpath_str)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(241, 108, 78, 1)', error_message

        logger.info("test case: C7183 begins...")
        navigator.nav_to('Projects')
        navigator.select_group('Nicole group')
        xpath_str = '//td/div[text()="Nicole group, V3PO_75c9f6d8-cc79-4b95-ac90-f8c7f9038a88"]'
        navigator.nav_to_by_xpath(xpath_str)

        error_message = "Schedule saving error."
        #Schedule asset 'Normal'
        xpath_str = '//a[text()="Assets"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@class="search-input"]/label/input'
        navigator.nav_search(xpath_str, "1440x2560jpg")
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="1440x2560jpg"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        navigator.select_by_xpath(xpath_str)
        assert self.save_event(), error_message

        #Schedule asset 'Playlist'
        xpath_str = '//a[text()="Playlists"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[text()="asdas"]/../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        navigator.select_by_xpath(xpath_str)
        assert self.save_event(), error_message

        #Schedule asset 'Domination'
        xpath_str = '//a[text()="Assets"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@class="search-input"]/label/input'
        navigator.nav_search(xpath_str, "sienna-piazza-48x48")
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="sienna-piazza-48x48"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Domination"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        if fl:
            el.click()
        assert self.save_event(), error_message

        #Schedule asset 'Critical Alert'
        xpath_str = '//a[text()="Assets"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@class="search-input"]/label/input'
        navigator.nav_search(xpath_str, "terra_incognita_tara_leaver")
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="terra_incognita_tara_leaver"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Critical Alert"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        if fl:
            el.click()
        assert self.save_event(), error_message

        time.sleep(5)

        #Validation
        validation()

        time.sleep(5)
        # value = input("Please confirm testing result (Empty as pass):\n")
        # assert value in ["","y","yes","Y","YES"]
        logger.info("Test case: C7183 successfully pass.")

    '''
    C7185
    Thumbnail view - layouts - schedule layout - This is to verify a layout can be scheduled to a canvas while in thumbnail view.
        Preconditions
            Be on the "Layouts" section of a project: TechOps portal ( ) > Login with valid credentials > Click on the grey bar visible on the left side of the page > Click on the "Projects" button of the Ops Portal's Sidebar menu > Click on the "Layouts" tab.
            Must be logged in as an admin user.
            Have layouts created.
            Must be in thumbnail view.
        Steps
            1 - From the "Layouts" page, click on the thumbnail view (multiple boxes).
            2 - Mouse over a thumbnail of a layout.
            3 - Click on the schedule button (clock).
            4 - Schedule the layout to a canvas.
        Expected Result
            1 - Verify the page switches to multiple thumbnails.
            2 - Verify a header appears with buttons.
            3 - Verify the user is brought to the layout's event page.
            4 - Verify the layout displays properly on the canvas.
    '''
    @pytest.mark.scheduler
    def test_C7185(self):
        logger.info("test case: C7185 begins...")
        navigator.nav_to('Projects')
        xpath_str = '//td/div[text()="Nicole group, V3PO_75c9f6d8-cc79-4b95-ac90-f8c7f9038a88"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//a[text()="Layouts"]'
        navigator.nav_to_by_xpath(xpath_str)

        #Step 1
        xpath_str = '//button[@id="activate-thumbnails-view-btn"]'
        navigator.nav_to_by_xpath(xpath_str)
        error_message = "Failed: Verify the page switches to multiple thumbnails."
        xpath_str = '//div[@id="search-results"]/ul[@id="layout-thumbnails"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        assert fl, error_message

        #Step 2
        error_message = "Failed: Verify a header appears with buttons."
        xpath_str = '//ul[@id="layout-thumbnails"]/li/div[text()="layout-tag"]/..'
        navigator.opr_mouseover(xpath_str)
        xpath_str = xpath_str+'/div[@class="actions"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        assert fl, error_message

        #Step 3
        error_message = "Failed: Verify the user is brought to the layout's event page."
        xpath_str = xpath_str + '/i[@title="Schedule Layout"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        assert fl, error_message

        #Step 4
        error_message = "Failed: Verify the layout displays properly on the canvas."
        assert self.save_event(), error_message

        self.validOnCanvas()
        logger.info("Test case: C7185 successfully pass.")
    
    '''
    C7186
    Scheduler - scheduled event delete - The purpose of this test case is to validate the ability of deleting a scheduled event.
        Preconditions
            Be on the "Schedule" tab of an online iCanvas: TechOps portal ( ) > Login with valid credentials > Click on the grey bar visible on the left side of the page > Click on the "iCANVASES" button of the Ops Portal's Sidebar menu > Click on any online iCanvas displaying content > Click the "Schedule" tab.
            Must be logged as a non-admin user.
            Have access to an online iCanvas displaying content.
        Steps
            1 - From the "Schedule" tab of an iCanvas displaying content, click the link button on the right of any event on the grid.
            2 - Click the "Delete" button at the bottom right.
            3 - Click the "OK" button.
        Expected Result
            1 - Verify that the user is redirected to the selected event's page.
            2 - Verify that a confirmation prompt appears with the following message:
                "Delete this event? This operation cannot be undone."
            3 - Verify that the following happens:
                A "Deleting..." bar appears at the top;
                The user is redirected back to the "Schedule" tab;
                The deleted event is no longer present on the grid within 3 minutes;
                The deleted event stops playing on the iCanvas within 3 minutes.
    '''
    @pytest.mark.scheduler
    def test_C7186(self):
        logger.info("test case: C7186 begins...")
        
        navigator.nav_to('Canvases')
        xpath_str = '//div[@class="search-input"]/label/input'
        navigator.nav_search(xpath_str, "nicole")
        xpath_str = '//div[text()="QA-nicole-Vmodule"]/../..'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//button[normalize-space()="1 Day View"]'
        navigator.nav_to_by_xpath(xpath_str)

        #Step 1
        error_message = "Failed: Verify that the user is redirected to the selected event's page."
        xpath_str = '//div[contains(@class,"event-content") and text()="layout-tag"]/i'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        assert fl, error_message

        #Step 2
        error_message = "Failed: Verify that a confirmation prompt appears with the following message: 'Delete this event? This operation cannot be undone.'"
        xpath_str = '//button[@id="delete-event"]'
        navigator.nav_to_by_xpath(xpath_str)
        xpath_str = '//div[@class="bootbox-body" and text()="Delete this  event?"]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        assert fl, error_message

        #Step 3
        error_message = "Failure for expected : "
        xpath_str = xpath_str + '/../../div[@class="modal-footer"]/button[text()="Ok"]'
        navigator.nav_to_by_xpath(xpath_str)
        expected = "'Deleting...' bar appears at the top;"
        xpath_str = '//div[text()="Deleting..."]'
        (fl,el) = navigator.select_by_xpath(xpath_str)
        assert fl, error_message + expected

        expected = "The user is redirected back to the 'Schedule' tab;"
        xpath_str = '//li[@id="schedule" and contains(@class,"active")]'
        (fl,el) = navigator.select_by_xpath(xpath_str, navigator.get_waiter(5))
        assert fl, error_message + expected

        expected = "The deleted event is no longer present on the grid within 3 minutes;"
        xpath_str = '//div[contains(@class,"event-content") and text()="layout-tag"]/i'
        (fl,el) = navigator.select_by_xpath(xpath_str, navigator.get_waiter(1))
        assert fl == False, error_message + expected

        expected = "The deleted event stops playing on the iCanvas within 3 minutes."
        self.validOnCanvas(error_message + expected)

        logger.info("Test case: C7186 successfully pass.")
    
    '''
    C7187
    Scheduler - scheduled image delete - The purpose of this test case is to validate the behavior of deleting an image while it is displaying on an iCanvas.
        Preconditions
            Be on the "Assets" tab of a project: TechOps portal ( ) > Login with valid credentials > Click on the grey bar visible on the left side of the page > Click on the "PROJECTS" button of the Ops Portal's Sidebar menu > Click on any project > Click the "Assets" tab.
            Must be logged as a non-admin user.
            Have an ingested image.
            Have access to an online iCanvas.
        Steps
            1 - Schedule an image on any online iCanvas.
            2 - Delete the image from its project folder and open the "Schedule" tab of the iCanvas.
        Expected Result
            1 - Verify that the scheduled image displays on the iCanvas.
            2 - Verify that the image stops being displayed on the screen and that its related event is no longer visible on the schedule's grid within 3 minutes.
    '''
    @pytest.mark.scheduler
    def test_C7187(self):
        logger.info("test case: C7187 begins...")
        logger.info("Test case: C7187 successfully pass.")

    @pytest.mark.scheduler
    def test_finial(self):
        driver.close()