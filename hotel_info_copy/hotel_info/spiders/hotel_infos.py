import scrapy
from lxml import etree

from collections import OrderedDict
import json
from urllib.parse import urlencode

from hotel_info.items import HotelInfoItem


class HotelInfosSpider(scrapy.Spider):
    name = 'hotel_infos'
    # allowed_domains = ['xxx']
    # start_urls = ['http://xxx/']
    # 为了防止item——pipelines的冲突，将project中的setting中的配置放到每个spider中
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'app.MyPipeline': 400,
            'hotel_info.pipelines.HotelInfoPipeline': 300,
        }
    }

    def start_requests(self):
        url = "https://www.tripadvisor.com/Hotels-g187427-Spain-Hotels.html"
        headers = {
            # 'accept': 'text/html, */*',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            # 'cache-control': 'no-cache',
            # 'content-length': '133',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.tripadvisor.com',
            # 'pragma': 'no-cache',
            'referer': 'https://www.tripadvisor.com/Hotels-g187427-Spain-Hotels.html',
            # 'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            # 'sec-fetch-dest': 'empty',
            # 'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'x-puid': '073032b3-b533-4848-88e8-25ab690ff811',
            'x-requested-with': 'XMLHttpRequest',
        }
        for page_number in range(10):
            data = {
                'plSeed': '1004003205',
                'offset': str(page_number * 30),
                # 'reqNum': '2',
                'isLastPoll': 'false',
                # 'paramSeqId': '4',
                # 'waitTime': '2526',
                'changeSet': '',
                'puid': '073032b3-b533-4848-88e8-25ab690ff811',
            }
            # 这种格式的请求是可以请求成功的
            # print(f"formdata={data}")
            print(f"开始请求第{page_number + 1}页")
            yield scrapy.Request(url, callback=self.parse,
                                 headers=headers, method='POST',
                                 body=urlencode(data))

            print(f"第{page_number + 1}页响应成功")

            # 可以构建FormRequest这种格式的,其中FormRequest也是继承自Request的，所以可以沿用它的参数
            # yield scrapy.FormRequest(url, callback=self.parse,
            #                          headers=headers,
            #                          data=)

    def parse(self, response):
        hotel_names = response.xpath("//div[@class='listing_title']//a/text()").getall()
        hotel_ids = response.xpath("//div[@class='listing_title']//a/@id").getall()
        hotel_urls = response.xpath('//a[@class="review_count"]/@href').getall()
        reviews_number = response.xpath('//a[@class="review_count"]/text()').getall()

        hotel_names = [name.strip() for name in hotel_names]
        hotel_ids = [hotel_id.replace("property_", "") for hotel_id in hotel_ids]
        hotel_urls = ["https://www.tripadvisor.com" + url for url in hotel_urls]
        reviews_number = [review.replace(" reviews", "").replace(',', '') if ',' in review else
                          review.replace(" reviews", "") for review in reviews_number]

        i = 0
        for hotel_id, hotel_name, hotel_url, reviews in zip(hotel_ids, hotel_names, hotel_urls, reviews_number):
            info = OrderedDict()
            info_temp = {
                'hotel_id': hotel_id,
                'hotel_name': hotel_name,
                'hotel_url': hotel_url,
                'reviews': reviews,
            }
            info.update(info_temp)
            another_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            }
            item = HotelInfoItem()
            item['single_record'] = info

            # print(f"ID为{info['hotel_id']}的店铺解析成功")
            i += 1

            yield scrapy.Request(hotel_url, headers=another_headers,
                                 callback=self.another_parse, meta={"item": item})
        print(f"该页共解析结果{i}个")


    def another_parse(self, response):
        html = etree.HTML(response.text, etree.HTMLParser())
        try:
            total_value = str(int(html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[1]/a/span[1]/@class')[0].split('_')[-1])/10)
        except Exception as e:
            total_value = None
        try:
            location_value = str(int(html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[2]/span/@class')[0].split('_')[-1])/10)
        except Exception as e:
            location_value = None
        try:
            cleanliness_value = str(int(html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[3]/span/@class')[0].split('_')[-1])/10)
        except Exception as e:
            cleanliness_value = None
        try:
            service_value = str(int(html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[4]/span/@class')[0].split('_')[-1])/10)
        except Exception as e:
            service_value = None
        try:
            value_value = str(int(html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[5]/span/@class')[0].split('_')[-1])/10)
        except Exception as e:
            value_value = None
        try:
            stars = html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[2]/div[3]/div[1]/div[2]/span/svg/@title')[0].split()[0]
        except Exception as e:
            stars = None
        try:
            reviews = html.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[1]/a/span[2]/text()')[0].split()[0]
            reviews = reviews.replace(',', '') if ',' in reviews else reviews
        except Exception as e:
            reviews = None
        temp_info = {
            'total_value': total_value,
            'location_value': location_value,
            'cleanliness_value': cleanliness_value,
            'service_value': service_value,
            'value_value': value_value,
            'stars': stars,
        }
        item = response.meta["item"]
        item['single_record'].update(temp_info)

        yield item


