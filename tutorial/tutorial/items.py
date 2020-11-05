# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EthereumItem(scrapy.Item):
    txnHashUrl = scrapy.Field()
    txnHash = scrapy.Field()
    blockUrl = scrapy.Field()
    block = scrapy.Field()
    dateTime = scrapy.Field()
    fromAddressUrl = scrapy.Field()
    fromAddress = scrapy.Field()
    toAddress = scrapy.Field()
    toAddressUrl = scrapy.Field()
    valueEther = scrapy.Field()
    txnFee = scrapy.Field()
