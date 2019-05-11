import scrapy
from pyquery import PyQuery
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse1)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse1(self, response):
        pq = PyQuery(response.body)
        quotes = pq(".quote")
        for quote in quotes.items():
            item = QuoteItem()
            item['text'] = quote('.text').text()
            item['author'] = quote('.author').text()
            item['tags'] = [tag.text() for tag in quote('.tag').items()]
            yield item
        
        next_page = pq('.next a').attr('href')
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback = self.parse1)
            yield response.follow(next_page, callback = self.parse1)