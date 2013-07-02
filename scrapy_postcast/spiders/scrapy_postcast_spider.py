from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from scrapy_postcast.items import ScrapyPostcastItem
from scrapy.http import Request
import nltk
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class ScrapyPostcastSpider(BaseSpider):
    name = 'scrapy_postcast'
    allowed_domains = ["scientificamerican.com"]
    start_urls = [
            "http://www.scientificamerican.com/podcast/podcasts.cfm?type=60-second-science"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        list = hxs.select('//*[@class="hasThumb message_box"]')
        items = []
        for li in list:
            item = ScrapyPostcastItem()
            item['_id'] = li.select('h3/a/text()').extract()[0]
            item['url'] = li.select('h3/a/@href').extract()
            item['desc'] = li.select('p/text()').extract()
            for url in item['url']:
                request =  Request(url, callback=self.get_content)
                request.meta['item'] = item
                yield request
            break

    def get_content(self, response):
        item = response.meta['item']
        hxs = HtmlXPathSelector(response)
        article = hxs.select('//*[@id="articleContent"]')
        mp3links = hxs.select('//*[@id="mp3Link"]/@href').extract()
        for art in article:
            prographs = art.select('p')
            raw = []
            for p in prographs:
                raw.append(nltk.clean_html(p.extract()))
            item['text'] = raw
        #yield item
        for link in mp3links:
            request = Request(link, callback=self.get_podcast)
            request.meta['item'] = item
            yield request

    def get_podcast(self, response):
        item = response.meta['item']
        item['podcast'] = response.body
        with open('postcast.mp3', 'wb+') as f:
            f.write(response.body)
        yield item
