from hotel import tasks

from lxml import etree
import requests


class CrawlerManager:
    domain  = 'https://www.booking.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}


    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.__next_url = True
        self.nextPageXpath = "//a[@title='下一頁']/@href"
        self.hotelPageXpath = "//a[@class='js-sr-hotel-link hotel_name_link url']/@href"

    
    def crawl(self, url):
        response = requests.get(url, headers = self.headers).text
        selector = etree.HTML(response)
        return selector

    
    def crawlHotelPage(self, start_url = None):
        if not start_url:
            start_url = self.start_urls

        while self.__next_url:
            selector = self.crawl(start_url)
            yield [self.domain + url.strip() for url in selector.xpath(self.hotelPageXpath)]
            
            self.__next_url = selector.xpath(self.nextPageXpath)
            if not self.__next_url:
                break
            self.__next_url = self.domain + self.__next_url[0]

    
    def parseAddress(self, selector):
        address = selector.xpath("//p[@class='address address_clean']/span/text()")[0].strip()
        return address[0:2], address[2:5], address[5:]
    

    def parseTourist(self, selector):
        tourists = []
        touristInfo = selector.xpath("//li[@class='bui-list__item']")
        for t in touristInfo:
            row = {}
            row['tourist']  = t.xpath("./div/div/text()")[0].strip()
            row['distance'] = t.xpath("./div/div/text()")[1].strip()
            tourists.append(row)
        return tourists


    def parse(self, hotelUrl):
        selector = self.crawl(hotelUrl)
        tourists = self.parseTourist(selector)
        city, town, address =  self.parseAddress(selector)

        name = selector.xpath("//h2[@id='hp_hotel_name']/text()")[1].strip()
        photo = selector.xpath("//a[@target='_blank']/@href")
        comments = selector.xpath("//span[@class='c-review__body']/text()")

        description = selector.xpath("//div[@id='property_description_content']/p/text()")
        description = ''.join(description)

        facilities = selector.xpath("//div[@class='hp_desc_important_facilities clearfix hp_desc_important_facilities--bui ']/div/text()")
        facilities = [i.strip() for i in list(filter(lambda x: x != '\n', facilities))]
            
        bed_type = selector.xpath("//div[@class='room-info']/a/text()")
        bed_type = [i.strip() for i in list(filter(lambda x: x != '\n', bed_type))]        
        
        stars = selector.xpath("//div[@class='bui-review-score c-score']/div[@class='bui-review-score__badge']/text()")
        stars = stars[0] if stars else 0 
        
        ratings = selector.xpath("//span[@class='hp__hotel_ratings']/span/i/@title")
        ratings = ratings[0] if ratings else 0 
        
        row = { 'pageUrl': hotelUrl,
                'hotel': name,
                'city': city,
                'town': town,
                'address': address,
                'ratings': int(ratings),
                'description': description,
                'facilities': facilities,
                'bed_type': bed_type,
                'tourists': tourists,
                'stars': float(stars),
                'comments': comments,
                'photo': photo
            }
        tasks.upload(row)