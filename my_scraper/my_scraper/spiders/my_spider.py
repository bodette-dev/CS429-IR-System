import scrapy
from scrapy.exceptions import CloseSpider
from my_scraper.items import MyScraperItem

class MySpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["www.iit.edu"]
    start_urls = ["https://www.iit.edu"]
    depth_limit = 5
    page_limit = 10
    page_count = 0

    def parse(self, response):
        # Increment page count
        self.page_count += 1
        
        # Close spider if page limit is reached
        if self.page_count > self.page_limit:
            raise CloseSpider("CloseSpider: Page Limit Reached")
        
        # Create instance of MyScraperItem
        scraper = MyScraperItem()
        
        # Extract information
        scraper["page_url"] = response.url
        scraper["main_content"] = response.xpath('//body').get()
        yield scraper
        
        # Go to next links if applicable
        next_links = response.css("a::attr(href)").getall()
        for next_link in next_links:
            if next_link:
                yield response.follow(next_link, self.parse)
