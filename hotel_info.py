"""
7. 爬取网站https://www.tripadvisor.com/Hotels-g187427-Spain-Hotels.html下的所有酒店
   的评价用户名称以及系统给出的总评分。
   - 系统评分：总评分
   - 环节评分：Location
             Cleanliness
             Service
             Value
   - 酒店名
   - 给酒店加个id
   - 每个酒店用户的姓名
   - 对该酒店的总评分
   - 有的酒店还有每个用户对其的分评分（room，cleanliness，service），必要时还需要对这3个分评分
     进行采集
"""
import requests
from lxml import etree

import csv
import time
import re
import json
from pprint import pprint as pp
from collections import OrderedDict
from multiprocessing.dummy import Pool as ThreadPool


url = "https://www.tripadvisor.com/Hotels-g187427-Spain-Hotels.html"


def get_hotel_html(page_number, url=url):
    data = {
        'plSeed': '1004003205',
        'offset': page_number * 30,
        # 'reqNum': '2',
        'isLastPoll': 'false',
        # 'paramSeqId': '4',
        # 'waitTime': '2526',
        'changeSet': '',
        'puid': '073032b3-b533-4848-88e8-25ab690ff811',
    }
    headers = {
        # 'accept': 'text/html, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        # 'cache-control': 'no-cache',
        # 'content-length': '133',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'TAUnique=%1%enc%3ANJIaHuufTG1VAUNSOdFCtl02CRZ9BjTOazyitDsNXGio5z%2Foq3Ib9g%3D%3D; TASSK=enc%3AALB4aRQD%2Bm9TFnKHq4kix691hKRLm155XQyQkD%2FItp5cMvxzPB8wSdndt0NCbldK9oPsqvRe73AS3eLOh3eeBmosxOXSnlv%2BDTUsvaj6Gp8CuMm7pstsbRv3X%2Bycj4cVZg%3D%3D; __ssid=ef0566d14d6a92020dcce694e2767b4; TADCID=zzHnFZKhII4X86a3ABQCFdpBzzOuRA-9xvCxaMyI12hdU6ipDYKn8z6A9WA2HGgJlOEEv3YNus8Cl3kjkhKdTtLplLEJFV57v4M; PAC=ADii9cf_tJQTqgFI_uOWTb6czXzbH_G_2ack6piAvHMdeHCZF7VKMsyarvGTn5jbqR0UooXQyAWc57HE_bZN53MdkyOm9fFvHmxaG_Ih_LCB82HTBXF0L7lLtd-c26EgkGYN5CzGvK_J36bQuo-KLieTwSCSC5RqCoAxjJlI9ed2; ServerPool=X; PMC=V2*MS.84*MD.20210902*LD.20210923; TART=%1%enc%3AVQFDUjnRQrbuHEfJ7Ugvv%2B2yQl4y5RzRpucU6Wje8BL6j7CFiW0omQdSO0jRAqittAVPBtssWSk%3D; TATravelInfo=V2*AY.2021*AM.10*AD.3*DY.2021*DM.10*DD.4*A.2*MG.-1*HP.2*FL.3*DSM.1632392190698*AZ.1*RS.1; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; TASID=BD2E018AEF7A49EFA0F4F846C47B952C; ak_bmsc=E7A06E8E87BF41D114E6309B9F603498~000000000000000000000000000000~YAAQLFgDF3rH0JJ7AQAAH0lNEg3G4vue/WmAGptK3o7/tX3xFqeBBZw1s91cq7KdeAl6oud37F85hZGKb+SJrYu63394mwq3CE0EeTuAFWTbsbkVJ/edZxTc5IM29ovgcPsV5cHFXe510vmwLDLjBWWA5qRbiWFgl5cqSNAix7uyqRPCtSLRLqwGFgDKPDj8acTxNOsvIwSxyBGSl96U5sZ9PQthqQhkE4IdEkTVhFA4QK/V1ZTp8yYAfEJb6aGFzmlo8o842e3z2c1kkZR+lKTlO5OUiei6Mze0Ug9sF+TC/GGL8f/1U1Yiiz+bSRdfTVfTHHTcUC3UjttYZJtdr/KLdCjqcvIp5DypYQJoDxTUauGmqtsTn4XMg2sC+XDBHgtv7L1QWRAHvKC2zz8Nxw==; bm_sv=86457905A68BACCD4E9C7F5A3932684A~z4U9eQFYO5lBP4RLfnDWOt1NtyB2uMpPwpNySV4rmEqUNl8RxetnObFeTCJfIVZaxxwpuUnuUllQrlprag5dYb7iAWJSlLtK1wbYA2pGMyvYzhGPgFdxx0hdpEkpkGNflGNPTsSYF+G+AJE32jq5k3uGlB+qG0gEm60aGyX7xlg=; __vt=77AYm8Yhgm9aJ4SaABQCIf6-ytF7QiW7ovfhqc-AvRg7KKCXmdW3HWYqCqm8CW6EwgC6syProrQk8IQgJIP438o1OLvQjbAkW__r58NQ59PauUo4BO1SxE1PgvXBTd2trNeCGVDQs742ZSY2f3nZCD9e5g; roybatty=TNI1625!AL%2FAzmW4n%2FelODh%2FP3xAz4A06pvHD%2FsH60kDl3lcuQOdR26t7laxiLIpP604eiZCKiGUr%2BXcyq3ccr2HKiMSbu2mTpontXMj48Rpa0PekosSZYnQ%2BZzjLwLJOWQvvT7o7Q7TNz2RGA%2FWlUTr5oZNAotTUTaqE1ZD%2By8zVbjKl%2FWU%2C1; TASession=V2ID.BD2E018AEF7A49EFA0F4F846C47B952C*SQ.58*LS.DemandLoadAjax*GR.27*TCPAR.12*TBR.91*EXEX.94*ABTR.73*PHTB.11*FS.8*CPU.6*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*TRA.false*LD.187427*EAU._; TAUD=LA-1632392065409-1*HDD-1-2021_10_03.2021_10_04*RDD-1-2021_09_23*ARDD-125298-2021_10_03.2021_10_04*HD-125735-2021_10_03.2021_10_04.187427*G-125736-2.1.187427.*LD-3386209-2021.10.3.2021.10.4*LG-3386212-2.1.T.; TAReturnTo=%1%%2FHotels%3Fg%3D187427%26offset%3D60%26reqNum%3D1%26puid%3D073032b3-b533-4848-88e8-25ab690ff811%26isLastPoll%3Dfalse%26plSeed%3D1004003205%26waitTime%3D74%26paramSeqId%3D3%26changeSet%3DMAIN_META%2CPAGE_OFFSET',
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
    try:
        response = requests.post(url=url, data=data, headers=headers)
        response.encoding = 'utf-8'
        print(f"第{page_number + 1}页响应成功，状态码为{response.status_code}")
    except Exception as e:
        print(f"获取失败")
    print("The One Barcelona" in response.text)
    return response


def parse_hotel_info(content):
    # hotel id, hotel name, hotel detail url and reviews number
    html = etree.HTML(content.content, etree.HTMLParser())

    hotel_names = html.xpath("//div[@class='listing_title']//a/text()")
    hotel_ids = html.xpath("//div[@class='listing_title']//a/@id")
    hotel_urls = html.xpath('//a[@class="review_count"]/@href')
    reviews_number = html.xpath('//a[@class="review_count"]/text()')

    hotel_names = [name.strip() for name in hotel_names]
    hotel_ids = [hotel_id.replace("property_", "") for hotel_id in hotel_ids]
    hotel_urls = ["https://www.tripadvisor.com" + url for url in hotel_urls]
    reviews_number = [review.replace(" reviews", "").replace(',', '') if ',' in review else
                      review.replace(" reviews", "") for review in reviews_number]
    # print(hotel_names)
    # print(hotel_ids)
    # print(hotel_urls)
    # print(reviews_number)
    for hotel_id, hotel_name, hotel_url, reviews in zip(hotel_ids, hotel_names, hotel_urls, reviews_number):
        info = OrderedDict()
        info_temp = {
            'hotel_id': hotel_id,
            'hotel_name': hotel_name,
            'hotel_url': hotel_url,
            'reviews': reviews,
        }
        info.update(info_temp)
        detail_info = parse_detail_info(get_html(hotel_url))
        info.update(detail_info)
        # pp(info)
        yield info


def get_html(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'TAUnique=%1%enc%3ANJIaHuufTG1VAUNSOdFCtl02CRZ9BjTOazyitDsNXGio5z%2Foq3Ib9g%3D%3D; TASSK=enc%3AALB4aRQD%2Bm9TFnKHq4kix691hKRLm155XQyQkD%2FItp5cMvxzPB8wSdndt0NCbldK9oPsqvRe73AS3eLOh3eeBmosxOXSnlv%2BDTUsvaj6Gp8CuMm7pstsbRv3X%2Bycj4cVZg%3D%3D; __ssid=ef0566d14d6a92020dcce694e2767b4; TADCID=zzHnFZKhII4X86a3ABQCFdpBzzOuRA-9xvCxaMyI12hdU6ipDYKn8z6A9WA2HGgJlOEEv3YNus8Cl3kjkhKdTtLplLEJFV57v4M; TART=%1%enc%3AVQFDUjnRQrbuHEfJ7Ugvv%2B2yQl4y5RzRpucU6Wje8BL6j7CFiW0omQdSO0jRAqittAVPBtssWSk%3D; TATravelInfo=V2*AY.2021*AM.10*AD.3*DY.2021*DM.10*DD.4*A.2*MG.-1*HP.2*FL.3*DSM.1632392190698*AZ.1*RS.1; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; ServerPool=X; PMC=V2*MS.84*MD.20210902*LD.20210924; TASID=5195B334147449498569EDD13A4B02EF; ak_bmsc=EC7BA916E1268679682E014BBEBA21F9~000000000000000000000000000000~YAAQVVcyuGYg5hV8AQAAiItSFg220SMjdUxrRkeAQ0onf1Q/aKb+3IR7hErGMHwEvC5V8TTu626yFOC4PKE3mdfA2gya600iJ587w+wypczvpujov2VVVhmrldLm/DFOSeES2ssUMpQHnJGSO7DuuCcGNuHKJ6SKESUM7anzbfSfb4pk1Zzx5/SPvfQ2sowXtucMjuE82MLrU11khkTETqNbmofNoJBhLjnyLPtBDZkApgRDZc7lE6bNCFnCyD8cznqc0twS2fEHWBIEn+jU+PnS9iQp9gphQO++NnbcTV/wom1J01u5WkjLl0XahwmhPI/GRKvMsbHsNYhObSOJwpIsY+iPfNrKgvr2QLV7X3U5nllW1D8zvdQ/tdllHfNnczkYZf3V/m5Ss6S5bjmeAg==; PAC=AIWm0kRfBerh8YmyfVZeb4_iMusg5Cm4o9wJHxkXZz3acSrSaEVKU0Mo4Q0XY_CJKdKqQwAk6RE7vRUHu8XDQRvYRE0DA9NU_tDVfTYS9dPqQBB9OtU-nlQ9Vte0aFNbYk9mrWlfIHHHdthuT1xhubb7rJS4GhYnC1wcKePh81n7pnFBfePj9QxOxV0tM8vjVlm83EvQxtcStKQjeTG7HEEWARY_wYd3P25u5HTvvdLBL-0yyMKRTkftBbTu8OdxTwJPGUdTIdyZWtVz6pCFiWw%3D; TAReturnTo=%1%%2FHotel_Review-g187443-d16643865-Reviews-or5-H10_Casa_de_la_Plata-Seville_Province_of_Seville_Andalucia.html; roybatty=TNI1625!AI4FGJoFGA2H0GtCVHAW%2B%2B5vQSZT%2FmlslwBXjZkyCZzt6oQYy7qfvK%2BsB6kbtOOTe7EX7E8FtKh5K9bynIEjvqH75pcGBcC9ugd%2FY8QP%2F2sBu0c89PZI3P%2BS4ThpP%2FMYh%2BKzZyAWbIRmEbrx%2FR3khCAzTSzCpIqIDL%2FDQtUAGEpd%2C1; bm_sv=408446E1A1B44AC9AA670633EF5B1EA9~0kIS7jGT9GQchVwFuxsVlriHKgeEc3aimy+NtXAswmSm340puUXSzrjzvV3fz2hGcUSkuVdIS0QxCIJgBHia+LzU02PXcnb4+HBy+UFDskBbfgBimkJype/zs0tVMwl9RHcaZnK77gaNrI8B9kooBGixnbRsJfoHUX9sWP+lp50=; TASession=V2ID.5195B334147449498569EDD13A4B02EF*SQ.67*LS.DemandLoadAjax*GR.16*TCPAR.39*TBR.24*EXEX.49*ABTR.58*PHTB.54*FS.92*CPU.39*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*TRA.false*LD.16643865*EAU._; TAUD=LA-1632392065409-1*HDD-1-2021_10_03.2021_10_04*RDD-1-2021_09_23*ARDD-125298-2021_10_03.2021_10_04*HD-125735-2021_10_03.2021_10_04.187427*G-125736-2.1.187427.*LD-70760376-2021.10.3.2021.10.4*LG-70760382-2.1.T.; __vt=MdFPIbqr-dGl-wZ5ABQCIf6-ytF7QiW7ovfhqc-AvRg_mLG7WUEbxiqVzEBkSPoQGxMnsI234ys-7aIDnyXnCIDIkuqQAMunSihmRS1gYi6MKVnPZuqCgFAeGwIr21hGSt_axjZzADQDp-BjSiu580xIew',
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
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"详情页请求失败")
    return response


def parse_detail_info(content):
    html = etree.HTML(content.text, etree.HTMLParser())
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
    info = {
        'total_value': total_value,
        'location_value': location_value,
        'cleanliness_value': cleanliness_value,
        'service_value': service_value,
        'value_value': value_value,
        'stars': stars,
    }
    # print(info)
    return info


def main(page_number):
    for info in parse_hotel_info(get_hotel_html(page_number)):
        global writer
        writer.writerow(info)


if __name__ == '__main__':
    # url = "https://www.tripadvisor.com/Hotels-g187427-Spain-Hotels.html"
    start_time = time.time()
    page_numbers = [i for i in range(56)]
    csv_header = ['hotel_id', 'hotel_name', 'hotel_url', 'reviews', 'total_value',
              'location_value', 'cleanliness_value', 'service_value', 'value_value', 'stars']
    pool = ThreadPool()
    with open('hotel_detail_new_another.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, csv_header)
        writer.writeheader()
        pool.map(main, page_numbers)
        # pool.join()
        # pool.close()
    print(f"共耗时{time.time() - start_time} seconds")

    # parse_hotel_info(get_hotel_html(url, 0))