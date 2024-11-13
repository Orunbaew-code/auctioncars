# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CopartCleanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class CopartItem(scrapy.Item):
    Title = scrapy.Field()
    Make = scrapy.Field()
    Model = scrapy.Field()
    Year = scrapy.Field()
    Mileage = scrapy.Field()
    Exterior = scrapy.Field()
    Interior = scrapy.Field()
    Drive_train = scrapy.Field()
    Engine = scrapy.Field()
    Sale_doc = scrapy.Field()
    Keys = scrapy.Field()
    Transmission = scrapy.Field()
    Buy_now = scrapy.Field()
    Fees = scrapy.Field()
    Cur_bid = scrapy.Field()
    Auction = scrapy.Field()
    End_date = scrapy.Field()