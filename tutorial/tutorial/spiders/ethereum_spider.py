import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from ..items import EthereumItem
import pandas as pd
class QuotesSpider(scrapy.Spider):
    name = "ethereum"

    def start_requests(self):
        urls = [
            'https://etherscan.io/txs?p=100',
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
        previousLink = response.xpath('//a[contains(@aria-label,"Previous")]/@href').get()
        previousUrl = 'https://etherscan.io/' + previousLink
        yield scrapy.Request(url=previousUrl, callback=self.parse_previous, meta={'loader':myItem})
        
    def parse_previous(self, response):
        myItem = response.meta['loader']
        myItem.response = response
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
        previousLink = response.xpath('//a[contains(@aria-label,"Previous")]/@href').get()
        if(previousLink != None):
            previousUrl = 'https://etherscan.io/' + previousLink
            yield scrapy.Request(url=previousUrl, callback=self.parse_previous, meta={'loader':myItem})
        else:
            items = myItem.load_item()
            # print(len(items['txnHashUrl']))
            # print(len(items['txnHash']))
            # print(len(items['blockUrl']))
            # print(len(items['block']))
            # print(len(items['dateTime']))
            # print(len(items['fromAddressUrl']))
            # print(len(items['fromAddress']))
            # print(len(items['toAddressUrl']))
            # print(len(items['toAddress']))
            # print(len(items['valueEther']))
            # print(len(items['txnFee']))
            # print(items['valueEther'])
            df = pd.DataFrame(dict(items))
            #print(items)
            #print(df)
            df.to_csv("ethereum1.csv", index=False)