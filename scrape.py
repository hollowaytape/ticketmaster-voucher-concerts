import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from pymongo import MongoClient

class Concert:
    def __init__(self, name, venue, city, date):
        self.name = name
        self.venue = venue
        self.city = city
        self.date = date

url = r"http://concerts.livenation.com/microsite/settlement#colMainWra"

months = {'January': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
          'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


client = MongoClient()
db = client.test

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


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

        for i in WebElement.find_elements_by_css_selector(full_table, 'tr'):
            try:
                month = months[WebElement.find_element_by_css_selector(i, 'abbr').get_attribute('title')]
                day = int(WebElement.find_element_by_css_selector(i, 'div.date').text)
            except NoSuchElementException:
                # There's a Counting Crowes concert that doesn't have a date yet, so skip it
                continue

            name = WebElement.find_element_by_css_selector(i, 'a.event').text
            venue, city, time = WebElement.find_element_by_css_selector(i, 'td.venue').text.split('\n')
            time = datetime.strptime(time, "%I:%M %p")

            # whoops, they're all showing up as "Voucher Sold Out for this Event" now.
            # they probably didn't want robots crawling the site! whoops, too late for that now.

            date = datetime(datetime.now().year, month, day, time.hour, time.minute)

            concert = Concert(name, venue, city, date)
            j = json.dumps(concert.__dict__, default=date_handler)
            result = db.concerts.insert_one(concert.__dict__)

            print result.inserted_id
            
    except TimeoutException:
        print "Something went wrong, the page didn't quite load"

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
