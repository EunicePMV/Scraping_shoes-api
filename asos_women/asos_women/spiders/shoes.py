import scrapy
from scrapy.http import Request
import json
from urllib.request import urlopen

class ShoesSpider(scrapy.Spider):
    name = 'shoes'
    allowed_domains = ['asos.com']
    start_urls = ['http://www.asos.com/women/']

    def parse(self, response):
        converse_url = response.xpath("//*[@aria-labelledby='shop-by-brand-a11']//li//a[contains(@href, 'converse')]/@href").get()
        yield Request(converse_url,
                      callback=self.parse_converse)

    def parse_converse(self, response):
        shoes = response.xpath("//div[@class='_3-pwX1m']/div[@class='_2MoInDZ']/div[@class='_3pQmLlY']/section[@class='_3YREj-P']//article")
        for shoe in shoes:
            shoe_url = shoe.xpath(".//a/@href").get()
            yield Request(shoe_url,
                          callback=self.parse_shoe)

        page = response.xpath('//div[@class="fWxiz1Y"]/following-sibling::a/@href').get()
        if page:
            yield Request(page,
                          callback=self.parse_converse)

    def parse_shoe(self, response):
        name = response.xpath('//h1/text()').get()

        json_file = response.xpath("//script[@id='split-structured-data']/text()").get()
        shoes = json.loads(json_file)
        product_id = str(shoes['productID'])
        price_url = 'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds='+ product_id +'&store=ROW&currency=GBP'
        price_response = urlopen(price_url)
        price_json = json.loads(price_response.read())
        price = price_json[0]['productPrice']['current']['text']
        
        yield {'name': name,
               'price': price}