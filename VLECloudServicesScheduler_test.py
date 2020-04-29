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
from portal_operator import PortalOperator
from logger import get_logger
from constant import RESOURCE_DIR

@pytest.fixture(scope="module")
def setup_cloud_services():
    global driver, waiter, navigator, operator, logger
    global images
    images = [RESOURCE_DIR+"images/test-img-01.jpeg",RESOURCE_DIR+"images/test-img-02.jpeg",RESOURCE_DIR+"images/test-img-03.jpeg"]
    logger = get_logger()
    driver = webdriver.Chrome()
    waiter = WebDriverWait(driver, 5)
    operator = PortalOperator(driver)
    driver.get("https://v-admin-qa.videri.com/icanvases")
    element = waiter.until(EC.presence_of_element_located((By.ID, "loginForm:username")))
    element.send_keys("nicole555")
    element = driver.find_element_by_id("loginForm:password")
    element.send_keys("Videri123QA")
    element = driver.find_element_by_id("loginForm:loginButton")
    element.click()
    locator = (By.ID, "icanvas-selector")
    operator.wait_for(locator)
    

@pytest.mark.usefixtures("setup_cloud_services")
class TestVLECloudServicesScheduler:
    
    def validOnCanvas(self, error_message="Canvas showing is NOT correct!"):
        time.sleep(10)
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
        locator = (By.CSS_SELECTOR, 'div.search-input input')
        operator.search(locator, "DPC-460TW1-180310016001")
        locator = (By.XPATH, "//*[text()='DPC-460TW1-180310016001']")
        operator.click(locator)
        locator = (By.CSS_SELECTOR, "div.slots > div")
        operator.wait_for(locator)

        def valid(days_elements, offset):
            elements = days_elements.find_elements_by_tag_name('div')
            assert len(elements) == 7, error_message
            d_today = date.today()
            d_today = d_today + timedelta(days=offset)
            str_today = d_today.strftime("%a (%m/%d)")
            assert elements[0].text == str_today, error_message
            d_today = d_today + timedelta(days=6)
            str_today = d_today.strftime("%a (%m/%d)")
            assert elements[6].text == str_today, error_message
            operator.wait_for(timeout=1)
        
        def step_check(error_message, locator, offset):
            operator.click(locator)        
            locator = (By.CSS_SELECTOR, "div.days")
            (fl, el) = operator.select(locator)
            assert fl, error_message
            valid(el, offset)

        #Step 1
        error_message = "(7 Day View) button doesn't work."
        locator = (By.XPATH, "//button[normalize-space()='7 Day View']")
        step_check(error_message, locator, 0)

        #Step 2
        error_message = "(Previous Day) button doesn't work."
        locator = (By.XPATH, "//button[@title='Previous Day']")
        step_check(error_message, locator, -1)

        #Step 3
        error_message = "(Next Day) button doesn't work."
        locator = (By.XPATH, "//button[@title='Next Day']")
        step_check(error_message, locator, 0)

        #Step 4
        error_message = "(Previous Week) button doesn't work."
        locator = (By.XPATH, "//button[@title='Previous Week']")
        step_check(error_message, locator, -7)

        #Step 5
        error_message = "(Next Week) button doesn't work."
        locator = (By.XPATH, "//button[@title='Next Week']")
        step_check(error_message, locator, 0)

        operator.wait_for(timeout=5)
        logger.info("Test case: C7182 successfully pass.")


    def save_event(self):
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "DPC-460TW1-180310016001")
        xpath_str = '//div[text()="DPC-460TW1-180310016001"]/../../td[@class="double-line"]/i'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//button[@id="save-event"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[text()="Your changes have been saved."]'
        locator = (By.XPATH, xpath_str)
        (fl, el) = operator.select(locator, waiter=operator.get_waiter(20))
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
            operator.nav_to_toptab('Canvases')
            xpath_str = '//div[@class="search-input"]/label/input'
            locator = (By.XPATH, xpath_str)
            operator.search(locator, "DPC-460TW1-180310016001")
            xpath_str = '//div[text()="DPC-460TW1-180310016001"]/../..'
            locator = (By.XPATH, xpath_str)
            operator.click(locator)
            error_message = "Events showing error."

            xpath_str = '//div[contains(@class, "critical-alert")]'
            locator = (By.XPATH, xpath_str)
            (fl,el) = operator.select(locator)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(228, 0, 0, 1)', error_message
            
            xpath_str = '//div[contains(@class, "domination")]'
            locator = (By.XPATH, xpath_str)
            (fl,el) = operator.select(locator)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(126, 126, 126, 1)', error_message
            
            xpath_str = '//div[contains(@class, "playlist")]'
            locator = (By.XPATH, xpath_str)
            (fl,el) = operator.select(locator)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(15, 173, 182, 1)', error_message
            
            xpath_str = '//div[contains(@class, "event  event even")]'
            locator = (By.XPATH, xpath_str)
            (fl,el) = operator.select(locator)
            assert fl,error_message
            rgba = el.value_of_css_property('background-color')
            assert rgba == 'rgba(241, 108, 78, 1)', error_message

        logger.info("test case: C7183 begins...")
        operator.nav_to_toptab('Projects')
        operator.nav_to_group('Nicole group')
        xpath_str = '//td/div[text()="Nicole group, V3PO_75c9f6d8-cc79-4b95-ac90-f8c7f9038a88"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)

        error_message = "Schedule saving error."
        #Schedule asset 'Normal'
        xpath_str = '//a[text()="Assets"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "1440x2560jpg")
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="1440x2560jpg"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        locator = (By.XPATH, xpath_str)
        operator.wait_for(locator)
        assert self.save_event(), error_message

        #Schedule asset 'Playlist'
        xpath_str = '//a[text()="Playlists"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[text()="asdas"]/../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        locator = (By.XPATH, xpath_str)
        operator.wait_for(locator)
        assert self.save_event(), error_message

        #Schedule asset 'Domination'
        xpath_str = '//a[text()="Assets"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "sienna-piazza-48x48")
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="sienna-piazza-48x48"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Domination"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
        if fl:
            el.click()
        assert self.save_event(), error_message

        #Schedule asset 'Critical Alert'
        xpath_str = '//a[text()="Assets"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "terra_incognita_tara_leaver")
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="terra_incognita_tara_leaver"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Critical Alert"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
        if fl:
            el.click()
        assert self.save_event(), error_message
        operator.wait_for(timeout=5)

        #Validation
        validation()
        operator.wait_for(timeout=5)

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
        operator.nav_to_toptab('Projects')
        xpath_str = '//td/div[text()="Nicole group, V3PO_75c9f6d8-cc79-4b95-ac90-f8c7f9038a88"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//a[text()="Layouts"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)

        #Step 1
        xpath_str = '//button[@id="activate-thumbnails-view-btn"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        error_message = "Failed: Verify the page switches to multiple thumbnails."
        xpath_str = '//div[@id="search-results"]/ul[@id="layout-thumbnails"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
        assert fl, error_message

        #Step 2
        error_message = "Failed: Verify a header appears with buttons."
        xpath_str = '//ul[@id="layout-thumbnails"]/li/div[text()="layout-tag"]/..'
        locator = (By.XPATH, xpath_str)
        operator.mouseover(locator)
        xpath_str = xpath_str+'/div[@class="actions"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
        assert fl, error_message

        #Step 3
        error_message = "Failed: Verify the user is brought to the layout's event page."
        xpath_str = xpath_str + '/i[@title="Schedule Layout"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
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
        
        operator.nav_to_toptab('Canvases')
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "DPC-460TW1-180310016001")
        xpath_str = '//div[text()="DPC-460TW1-180310016001"]/../..'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//button[normalize-space()="1 Day View"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)

        #Step 1 //div[@class="explicit_slot"]/div[@class="slot"]
        error_message = "Failed: Verify that the user is redirected to the selected event's page."
        xpath_str = '//div[contains(@class,"event-content")]/i'
        locator = (By.XPATH, xpath_str)
        (fl, els) = operator.select_all(locator)
        assert fl and len(els) > 0
        els[0].click()
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
        assert fl, error_message

        #Step 2
        error_message = "Failed: Verify that a confirmation prompt appears with the following message: 'Delete this event? This operation cannot be undone.'"
        xpath_str = '//button[@id="delete-event"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="bootbox-body" and text()="Delete this  event?"]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator)
        assert fl, error_message

        #Step 3
        error_message = "Failure for expected : "
        expected = "'Deleting...' bar appears at the top;"
        xpath_str = xpath_str + '/../../div[@class="modal-footer"]/button[text()="Ok"]'
        locator = (By.XPATH, xpath_str)
        check_locator = (By.XPATH, '//div[text()="Deleting..."]')
        fl = operator.click_and_check(locator, check_locator)
        assert fl, error_message + expected

        expected = "The user is redirected back to the 'Schedule' tab;"
        xpath_str = '//li[@id="schedule" and contains(@class,"active")]'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator, operator.get_waiter(5))
        assert fl, error_message + expected

        expected = "The deleted event is no longer present on the grid within 3 minutes;"
        xpath_str = '//div[contains(@class,"event-content") and text()="layout-tag"]/i'
        locator = (By.XPATH, xpath_str)
        (fl,el) = operator.select(locator, operator.get_waiter(1))
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
    @pytest.mark.scheduler_cur
    def test_C7187(self):
        logger.info("test case: C7187 begins...")
        image_full_path = images[0]
        image_file_name = 'test-img-01'

        operator.nav_to_group('Nicole group')

        operator.nav_to_toptab('Projects')        
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "nicole-group-at")
        xpath_str = '//div[text()="nicole-group-at"]/../..'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        operator.drag_and_drop_file(image_full_path)
        xpath_str = '//span[text()="Upload"]/..'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="'+image_file_name+'"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Delete"]'
        assert operator.wait_for((By.XPATH, xpath_str), 10)

        #Step 1 - Schedule an image on any online iCanvas.
        error_message = "Schedule saving error."
        xpath_str = '//a[text()="Assets"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, image_file_name)
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="'+image_file_name+'"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Schedule"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@id="priority-container"]//select/option[@value="Normal"]'
        locator = (By.XPATH, xpath_str)
        operator.wait_for(locator)
        assert self.save_event(), error_message

        error_message = "Failure for expected : 1 - Verify that the scheduled image displays on the iCanvas."
        self.validOnCanvas(error_message)

        #Step 2 - Delete the image from its project folder and open the "Schedule" tab of the iCanvas.
        operator.nav_to_toptab('Projects')        
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, "nicole-group-at")
        xpath_str = '//div[text()="nicole-group-at"]/../..'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//a[text()="Assets"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="search-input"]/label/input'
        locator = (By.XPATH, xpath_str)
        operator.search(locator, image_file_name)
        xpath_str = '//table[@id="asset-selector"]/tbody/tr/td/div/span[@class="asset-name" and text()="'+image_file_name+'"]/../../../td[@class="list-action left-col"]/div/div/i[@title="Delete"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)
        xpath_str = '//div[@class="modal-footer"]/button[text()="Ok"]'
        locator = (By.XPATH, xpath_str)
        operator.click(locator)

        error_message = "Failure for expected : Verify that the image stops being displayed on the screen and that its related event is no longer visible on the schedule's grid within 3 minutes."
        self.validOnCanvas()
        

        logger.info("Test case: C7187 successfully pass.")

    @pytest.mark.scheduler_cur
    def test_finial(self):
        driver.close()