import scrapy
from scrapy_selenium import SeleniumRequest
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SpiderSpider(scrapy.Spider):
    name = "spider"

    def start_requests(self):
        url = "https://soundcloud.com/search/sounds?q=jazz"
        yield SeleniumRequest(url=url,
                              callback=self.parse,
                              wait_time=10,
                              wait_until=EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')),
                              script="document.getElementById('onetrust-accept-btn-handler').click()")

    def parse(self, response):
        time.sleep(5)
        # Get driver
        driver = response.request.meta["driver"]

        # Maximize window's size
        driver.maximize_window()

        # Scroll the windows 37 times, 500 pixels for each time
        time.sleep(5)
        for x in range(0, 37):
            ActionChains(driver) \
                .scroll_by_amount(0, 500) \
                .perform()
            time.sleep(1)
        time.sleep(5)

        for track in driver.find_elements(By.CSS_SELECTOR, 'li.searchList__item.sc-mt-3x'):
            # Get track name
            try:
                name = track.find_element(By.CSS_SELECTOR,
                                          'a.sc-link-primary.soundTitle__title.sc-link-dark.sc-text-h4').text.strip()
            except:
                name = 'None'
            
            # Get poster name
            try:
                poster = track.find_element(By.CSS_SELECTOR,
                                            '.soundTitle__usernameText').text.strip()
            except:
                poster = 'None'

            # Get number of plays and comments
            plays_comments = track.find_elements(By.CSS_SELECTOR, '.sc-ministats-item')
            
            try:
                plays = plays_comments[0].get_attribute('title')
            except:
                plays = 0

            try:
                comments = plays_comments[1].get_attribute('title')
            except:
                comments = 0

            # Get number of likes
            try:
                likes = track.find_element(By.CSS_SELECTOR, 
                                           '.sc-button-like.sc-button-secondary.sc-button.sc-button-small.sc-button-responsive'
                                          ).text.strip()
            except:
                likes = 0
            
            # Get number of reposts
            try:
                reposts = track.find_element(By.CSS_SELECTOR,
                                             '.sc-button-repost.sc-button-secondary.sc-button.sc-button-small.sc-button-responsive'
                                            ).text.strip()
            except:
                reposts = 0

            # Get posted time
            try:
                posted_time = track.find_element(By.CSS_SELECTOR,
                                                 '.relativeTime.sc-text-secondary.sc-text-captions'
                                                ).get_attribute('title')
            except:
                posted_time = 'None'
            
            # Get tag name
            try:
                tag = track.find_element(By.CSS_SELECTOR, 'a.sc-tag.soundTitle__tag.sc-tag-small').text
            except:
                tag = 'None'

            # Return the item
            yield {
                'name': name,
                'poster': poster,
                'plays': plays,
                'comments': comments,
                'likes': likes,
                'reposts': reposts,
                'posted_time': posted_time,
                'tag': tag
            }

        time.sleep(5)

