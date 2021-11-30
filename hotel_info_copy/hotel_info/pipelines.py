# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import redis
import pandas as pd

import os.path
import csv


class HotelInfoPipeline:
    def open_spider(self, spider):
        self.redis_client = redis.Redis()
        self.csv_header = ['hotel_id', 'hotel_name', 'hotel_url', 'reviews',
                      'total_value', 'location_value', 'cleanliness_value',
                      'service_value', 'value_value', 'stars']
        self.file_handle = open(os.path.dirname(__file__) + "/spiders/hotels.csv", 'w',
                                encoding='utf-8', newline='')
        self.writer = csv.DictWriter(self.file_handle, self.csv_header)
        self.writer.writeheader()
        # self.file_name = os.path.dirname(__file__) + "/spiders/hotels.csv"
        # with open(self.file_name, 'w', encoding='utf-8', newline='') as f:
        #     writer = csv.DictWriter(f, self.csv_header)
        #     writer.writeheader()

    def process_item(self, item, spider):
        hotel_id = item['single_record']['hotel_id']
        number_of_reviews = item['single_record']['reviews']
        self.redis_client.lpush('hotel_id', hotel_id)
        self.redis_client.lpush('number_of_reviews', number_of_reviews)
        self.writer.writerow(item['single_record'])

        # df = pd.DataFrame([item['single_record']], columns=self.csv_header)
        # df.to_csv(self.file_name, mode='a', header=False, index=False)

        return item


    def close_spider(self, spider):
        self.file_handle.close()



class ReviewInfoPipeline:
    def open_spider(self, spider):
        review_header = [
            'hotel_id',
            'hotel_name',
            'hotel_region',
            'displayed_username',
            'username',
            'review_text',
            'rating',
            "Rooms",
            "Cleanliness",
            "Service",
            'Location',
            "Sleep Quality",
        ]
        self.review_handle = open(os.path.dirname(__file__) + "/spiders/reviews_few.csv", 'w',
                                encoding='utf-8', newline='')
        self.writer = csv.DictWriter(self.review_handle, review_header)
        self.writer.writeheader()

    def process_item(self, review_item, spider):
        self.writer.writerow(review_item['single_review'])
        return review_item

    def close_spider(self, spider):
        self.review_handle.close()