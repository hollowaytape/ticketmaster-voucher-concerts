from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

url = r"http://concerts.livenation.com/microsite/settlement#colMainWra"

def init_driver():
    """Create Firefox profile and start the webdriver."""
    # Gotta change some firefox settings - otherwise it opens a "firstrun" page instead of iceqube
    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.startup.homepage_override.mstone', 'ignore')
    fp.set_preference('browser.startup.homepage', 'about:blank')
    fp.set_preference('startup.homepage_welcome_url', 'about:blank')
    fp.set_preference('startup.homepage_welcome_url.additional', 'about:blank')

    driver = webdriver.Firefox(firefox_profile=fp)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def scrape_concerts(driver):
    driver.get(url)
    try:
        full_table = driver.wait.until(expected_conditions.presence_of_element_located(
            (By.ID, 'result_national')))
        #button = driver.wait.until(expected_conditions.element_to_be_clickable(
        #    (By.NAME, 'Pin')))
        print full_table
        #button.click()
        #for i in WebElement.find_elements_by_class_name(full_table, 'month'):
        for i in WebElement.find_elements_by_css_selector(full_table, 'tr'):
            try:
                month = WebElement.find_element_by_css_selector(i, 'abbr').get_attribute('title')
                day = WebElement.find_element_by_css_selector(i, 'div.date').text
            except NoSuchElementException:
                month = '?'
                day = "?"

            performer = WebElement.find_element_by_css_selector(i, 'a.event').text
            venue, city, time = WebElement.find_element_by_css_selector(i, 'td.venue').text.split('\n')

            # whoops, they're all showing up as "Voucher Sold Out for this Event" now.
            # they probably didn't want robots crawling the site! whoops, too late for that now.

            print month, day, performer, venue, city, time
    except TimeoutException:
        print "Box or Button not found in iceqube page"

def next_page(driver):
    try:
        button = driver.wait.until(expected_conditions.presence_of_element_located(
        (By.CLASS_NAME, 'next')))
        button.click()
        return True
    except TimeoutException:
        print "No more pages remain"
        return False

if __name__ == '__main__':
    driver = init_driver()
    scrape_concerts(driver)

    while next_page(driver):
        scrape_concerts(driver)

    WebDriverWait(10, driver)
    driver.close() # close the window
