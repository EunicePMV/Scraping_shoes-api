# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

class AsosWomenItem(scrapy.Item):
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst)
    price = scrapy.Field(output_processor = TakeFirst)