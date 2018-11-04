import requests
from requests import RequestException
import re

import json

import os

from config import *

# 获取阅读模块数据 文章 + 评论

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


def get_page_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 获取课程介绍
def get_course_introduce(course_url):
    html = get_page_html(course_url)
    pattern = re.compile('<div class="class-detail-tab" data-slidenav-content="true">(.*?)<div class="recommend-list">',
                         re.S)
    introduce = re.findall(pattern, html)
    return introduce


def get_course_detail(url):
    html = get_page_html(url)
    # print(html)
    pattern = re.compile('"video_id":"(.*?)","is_video":(.*?),"', re.S)
    detail = re.findall(pattern, html)
    return detail

def save_to_json(result, fileUrl):
    with open(fileUrl, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
        f.close()

def main():
    html = get_page_html('http://m.xinli001.com/lesson/tagList?tag_name=free&page=1&size=20&lesson_type=normal')
    # print(html)
    pattern = re.compile('"id":"(.*?)"', re.S)
    course_id = re.findall(pattern, html)
    no = 1
    fileUrl = os.getcwd()
    for id in course_id:
        item = {}
        introduce = get_course_introduce('http://m.xinli001.com/lesson/' + id)
        item['introduce'] = introduce
        save_to_json(item, fileUrl + '\\Course\\introduce\\' + str(id) + '.json')
        print('course directory ' + str(id) + '.json')
        count = 1
        item = {}
        for detail in get_course_detail(
                'https://m.xinli001.com/lesson/getPeriodList?lesson_id=' + id + '&__from__=detail'):
            if detail[0] != '':
                url_1 = detail[0][:10]
                url_2 = detail[0][31:32]
                url_3 = detail[0][:33]
                # print(url_1 + '  ' + url_2 + '  ' + url_3)
                # https://plvod01.videocc.net/605ea32bee/1/605ea32beeff8e75d23d0b170f9fa071_1.mp3
                url = 'https://plvod01.videocc.net/' + url_1 + '/' + url_2 + '/' + url_3 + '1.mp3'
                item['media'] = url
                # print(id + '  ' + detail[0] + '  ' + url)
                # 将文章内容保存到json文件
                save_to_json(item, fileUrl + '\\Course\\detail\\' + str(id) + "_" + str(count) + '.json')
                print('course detail ' + str(id) + "_" + str(count) + '.json')
                count = count + 1

if __name__ == '__main__':
    main()
