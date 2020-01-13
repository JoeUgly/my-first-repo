


import scrapy, datetime
from scrapy.crawler import CrawlerProcess



startTime = datetime.datetime.now()




class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.johnstownschools.org/job-openings/']

    def parse(self, response):

        outputResponse['text'] = response.css('::text').getall()




process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


outputResponse = {}


process.crawl(BrickSetSpider)
process.start()



ooo = outputResponse["text"]


for i in ooo:

    i = i.strip()

    if i: print(i)





print(datetime.datetime.now() - startTime)








