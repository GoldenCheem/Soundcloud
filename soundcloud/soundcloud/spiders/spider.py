import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["soundcloud.com"]
    start_urls = ["https://soundcloud.com/search/sounds?q=jazz"]

    def parse(self, response):
        pass
