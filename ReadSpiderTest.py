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


def parse_one_page(html):
    pattern = re.compile(
        '<div class="item">.*?<a target="_blank" href="(.*?)" >.*?<img src="(.*?)".*?class="title">(.*?)</a>.*?class="desc">(.*?)</p>.*?class="info">.*?<span>(.*?)</span>.*?class="date">(.*?)</span>.*?class="statistics">(.*?)</span>'
        , re.S)
    items = re.findall(pattern, html)
    # 文章链接  图片  标题  描述  作者  发布时间  阅读量
    for item in items:
        yield {
            'article_url': 'https:' + item[0],
            'image': item[1],
            'title': item[2],
            'describe': item[3],
            'author': item[4],
            'push_time': item[5],
            'count': item[6]
        }


def get_article_detail(url):
    html = get_page_html(url)

    article = []
    # 获取文章分类标签
    pattern = re.compile('<a data-tag=".*?>(.*?)</a>', re.S)
    tags = re.findall(pattern, html)
    tags_modify = []
    for tag in tags:
        tags_modify.append(tag.strip())
    # 获取点赞数
    pattern = re.compile('<div class="info">.*?<span class="like">(.*?)</span>', re.S)
    like = re.findall(pattern, html)
    # 获取文章内容
    pattern = re.compile('<div class="article-body-m">(.*?)<div id="copyright">', re.S)
    detail = re.findall(pattern, html)

    article.append(tags_modify)
    article.append(like)
    article.append(detail)

    return article


def get_article_common(url):
    html = get_page_html(url)
    # 评论者头像  评论者名称  评论内容  点赞数  评论发表时间
    pattern = re.compile(
        '<div class="comment-item">.*?<img src="(.*?)".*?/>.*?class="nickname">(.*?)：</span>.*?class="comment-text">(.*?)</span>.*?class="like-btn".*?><span>(.*?)</span>.*?class="right-bottom">.*?<span>(.*?)</span>',
        re.S)
    article_comment = re.findall(pattern, html)

    for common in article_comment:
        yield {
            'common_user_img': common[0],
            'common_user_name': common[1].strip(),
            'common_detail': common[2].strip(),
            'common_like': common[3],
            'common_push_time': common[4]
        }

def save_to_json(result, fileUrl):
    with open(fileUrl, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
        f.close()

def main():
    count = 1
    for tag in ARTICLE_CLASS:
        title = ARTICLE_CLASS[tag]
        print(title)
        url_1 = 'http://www.xinli001.com/info/tag_' + tag
        for page in range(1, PAGEREAD):
            url = url_1 + '?page=' + str(page)
            print(url)
            html = get_page_html(url_1)
            for item in parse_one_page(html):
                # print(item)
                article = get_article_detail(item['article_url'])
                # print(result)
                item['tag'] = article[0]
                item["like"] = article[1]
                item["article_detail"] = article[2]
                # 将文章内容保存到json文件
                fileUrl = os.getcwd()
                save_to_json(item, fileUrl + '\\Read\\Article\\' + str(tag) + "_" + str(count) + '.json')
                print('article ' + item['title'] + "   " + str(tag) + "_" + str(count) + '.json')
                num = 1
                for common in get_article_common('http://www.xinli001.com/ajax/article-comment-list.json?' + 'article_id=' + item['article_url'][30:] + '&page=1'):
                    # print(common)
                    save_to_json(common, fileUrl + '\\Read\\Common\\' + str(tag) + "_" + str(count) + "_" + str(num) + '.json')
                    print('common ' + common['common_user_name'] + '   ' + str(tag) + "_" + str(count) + "_" + str(num) + '.json')
                    num = num + 1
                count = count + 1
            url = url_1

if __name__ == '__main__':
    main()
