# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # hotel_id = scrapy.Field()
    # hotel_name = scrapy.Field()
    # hotel_url = scrapy.Field()
    # reviews = scrapy.Field()
    # total_value = scrapy.Field()
    # location_value = scrapy.Field()
    # cleanliness_value = scrapy.Field()
    # service_value = scrapy.Field()
    # value_value = scrapy.Field()
    # stars = scrapy.Field()
    single_record = scrapy.Field()


class ReviewInfoItem(scrapy.Item):
    single_review = scrapy.Field()
