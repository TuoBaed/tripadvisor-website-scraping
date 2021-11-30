import time

import requests

from collections import OrderedDict
import json
import csv
from pprint import pprint as pp
from multiprocessing.dummy import Pool as ThreadPool

def get_json_content(page_id, url='https://www.tripadvisor.com/data/graphql/batched'):
    # 这是request——payload参数，形式应该为JavaScript对象形式，其中需要替换的参数为null->None，false->False
    # page_number表示这是第几页评论，offset与page_number相对应，每页5个评论
    # location_id替换为对应的hotel的专属id，其中出现专属id的地方都要替换
    # 评论所占页数 = 总评论数 // 每页评论数 + 1 if 总评论数 // 每页评论数 == 0 else 总评论数 // 每页评论数
    # 每页最多20个评论
    limit_number = 20
    # 第几页
    page_number = page_id[0]
    # 每一页的起始评论编号
    offset_number = (page_number - 1) * limit_number
    # hotel的id号
    hotel_id = page_id[1]  # '3615334'
    hotel_id = int(hotel_id)
    data = [{
            "query": "mutation LogBBMLInteraction($interaction: ClientInteractionOpaqueInput!) {\n  logProductInteraction(interaction: $interaction)\n}\n",
            "variables": {
                "interaction": {
                    "productInteraction": {
                        "interaction_type": "CLICK",
                        "item": {
                            "item_attributes": {
                                "action_name": "REVIEW_NAV",
                                "element_type": "number",
                                "limit": limit_number,
                                "offset": offset_number,
                                "page_number": page_number
                            },
                            "item_id": hotel_id,
                            "item_id_type": "ta-location-id",
                            "product_type": "Hotels"
                        },
                        "item_group": {
                            "item_group_collection_key": "44b94aed-e68b-4653-a7e5-98ac10b1ebdf"
                        },
                        "pageview": {
                            "pageview_attributes": {
                                "geo_id": 1080448,
                                "location_id": hotel_id,
                                "servlet_name": "Hotel_Review"
                            },
                            "pageview_request_uid": "44b94aed-e68b-4653-a7e5-98ac10b1ebdf"
                        },
                        "search": {},
                        "site": {
                            "site_business_unit": "Hotels",
                            "site_domain": "www.tripadvisor.com",
                            "site_name": "ta"
                        },
                        "user": {
                            "site_persistent_user_uid": "web554a.183.188.206.93.17BA9757B5B",
                            "unique_user_identifiers": {
                                "session_id": "BD2E018AEF7A49EFA0F4F846C47B952C"
                            },
                            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                        }
                    }
                }
            }
        }, {
            "query": "query ReviewListQuery($locationId: Int!, $offset: Int, $limit: Int, $filters: [FilterConditionInput!], $prefs: ReviewListPrefsInput, $initialPrefs: ReviewListPrefsInput, $filterCacheKey: String, $prefsCacheKey: String, $keywordVariant: String!, $needKeywords: Boolean = true) {\n  cachedFilters: personalCache(key: $filterCacheKey)\n  cachedPrefs: personalCache(key: $prefsCacheKey)\n  locations(locationIds: [$locationId]) {\n    locationId\n    parentGeoId\n    name\n    placeType\n    reviewSummary {\n      rating\n      count\n    }\n    keywords(variant: $keywordVariant) @include(if: $needKeywords) {\n      keywords {\n        keyword\n      }\n    }\n    ... on LocationInformation {\n      parentGeoId\n    }\n    ... on LocationInformation {\n      parentGeoId\n    }\n    ... on LocationInformation {\n      name\n      currentUserOwnerStatus {\n        isValid\n      }\n    }\n    ... on LocationInformation {\n      locationId\n      currentUserOwnerStatus {\n        isValid\n      }\n    }\n    ... on LocationInformation {\n      locationId\n      parentGeoId\n      accommodationCategory\n      currentUserOwnerStatus {\n        isValid\n      }\n      url\n    }\n    reviewListPage(page: {offset: $offset, limit: $limit}, filters: $filters, prefs: $prefs, initialPrefs: $initialPrefs, filterCacheKey: $filterCacheKey, prefsCacheKey: $prefsCacheKey) {\n      totalCount\n      preferredReviewIds\n      reviews {\n        ... on Review {\n          id\n          url\n          location {\n            locationId\n            name\n          }\n          createdDate\n          publishedDate\n          provider {\n            isLocalProvider\n          }\n          userProfile {\n            id\n            userId: id\n            isMe\n            isVerified\n            displayName\n            username\n            avatar {\n              id\n              photoSizes {\n                url\n                width\n                height\n              }\n            }\n            hometown {\n              locationId\n              fallbackString\n              location {\n                locationId\n                additionalNames {\n                  long\n                }\n                name\n              }\n            }\n            contributionCounts {\n              sumAllUgc\n              helpfulVote\n            }\n            route {\n              url\n            }\n          }\n        }\n        ... on Review {\n          title\n          language\n          url\n        }\n        ... on Review {\n          language\n          translationType\n        }\n        ... on Review {\n          roomTip\n        }\n        ... on Review {\n          tripInfo {\n            stayDate\n          }\n          location {\n            placeType\n          }\n        }\n        ... on Review {\n          additionalRatings {\n            rating\n            ratingLabel\n          }\n        }\n        ... on Review {\n          tripInfo {\n            tripType\n          }\n        }\n        ... on Review {\n          language\n          translationType\n          mgmtResponse {\n            id\n            language\n            translationType\n          }\n        }\n        ... on Review {\n          text\n          publishedDate\n          username\n          connectionToSubject\n          language\n          mgmtResponse {\n            id\n            text\n            language\n            publishedDate\n            username\n            connectionToSubject\n          }\n        }\n        ... on Review {\n          id\n          locationId\n          title\n          text\n          rating\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          photos {\n            id\n            statuses\n            photoSizes {\n              url\n              width\n              height\n            }\n          }\n          userProfile {\n            id\n            displayName\n            username\n          }\n        }\n        ... on Review {\n          mgmtResponse {\n            id\n          }\n          provider {\n            isLocalProvider\n          }\n        }\n        ... on Review {\n          translationType\n          location {\n            locationId\n            parentGeoId\n          }\n          provider {\n            isLocalProvider\n            isToolsProvider\n          }\n          original {\n            id\n            url\n            locationId\n            userId\n            language\n            submissionDomain\n          }\n        }\n        ... on Review {\n          locationId\n          mcid\n          attribution\n        }\n        ... on Review {\n          __typename\n          locationId\n          helpfulVotes\n          photoIds\n          route {\n            url\n          }\n          socialStatistics {\n            followCount\n            isFollowing\n            isLiked\n            isReposted\n            isSaved\n            likeCount\n            repostCount\n            tripCount\n          }\n          status\n          userId\n          userProfile {\n            id\n            displayName\n            isFollowing\n          }\n          location {\n            __typename\n            locationId\n            additionalNames {\n              normal\n              long\n              longOnlyParent\n              longParentAbbreviated\n              longOnlyParentAbbreviated\n              longParentStateAbbreviated\n              longOnlyParentStateAbbreviated\n              geo\n              abbreviated\n              abbreviatedRaw\n              abbreviatedStateTerritory\n              abbreviatedStateTerritoryRaw\n            }\n            parent {\n              locationId\n              additionalNames {\n                normal\n                long\n                longOnlyParent\n                longParentAbbreviated\n                longOnlyParentAbbreviated\n                longParentStateAbbreviated\n                longOnlyParentStateAbbreviated\n                geo\n                abbreviated\n                abbreviatedRaw\n                abbreviatedStateTerritory\n                abbreviatedStateTerritoryRaw\n              }\n            }\n          }\n        }\n        ... on Review {\n          text\n          language\n        }\n        ... on Review {\n          locationId\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          originalLanguage\n          rating\n        }\n        ... on Review {\n          id\n          locationId\n          title\n          labels\n          rating\n          absoluteUrl\n          mcid\n          translationType\n          mtProviderId\n          alertStatus\n        }\n      }\n    }\n    reviewAggregations {\n      ratingCounts\n      languageCounts\n      alertStatusCount\n    }\n  }\n}\n",
            "variables": {
                "filterCacheKey": None,
                "filters": [],
                "initialPrefs": {},
                "keywordVariant": "location_keywords_v2_llr_order_30_en",
                "limit": limit_number,
                "locationId": hotel_id,
                "needKeywords": False,
                "offset": offset_number,
                "prefs": None,
                "prefsCacheKey": "locationReviewPrefs"
            }
        }, {
            "query": "query PageTargetingQuery($pageAdsRequestInput: AdContext_PageAdsRequestInput) {\n  gptInfo: AdContext_getPageAdsBatch(requests: [$pageAdsRequestInput]) {\n    adBase\n    ppid\n    pageLevelTargeting {\n      key\n      value\n    }\n  }\n}\n",
            "variables": {
                "pageAdsRequestInput": {
                    "browserType": "CHROME",
                    "drs": [{
                            "sliceNum": 90,
                            "space": "ABC"
                        }, {
                            "sliceNum": 78,
                            "space": "AFIL"
                        }, {
                            "sliceNum": 28,
                            "space": "ATTPromo"
                        }, {
                            "sliceNum": 29,
                            "space": "AUC"
                        }, {
                            "sliceNum": 37,
                            "space": "BBML"
                        }, {
                            "sliceNum": 63,
                            "space": "BMP"
                        }, {
                            "sliceNum": 52,
                            "space": "BRDTTD"
                        }, {
                            "sliceNum": 6,
                            "space": "Brand"
                        }, {
                            "sliceNum": 68,
                            "space": "CAKE"
                        }, {
                            "sliceNum": 46,
                            "space": "CAR"
                        }, {
                            "sliceNum": 30,
                            "space": "COM"
                        }, {
                            "sliceNum": 49,
                            "space": "CRS"
                        }, {
                            "sliceNum": 95,
                            "space": "Community"
                        }, {
                            "sliceNum": 51,
                            "space": "Content"
                        }, {
                            "sliceNum": 95,
                            "space": "CoreX"
                        }, {
                            "sliceNum": 51,
                            "space": "EATPIZZA"
                        }, {
                            "sliceNum": 28,
                            "space": "EID"
                        }, {
                            "sliceNum": 28,
                            "space": "EXP"
                        }, {
                            "sliceNum": 33,
                            "space": "Engage"
                        }, {
                            "sliceNum": 66,
                            "space": "FDP"
                        }, {
                            "sliceNum": 81,
                            "space": "FDS"
                        }, {
                            "sliceNum": 16,
                            "space": "FDU"
                        }, {
                            "sliceNum": 49,
                            "space": "FLTMERCH"
                        }, {
                            "sliceNum": 56,
                            "space": "FLTREV"
                        }, {
                            "sliceNum": 92,
                            "space": "Filters"
                        }, {
                            "sliceNum": 88,
                            "space": "Flights"
                        }, {
                            "sliceNum": 8,
                            "space": "HRATF"
                        }, {
                            "sliceNum": 92,
                            "space": "HSX"
                        }, {
                            "sliceNum": 43,
                            "space": "HSXB"
                        }, {
                            "sliceNum": 52,
                            "space": "IBEX"
                        }, {
                            "sliceNum": 90,
                            "space": "ING"
                        }, {
                            "sliceNum": 61,
                            "space": "INT1"
                        }, {
                            "sliceNum": 39,
                            "space": "INT2"
                        }, {
                            "sliceNum": 47,
                            "space": "ITR"
                        }, {
                            "sliceNum": 15,
                            "space": "L10N"
                        }, {
                            "sliceNum": 24,
                            "space": "ML"
                        }, {
                            "sliceNum": 96,
                            "space": "ML6"
                        }, {
                            "sliceNum": 31,
                            "space": "MM"
                        }, {
                            "sliceNum": -1,
                            "space": "MOBILEAPP"
                        }, {
                            "sliceNum": 75,
                            "space": "MOF"
                        }, {
                            "sliceNum": 56,
                            "space": "MPS"
                        }, {
                            "sliceNum": 24,
                            "space": "MTA"
                        }, {
                            "sliceNum": 87,
                            "space": "Me2"
                        }, {
                            "sliceNum": 19,
                            "space": "Mem"
                        }, {
                            "sliceNum": 82,
                            "space": "Mobile"
                        }, {
                            "sliceNum": 58,
                            "space": "MobileCore"
                        }, {
                            "sliceNum": 22,
                            "space": "Notifications"
                        }, {
                            "sliceNum": 42,
                            "space": "Other"
                        }, {
                            "sliceNum": 31,
                            "space": "P13N"
                        }, {
                            "sliceNum": 66,
                            "space": "PIE"
                        }, {
                            "sliceNum": 7,
                            "space": "PLS"
                        }, {
                            "sliceNum": 45,
                            "space": "POS"
                        }, {
                            "sliceNum": 33,
                            "space": "PRT"
                        }, {
                            "sliceNum": 68,
                            "space": "RDS1"
                        }, {
                            "sliceNum": 37,
                            "space": "RDS2"
                        }, {
                            "sliceNum": 20,
                            "space": "RDS3"
                        }, {
                            "sliceNum": 4,
                            "space": "RDS4"
                        }, {
                            "sliceNum": 18,
                            "space": "RDS5"
                        }, {
                            "sliceNum": 98,
                            "space": "RET"
                        }, {
                            "sliceNum": 40,
                            "space": "REV"
                        }, {
                            "sliceNum": 88,
                            "space": "REVB"
                        }, {
                            "sliceNum": 70,
                            "space": "REVH"
                        }, {
                            "sliceNum": 73,
                            "space": "REVM"
                        }, {
                            "sliceNum": 17,
                            "space": "REVSD"
                        }, {
                            "sliceNum": 14,
                            "space": "REVSP"
                        }, {
                            "sliceNum": 81,
                            "space": "REVXS"
                        }, {
                            "sliceNum": 82,
                            "space": "RNA"
                        }, {
                            "sliceNum": 57,
                            "space": "RSE1"
                        }, {
                            "sliceNum": 30,
                            "space": "RSE2"
                        }, {
                            "sliceNum": 87,
                            "space": "Rooms"
                        }, {
                            "sliceNum": 98,
                            "space": "S3PO"
                        }, {
                            "sliceNum": 68,
                            "space": "SD40"
                        }, {
                            "sliceNum": 78,
                            "space": "SE2O"
                        }, {
                            "sliceNum": 22,
                            "space": "SEM"
                        }, {
                            "sliceNum": 52,
                            "space": "SEO"
                        }, {
                            "sliceNum": 88,
                            "space": "SORT1"
                        }, {
                            "sliceNum": 2,
                            "space": "Sales"
                        }, {
                            "sliceNum": 1,
                            "space": "Search"
                        }, {
                            "sliceNum": 66,
                            "space": "SiteX"
                        }, {
                            "sliceNum": 28,
                            "space": "Surveys"
                        }, {
                            "sliceNum": 77,
                            "space": "T4B"
                        }, {
                            "sliceNum": 52,
                            "space": "TGT"
                        }, {
                            "sliceNum": 35,
                            "space": "TRP"
                        }, {
                            "sliceNum": 10,
                            "space": "TTD"
                        }, {
                            "sliceNum": 94,
                            "space": "TX"
                        }, {
                            "sliceNum": 48,
                            "space": "Timeline"
                        }, {
                            "sliceNum": 93,
                            "space": "VP"
                        }, {
                            "sliceNum": 11,
                            "space": "VR"
                        }, {
                            "sliceNum": 3,
                            "space": "YM"
                        }, {
                            "sliceNum": 42,
                            "space": "YMB"
                        }
                    ],
                    "globalContextUrlParameters": [{
                            "key": "offset",
                            "value": "r15"
                        }, {
                            "key": "detailId",
                            "value": str(hotel_id)
                        }, {
                            "key": "geoId",
                            "value": "1080448"
                        }
                    ],
                    "hotelTravelInfo": {
                        "checkInDate": "2021-10-02",
                        "checkOutDate": "2021-10-03",
                        "defaultDates": False
                    },
                    "locationId": hotel_id,
                    "pageType": "Hotel_Review",
                    "userAgentCategory": "DESKTOP"
                }
            }
        }
    ]

    # 有意思的是referer中会出现hotel的专属id，但是获取另一店铺评论数据的响应时却不需要替换其中的内容
    # 可能的原因是referer中的内容并不作为反爬的依据
    # 参与反爬的内容基本就是以下几样
    headers = {
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '11745',
        'content-type': 'application/json',
        'Host': 'www.tripadvisor.com',
        'Origin': 'https://www.tripadvisor.com',
        # 'Pragma': 'no-cache',
        # 'Referer': 'https://www.tripadvisor.com/Hotel_Review-g187443-d16643865-Reviews-or15-H10_Casa_de_la_Plata-Seville_Province_of_Seville_Andalucia.html',
        # 'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'x-requested-by': 'TNI1625!AKlGxBQVUyBYlc8tt/4B6Rzh0HgjsScYl7R1yYJpFqGdTEVVItEQvENwKI30nzXM7+mokZO/Q1fsi4tp2TyIQHvaBLJ0MCEWafzM+B7z1dZ8rghutAePnXF906FUqw1Jyc2qt059RInvd9+Ks6DdS/FAv0nSNkWHc2JXxmngxhaN',
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.encoding = 'utf-8'
        print(f"店铺ID为{hotel_id}的第{page_number}页评论请求成功，状态码为{response.status_code}")
        results = response.json()
    except Exception as e:
        results = None
        print(f"店铺ID为{hotel_id}的第{page_number}页评论请求失败")
    return results


def parse_reviews(json_content):
    if json_content:
        reviews = json_content[1]['data']["locations"][0]["reviewListPage"]['reviews']
        for review_index, review in enumerate(reviews, 1):
            review_info = OrderedDict()
            try:
                hotel_id = review['location']['locationId']  # hotel_id,唯一标识一个hotel
            except Exception as e:
                hotel_id = None
            try:
                hotel_name = review['location']['name']
            except Exception as e:
                hotel_name = None
            try:
                hotel_region = review['location']['parent']["additionalNames"]["long"]
            except Exception as e:
                hotel_region = None
            try:
                displayed_username = review["userProfile"]["displayName"]
            except Exception as e:
                displayed_username = None
            try:
                username = review["userProfile"]["username"]
            except Exception as e:
                username = None
            try:
                review_text = review['text'],
            except Exception as e:
                review_text = None
            try:
                rating = review['rating']
            except Exception as e:
                rating = None
            temp_info = {
                'hotel_id': hotel_id,  # hotel_id,唯一标识一个hotel
                'hotel_name': hotel_name,
                'hotel_region': hotel_region,
                'displayed_username': displayed_username,
                'username': username,
                'review_text': review_text,
                'rating': rating,
                "Rooms": None,
                "Cleanliness": None,
                "Service": None,
                'Location': None,
                "Sleep Quality": None
            }
            review_info.update(temp_info)
            # 检查是否有分评论打分，如果有，也将其加入到字段中
            additionalRatings = review["additionalRatings"]
            if additionalRatings:
                for additionrating in additionalRatings:
                    if additionrating["ratingLabel"] in ["Rooms", "Cleanliness", "Service", 'Location', "Sleep Quality"]:
                        review_info.update({additionrating["ratingLabel"]: additionrating['rating']})

            print(f"店铺ID为{review_info['hotel_id']}的第{review_index}条评论解析成功")
            # pp(review_info)
            yield review_info


def main(id_reviews_list):
    for hotel_id, reviews in id_reviews_list:
        # 根据评论数量构建评论页数
        page_number = reviews // 20 if reviews % 20 == 0 else reviews // 20 + 1
        for page in range(1, page_number+1):
            for single_review in parse_reviews(get_json_content((page, hotel_id))):
                # pp(single_review)
                global writer
                writer.writerow(single_review)


def main_pool(*args):
    for hotel_id, reviews in zip(args[0], args[1]):
        # 根据评论数量构建评论页数
        page_number = reviews // 20 if reviews % 20 == 0 else reviews // 20 + 1
        for page in range(1, page_number+1):
            for single_review in parse_reviews(get_json_content((page, hotel_id))):
                # pp(single_review)
                global writer
                writer.writerow(single_review)


if __name__ == '__main__':
    start_time = time.time()
    csv_header = [
        'hotel_id', 'hotel_name', 'hotel_url', 'reviews', 'total_value',
        'location_value', 'cleanliness_value', 'service_value', 'value_value', 'stars',
    ]
    # 读取hotel_id以及店铺的评论数量到一个列表中
    id_reviews_list = []
    with open('hotel_detail_new.csv', 'r') as f:
        csv_reader = csv.DictReader(f, csv_header)
        for row in csv_reader:
            if row['hotel_id'] != 'hotel_id':
                id_reviews_list.append((row['hotel_id'], int(row['reviews'])))

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

    with open('reviews_new.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, review_header)
        writer.writeheader()
        main(id_reviews_list)
        # pool.join()
        # pool.close()
    print(f"共耗时{time.time() - start_time} seconds")


    # # 线程池版本, 不理想
    # pool = ThreadPool()
    # with open('reviews_pool.csv', 'w', encoding='utf-8', newline='') as f:
    #     writer = csv.DictWriter(f, review_header)
    #     writer.writeheader()
    #     args1 = (item[0] for item in id_reviews_list)
    #     args2 = (item[0] for item in id_reviews_list)
    #     pool.map(main_pool, (args1, args2))
    #     # pool.join()
    #     # pool.close()
    # print(f"共耗时{time.time() - start_time} seconds")

    # main(id_reviews_list)
    # for hotel_id, reviews in id_reviews_list:
    #     # 根据评论数量构建评论页数
    #     page_number = reviews // 20 if reviews % 20 == 0 else reviews // 20 + 1
    #     for page in range(1, page_number+1):
    #         parse_reviews(get_json_content((page, hotel_id)))


    # reviews = results[1]['data']["locations"][0]["reviewListPage"]['reviews']
    # >> > type(reviews)
    # <
    #
    # class 'list'>
    #
    # >> > len(reviews)
    # 20
    # >> > locationid = results[1]['data']["locations"][0]["locationId"]
    # >> > locationid
    # 20010678
    # >> > parentid = results[1]['data']["locations"][0]["parentGeoId"]
    # >> > parentid
    # 1080448
    # >> > username = reviews[0]["username"]
    # >> > usename
