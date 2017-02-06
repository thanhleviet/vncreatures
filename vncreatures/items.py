# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VncreaturesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    # pass


class PlantItem(scrapy.Item):
    id = scrapy.Field()
    species = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()


# class PlantDesc(scrapy.Item):
#     id = scrapy.Field()
#     description = scrapy.Field()
