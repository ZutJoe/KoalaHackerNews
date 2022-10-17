import os
import re
import json
import itertools
import dataclasses
from dataclasses import dataclass

from typing import Iterator

import requests


os.environ["NO_PROXY"] = "bilibili.com"

HEADERS = {
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


def get_aids() -> Iterator[int]:
    """
    获取视频合集内视频的av号

    :return: 合集内每个视频的av号
    """
    for page_num in itertools.count(1):
        params = {
            'mid': '489667127',
            'season_id': '249279',
            'sort_reverse': 'false',
            'page_num': str(page_num),
            'page_size': '30',
        }
        response = requests.get(
            'https://api.bilibili.com/x/polymer/space/seasons_archives_list',
            params=params,
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        aids = data['data']['aids']
        if len(aids) == 0:
            break

        for aid in aids:
            yield aid


@dataclass(frozen=True)
class CommentData:
    aid: int  # 视频av号
    top_comment: str | None  # 置顶评论内容，可能不存在


def get_comment_data() -> Iterator[CommentData]:
    """
    对每页获取到的评论进行处理，获取置顶评论
    """
    base_url = 'http://api.bilibili.com/x/v2/reply/main'

    for aid in get_aids():
        params = {
            'type': 1,
            'oid': aid,
        }
        response = requests.get(
            url=base_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        comment_data = response.json()

        top_comment_data = comment_data['data']['top']['upper']
        if top_comment_data is None:
            yield CommentData(aid, None)
        else:
            yield CommentData(aid, top_comment_data['content']['message'])


@dataclass(frozen=True)
class VideoTime:
    minutes: int
    seconds: int


@dataclass
class HackerNewsItems:
    times: list[VideoTime]
    introduces: list[str]
    links: list[str | list[str]]

    @classmethod
    def from_dict(cls, d: dict) -> 'HackerNewsItems':
        return HackerNewsItems(
            [VideoTime(**time) for time in d['times']],
            d['introduces'],
            d['links'],
        )


def _parse_time_and_intro(
    line: str,
    matches: list[re.Match],
    times: list[VideoTime],
    introduces: list[str],
) -> None:
    """解析时间和简介"""
    # 一行有可能有不止一个时间，如 https://b23.tv/av1497344798
    for match, match_next in itertools.pairwise(matches):
        times.append(VideoTime(int(match[1]), int(match[2])))
        intro = line[match.end():match_next.start()].strip()
        introduces.append(intro.replace("|", "｜"))

    match = matches[-1]
    times.append(VideoTime(int(match[1]), int(match[2])))
    intro = line[match.end():].strip()
    introduces.append(intro.replace("|", "｜"))


def parse_top_comment(message: str | None) -> HackerNewsItems:
    """
    解析置顶评论，获得每个条目的时间轴、简介、以及链接
    """
    times: list[VideoTime] = []
    introduces: list[str] = []
    links: list[str | list[str]] = []

    if message is None:
        message = ""

    # 一个简单的状态机，解析什么内容取决于当前的状态 state
    state: str = '开始'
    for line in message.splitlines():

        if state == '开始':
            match = re.search(r'时间轴', line)
            if match is None:
                continue
            line = line[match.end():]
            state = '时间轴'

        if state == '时间轴':
            matches = list(re.finditer(r'(\d{1,}):(\d{2})', line, re.ASCII))
            if len(matches) > 0:
                _parse_time_and_intro(line, matches, times, introduces)
                continue

            # 这一行里没有找到时间，尝试寻找“链接”二字
            match = re.search(r'链接', line)
            if match is None:
                continue
            line = line[match.end():]
            state = '链接'

        if state == '链接':
            line_links: list[str] = []
            # 双引号、空格、左右尖括号、竖线一定不会出现在 URL 中
            for match in re.finditer(r'(https?://[^\s"<>|]+)', line, re.ASCII):
                line_links.append(match.group())

            # 一行里如果有多个链接，那就是同一个条目的链接，如：
            # https://b23.tv/av346450481
            if len(line_links) <= 1:
                links.extend(line_links)
            else:
                links.append(line_links)

    return HackerNewsItems(times, introduces, links)


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
    f.write('b站up主[Koala聊开源](https://space.bilibili.com/489667127)的《hacker news 周报》[合集](https://space.bilibili.com/489667127/channel/collectiondetail?sid=249279)的内容总结 \n')
    f.write('\n')
get_commont_data()
parse_top_commont()

