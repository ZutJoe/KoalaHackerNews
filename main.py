import os
import re
import json
import requests

os.environ["NO_PROXY"] = "bilibili.com"

headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com/489667127/channel/collectiondetail?sid=249279',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37',
}

def get_data() -> list[object]:
    """
    获取视频集合的数据，如果当前页没有视频数据则退出循环

    :return: 每一页的所有视频信息
    """

    page_num = 0
    while True:
        page_num += 1
        bv_list = []
        params = {
            'mid': '489667127',
            'season_id': '249279',
            'sort_reverse': 'false',
            'page_num': str(page_num),
            'page_size': '30',
        }

        response = requests.get('https://api.bilibili.com/x/polymer/space/seasons_archives_list', params=params, headers=headers)
        data = response.json()
        if len(data['data']['archives']) == 0:
            break

        print(len(data['data']['archives']))
        for obj in data['data']['archives']:
            bv_list.append(obj)

        yield bv_list


def get_commont_data() -> None:
    """
    对每页获取到的评论进行处理，获取置顶评论，格式化数据并将相应视频bv号添加到json数据中
    """

    base_url = 'http://api.bilibili.com/x/v2/reply/main'
    with open('data.json', 'a+', encoding='utf-8') as f:
        f.write('[')
    for urls in get_data():
        for url in urls:
            data = json.loads(json.dumps(url))
            params = {
                'type': 1,
                'oid': data['aid']
            }
            commont_data = requests.get(url=base_url, params=params, headers=headers)
            commont_data = commont_data.json()
            with open('data.json', 'a+', encoding='utf-8') as f:
                if (top_commont_data := commont_data['data']['top']['upper']) is not None:
                    content = json.dumps(top_commont_data['content'], ensure_ascii=False)
                    content = content[:-1]
                    content += ', "bvid": "' + data['bvid'] + '"}'
                    f.write(content)
                else:
                    f.write('{"aid": ' + str(data['aid']) + '}')
                f.write(',')
    with open('data.json', 'rb+') as f:
        f.seek(-1, os.SEEK_END)
        f.truncate()
        f.write(b']\n')


def parse_top_commont() -> None:
    """
    对所有的置顶评论进行解析
    """

    with open('data.json', 'r', encoding='utf-8') as f:
        top_commont = json.load(f)
        for i in range(0, len(top_commont)):
            if (msg := top_commont[i].get('message')) is not None:
                times = []
                introduces = []
                links = []
                for content in msg.split('\n'):
                    if (time := re.search(r'^\d{2}:\d{2}', content.strip()[:5])) != None or re.search(r'[|｜]', content.strip()) != None:
                        if time == None:
                            introduces.append(content.strip())
                            continue
                        times.append(time.group())
                        introduces.append(content.strip()[6:].strip().replace('|', '｜'))
                    elif re.search(r'时间轴', content) != None or re.search(r'链接', content) != None:
                        continue
                    elif re.search(r'https', content) != None:
                        links.append(content.strip())
                    else:
                        continue
                
                bvid = top_commont[i]['bvid']
                write_md(times, introduces, links, bvid)


def write_md(times: list[str], introduces: list[str], links: list[str], bvid: str) -> None:
    """
    对解析之后的单个视频置顶评论写入到md文件当中

    :param times: 解析出来的时间数据
    :param introduces: 解析出来的简介
    :param links: 解析出来的链接
    :param bvid: 该视频的bvid
    """
    
    vedio_url = f'https://www.bilibili.com/video/{bvid}'
    with open('README.md', 'a+', encoding='utf-8') as f:
        f.write(f'## [视频链接]({vedio_url})\n\n')
        f.write('|时间轴|简介|链接|\n')
        f.write('|:--:|:--:|:--:|\n')
        for i in range(max(len(times), len(introduces), len(links))):
            if i < len(times):
                time = times[i]
                m = int(time.split(':')[0])
                s = int(time.split(':')[1])
                f.write(f'|[{time}]({vedio_url}?t={m*60 + s})|')
            else:
                f.write('| |')

            if i < len(introduces):
                f.write(introduces[i] + '|')
            else:
                f.write(' |')

            if i < len(links):
                f.write(links[i] + '|\n')
            else:
                f.write(' |\n')


os.remove('data.json')
os.remove('README.md')
with open('README.md', 'a+', encoding='utf-8') as f:
    f.write('# Koala_hacker_news \n\n')
    f.write('b站up主[Koala聊开源](https://space.bilibili.com/489667128)的《hacker news 周报》[合集](https://space.bilibili.com/489667127/channel/collectiondetail?sid=249279)的内容总结 \n')
    f.write('\n')
get_commont_data()
parse_top_commont()

