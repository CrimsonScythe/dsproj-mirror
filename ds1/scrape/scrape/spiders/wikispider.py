group_nr=16
alph = "ABCDEFGHIJKLMNOPRSTUVWZABCDEFGHIJKLMNOPRSTUVWZ"[group_nr%23:group_nr%23+10]
import scrapy
import re

class Spider(scrapy.Spider):
    
    name = "wiki"

    def start_requests(self):
        urls = [
            'https://en.wikinews.org/wiki/Category:Politics_and_conflicts',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # va=response.css('a::attr(href)').get()
        va=response.css('tbody')
        vaa=va.css('td')

        # regexp = re.compile(r'>[R|S|T|U|V|W|Z|A|B|C]<')
        regexp=re.compile(r'from=[R|S|T|U|V|W|Z|A|B|C]')
        vaaa = vaa.css('a::attr(href)').getall()
        for l in vaaa:
            if regexp.search(l):
                print(l)
            # print(l)

        # vaaa = vaa.css('a::attr(href)').getall()
        # for l in vaaa:
        #     print(l)
        