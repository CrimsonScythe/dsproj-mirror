group_nr=16
alph = "ABCDEFGHIJKLMNOPRSTUVWZABCDEFGHIJKLMNOPRSTUVWZ"[group_nr%23:group_nr%23+10]
import scrapy
import re
import sys
from datetime import datetime

class Spider(scrapy.Spider):
    
    name = "rwiki"

    def start_requests(self):
        urls = [
            'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=A',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=B',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=C',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=R',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=S',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=T',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=U',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=V',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=W',
            # 'https://en.wikinews.org/w/index.php?title=Category:Politics_and_conflicts&from=Z'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    # FROM HERE (MORE EXAMPLES AND PATTERNS)
    # https://doc.scrapy.org/en/latest/intro/tutorial.html#following-links

    def parse(self, response):
        # if letter in alph
        # letter = response.xpath('//div[@class="mw-category-generated"]').xpath('child::div[2]').xpath('descendant::h3/text()').get()
        if (True):

            # print(letter)
            # print("WORKING")
     
            # we are down to the A list"
            pages=response.xpath('//div[@class="mw-category-generated"]').xpath('child::div[2]').xpath('child::div').xpath('child::div').xpath('child::div').xpath('child::ul')
            # specifying the a follow automatically extracts the link
            anchors = pages.css('li a')
            # follows all links on the current page
            # the callback here is different because we want to defer extraction of data to a different function
            yield from response.follow_all(anchors, callback=self.parse_single)
            # yield response.follow(anchors[0], callback=self.parse_single)
            # from is required if we follow_all
            # nextPages = response.xpath('//div[@class="mw-category-generated"]').xpath('child::div[2]').xpath('child::*[self::text()[contains(.,"next page")]]')
            
        nextPages = response.xpath('//div[@class="mw-category-generated"]').xpath('child::div[2]').xpath('descendant::a[contains(.,"next page")]/@href').get()
        if (not(nextPages is None)):
            yield response.follow(nextPages, callback=self.parse)
        # else:
            # sys.exit()    

    def parse_single(self, response):
        title=response.xpath('//div[@id="content"]').xpath('child::h1[@id="firstHeading"]/text()').get()
        if (title[0] in alph):
       
            yield{
                #  extract text from h1 attribute
                'title' : response.xpath('//div[@id="content"]').xpath('child::h1[@id="firstHeading"]/text()').get(),
                'date' : response.xpath('//div[@id="content"]//strong[@class="published"]//span/@title').get(),
                'content' :  response.xpath('//div[@id="content"]//div[@id="mw-content-text"]//child::text()[not(ancestor::h2) and not(ancestor::div/@class="infobox noprint desktop-only") and not(ancestor::span/@class="sourceTemplate") and not(ancestor::a/@class="external text") and not(ancestor::table/@id="social_bookmarks") and not(ancestor::div/@id="commentrequest") and not(ancestor::div/@class="thumbcaption")]').getall(),
                'url' : response.url,
                'domain' : re.search("https?://([A-Za-z_0-9.-]+).*", response.url).group(1),
                'scraped_at' : datetime.now(),
                'type' : 'reliable'
            }

        # head=response.xpath('//div[@id="content"]').xpath('child::h1[@id="firstHeading"]/text()').get()
        # print(head)

        # alfredHitch = response.xpath('//div[@id="content"]//strong[@class="published"]//span/@title').get()
        # print(alfredHitch)

        # for the content we need to look for <p> and <ul> tags. We stop when we see a <center> tag 
        # the // command finds children
        # var = response.xpath('//div[@id="content"]//div[@id="mw-content-text"]//p//text()').getall()
        # below excludes the related articles box
        # var = response.xpath('//div[@id="content"]//div[@id="mw-content-text"]//child::text()[not(ancestor::div/@class="infobox noprint desktop-only")]').getall()
        # below excludes headings
        # var = response.xpath('//div[@id="content"]//div[@id="mw-content-text"]//child::text()[not(ancestor::h2)]').getall()
        # below remove Sources points
        # var = response.xpath('//div[@id="content"]//div[@id="mw-content-text"]//child::text()[not(ancestor::span/@class="sourceTemplate")]').getall()

        # below combining both
        # below works and in PROD
        # var = response.xpath('//div[@id="content"]//div[@id="mw-content-text"]//child::text()[not(ancestor::h2) and not(ancestor::div/@class="infobox noprint desktop-only") and not(ancestor::span/@class="sourceTemplate") and not(ancestor::a/@class="external text") and not(ancestor::table/@id="social_bookmarks") and not(ancestor::div/@id="commentrequest")]').getall()
        # var = re.search("https?://([A-Za-z_0-9.-]+).*", response.url)
        # remove thumb caption below
        # and not(ancestor::div/@class="thumbcaption")]')

        

        # print(var)


# scrapy crawl rwiki -o rwiki.csv