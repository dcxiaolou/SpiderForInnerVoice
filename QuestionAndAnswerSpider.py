import json
import os

import requests
from requests import RequestException
import re
from config import *

# # 获取问答模块数据 问题 + 回答

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
        '<li>.*?class="user".*?class="common-a" target="_blank" href="(.*?)">.*?<span>(.*?)</span>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'url': 'http://www.xinli001.com' + item[0],
            'title': item[1].strip()  # 去除字符串空格
        }
    return items


def get_detail_question(url):
    html = get_page_html(url)
    # 获取问题
    pattern = re.compile(
        '<div class="content">.*?class="common-a".*?<img src="(.*?)" />.*?<strong>(.*?)</strong>.*?class="read-capacity".*?<span>(.*?)</span>.*?<a>(.*?)</a></span>.*?class="text">(.*?)</p>.*?class="label detail-tag">(.*?)</ul>',
        re.S)
    question = re.findall(pattern, html)

    pattern = re.compile(
        '<li class=".*?">(.*?)</li>',
        re.S)

    yield {
        'question_user_img': question[0][0],  # 提问者的头像
        'question_answer_num': question[0][1],  # 共有多少个回答
        'question_push_time': question[0][2],  # 问题提出的时间
        'question_reader_num': question[0][3],  # 有多少人看了该问题
        'question_content': question[0][4],  # 问题的具体内容
        'question_tag': re.findall(pattern, question[0][5])  # 问题的类型
    }


def get_detail_answer(url):
    html = get_page_html(url)
    # 获取回答
    pattern = re.compile(
        '.*?class="user".*?<img src="(.*?)" />.*?class="username">(.*?)</span>.*?class="text">(.*?)</p>.*?class="like-light">.*?<font>(.*?)</font></a>.*?class="comment_num">.*?<p>(.*?)</p>',
        re.S)
    answer = re.findall(pattern, html)
    return answer

def save_to_json(result, fileUrl):
    with open(fileUrl, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
        f.close()

def main():
    count = 1
    for page in range(1, PAGEQUESTIONANDANSWER):
        html = get_page_html('http://www.xinli001.com/qa?page=' + str(page))
        # print(html)
        # 将文章内容保存到json文件
        fileUrl = os.getcwd()
        for item in parse_one_page(html):
            question = get_detail_question(item['url'])
            for q in question:
                save_to_json(q, fileUrl + '\\QuestionAndAnswer\\Question\\' + str(count) + '.json')
                print('save question ' + str(count) + '.json' + ' success')
                answer = get_detail_answer(item['url'])
                item = 1
                for a in answer:
                    result = {
                        'answer_user_img': a[0],  # 回答者的头像
                        'answer_user_name': a[1],  # 回答者的名称
                        'answer_content': a[2],  # 回答的具体内容
                        'answer_digg': a[3],  # 点赞数
                        'answer_push_time': a[4]  # 回答的发布时间
                    }
                    save_to_json(result, fileUrl + '\\QuestionAndAnswer\\Answer\\' + str(count) + '_' + str(item) + '.json')
                    print('save answer ' + str(count) + '_' + str(item) + '.json' + ' success')
                    item = item + 1
            count = count + 1


if __name__ == '__main__':
    main()
