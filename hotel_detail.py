import requests
from lxml import etree

import json


def get_html(url):
    headers = {
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
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"请求失败")
    return response


def parse_detail_info(content):
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
    info = {
        'total_value': total_value,
        'location_value': location_value,
        'cleanliness_value': cleanliness_value,
        'service_value': service_value,
        'value_value': value_value,
        'stars': stars,
        'reviews': reviews,
    }
    print(info)


if __name__ == '__main__':
    url = 'https://www.tripadvisor.com/Hotel_Review-g187514-d4719800-Reviews-Only_You_Boutique_Hotel_Madrid-Madrid.html'
    url1 = 'https://www.tripadvisor.com/Hotel_Review-g187497-d22861924-Reviews-Habitat_Apartments_Alaia-Barcelona_Catalonia.html'
    url2 = 'https://www.tripadvisor.com/Hotel_Review-g15690725-d6217896-Reviews-Globales_Playa_Estepona-Atalaya_Isdabe_Costa_del_Sol_Province_of_Malaga_Andalucia.html'
    response = get_html(url2)
    with open('detail.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    parse_detail_info(response)