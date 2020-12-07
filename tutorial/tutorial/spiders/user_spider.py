import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from ..items import EthereumItem
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import time
class UserSpider(scrapy.Spider):
    name = "user"

    def start_requests(self):
        urls = [
            'https://etherscan.io/txs',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # for quote in response.css('td.price'):
        #     yield {
        #         'text': quote.css('div::text').get(),}
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall()
        myItem = ItemLoader(item=EthereumItem(), response=response)
        myItem.add_xpath('txnHashUrl', '//tr/td[2]/span/a/@href')
        myItem.add_xpath('txnHash', '//tr/td[2]/span/a/text()')
        myItem.add_xpath('blockUrl', '//tr/td[3]/a/@href')
        myItem.add_xpath('block', '//tr/td[3]/a/text()')
        myItem.add_xpath('dateTime', '//td[contains(@class,"showDate")]/span/text()')
        myItem.add_xpath('fromAddressUrl', '//tr/td[6]/span/a/@href | //tr/td[6]/a/@href')
        myItem.add_xpath('fromAddress', '//tr/td[6]/span/a/text() | //tr/td[6]/a/text()')
        myItem.add_xpath('toAddressUrl', '//tr/td[8]/span/a/@href | //tr/td[8]/span/span/a/@href | //tr/td[8]/a/@href')
        myItem.add_xpath('toAddress', '//tr/td[8]/span/a/text() | //tr/td[8]/span/span/a/text() | //tr/td[8]/a/text()')
        valueEther = [valueEther.xpath('normalize-space(.)').get() for valueEther in response.xpath('//tr/td[9]')]
        txnFee = [txnFee.xpath('normalize-space(./span)').get() for txnFee in response.xpath('//tr/td[10]')]
        myItem.add_value('valueEther',valueEther)
        myItem.add_value('txnFee', txnFee)
        items = myItem.load_item()
        #producer = KafkaProducer(bootstrap_servers=['192.168.43.75:9092'])
        item = dict(items)
        
        for row in zip(item['fromAddress'], item['toAddress'], item['dateTime'], item['valueEther']):
            message = row[0]+' '+row[1]+' '+row[2]+' '+row[3].split(' ')[0]
            print(message)
            #producer.send('quickstart-events',message.encode('utf-8'))
            #time.sleep(2)
        print("length", len(item['fromAddress']))
        
        time.sleep(2)
        yield scrapy.Request(url='https://etherscan.io/txs', callback=self.parse)

