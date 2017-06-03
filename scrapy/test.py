import scrapy
from scrapy.crawler import CrawlerProcess
#import logging

# # logging.basicConfig(filename='record.log')
# # logger = logging.getLogger(__name__)

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/tag/humor/',
#     ]

#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').extract_first(),
#                 'author': quote.xpath('span/small/text()').extract_first(),
#             }

#         next_page = response.css('li.next a::attr("href")').extract_first()
#         # logger.info("hello world")
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['ebay.com']
    start_urls = ['https://www.i-traffic.co.za/traffic/time_speed.aspx']
    # start_urls = ['http://www.ebay.com/sch/i.html?_odkw=books&_osacat=0&_trksid=p2045573.m570.l1313.TR0.TRC0.Xpython&_nkw=python&_sacat=0&_from=R40']

    def parse(self, response):
        # self.driver.get(response.url)
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get(response.url)
        
        kaka = []
        # scrape 10 pages
        for i in range(10):
            # click 'next' button to get data from next page
            next = driver.find_elements_by_xpath('//td[@class="listPagerCell"]/a')[-1]
            next.click()
            try:
                # record the datas
                time.sleep(3)
                for i in range(2,12):
                    info = driver.find_elements_by_xpath('//table[@class="listGridView"]//tr')[i]
                    soup = BeautifulSoup(info.get_attribute('innerHTML'), 'lxml')
                    data = []
                    for item in soup.find_all('span'):
                        data += [item.get_text()]
                    yield {
                        'Roadway': data[0],
                        'Direction': data[1],
                        'Segment': data[2],
                        'Length': data[3],
                        'Travel Time': data[4],
                        'Avg Speed': data[5]
                    }

            except:
                break

        driver.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_URI': 'export.json'
})
process.crawl(ProductSpider)
process.start() # the script will block here until the crawling is finished