import os
import re
import sys
import json
import itertools
import dataclasses
import dominate
from dataclasses import dataclass
from dominate import tags
from dominate.tags import *

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


def get_top_comment(aid: int) -> str | None:
    """
    获取视频的置顶评论，如果没有置顶评论则返回 None
    """
    base_url = 'http://api.bilibili.com/x/v2/reply/main'

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

        # 如果没有置顶评论则查看最上面的一条评论
        if comment_data['data']['replies'][0]['member']['mid'] == '489667127':
            return comment_data['data']['replies'][0]['content']['message']
        else:
            return None
            
    else:
        return top_comment_data['content']['message']


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


@dataclass(kw_only=True)
class VideoInfo:
    aid: int
    hn_items: HackerNewsItems

    @classmethod
    def from_dict(cls, d: dict) -> 'VideoInfo':
        return VideoInfo(
            aid = d['aid'],
            hn_items = HackerNewsItems.from_dict(d['hn_items']),
        )


def load_data_json() -> list[VideoInfo]:
    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)

    return [VideoInfo.from_dict(video_info) for video_info in data]


def save_data_json(video_info_list: list[VideoInfo]) -> None:
    data = [dataclasses.asdict(video_info) for video_info in video_info_list]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')  # 为文本文件添加行尾换行符


def update_data_json() -> list[VideoInfo]:
    """
    更新最新视频数据，解析后保存到 data.json
    """
    try:
        video_infos = load_data_json()
    except FileNotFoundError:
        print("没有找到 data.json 文件，将自动重新获取完整数据", file=sys.stderr)
        video_infos = []

    video_info_dict = {video_info.aid: video_info for video_info in video_infos}
    new_video_infos: list[VideoInfo] = []

    for aid in get_aids():
        # 已经保存在 data.json 中的视频，无需重新获取一遍
        video_info = video_info_dict.get(aid)
        if video_info is None:
            video_info = VideoInfo(
                aid=aid,
                hn_items=parse_top_comment(get_top_comment(aid)),
            )
        new_video_infos.append(video_info)

    save_data_json(new_video_infos)
    return new_video_infos


def generate_md_table(video_info: VideoInfo) -> list[str]:
    """
    把解析之后的单个视频置顶评论转换成 markdown 表格形式
    """
    aid = video_info.aid
    times = video_info.hn_items.times
    introduces = video_info.hn_items.introduces
    links = video_info.hn_items.links
    video_url = f'https://www.bilibili.com/video/av{aid}'

    readme: list[str] = []

    readme.append(
        '\n'
        f'## [视频链接]({video_url})\n'
        '\n'
        '|时间轴|简介|链接|\n'
        '|:--:|:--:|:--:|\n'
    )

    time: VideoTime | None
    intro: str | None
    link: str | list[str] | None
    for time, intro, link in itertools.zip_longest(times, introduces, links):
        if time is None:
            time_str = ' '
        else:
            m = time.minutes
            s = time.seconds
            time_str = f'[{m:02d}:{s:02d}]'  f'({video_url}?t={m*60 + s})'

        intro_str = intro.replace('|', '｜') if intro else ' '

        if link is None:
            link_str = ' '
        elif isinstance(link, list):
            link_str = '<br>'.join(link)
        else:
            link_str = link

        readme.append(f'|{time_str}|{intro_str}|{link_str}|\n')

    return readme


def write_md(video_infos: list[VideoInfo]) -> None:
    readme: list[str] = []
    readme.append(
        '# Koala_hacker_news \n'
        '\n'
        'b站up主[Koala聊开源](https://space.bilibili.com/489667127)'
        '的《hacker news 周报》[合集]'
        '(https://space.bilibili.com/489667127/channel/collectiondetail?sid=249279)'
        '的内容总结 \n'
    )
    for video_info in video_infos:
        readme.extend(generate_md_table(video_info))

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("".join(readme))


def generate_html_table(video_info: VideoInfo) -> tags.div:
    """
    把解析之后的单个视频置顶评论转换成 html 表格形式
    """
    aid = video_info.aid
    times = video_info.hn_items.times
    introduces = video_info.hn_items.introduces
    links = video_info.hn_items.links
    video_url = f'https://www.bilibili.com/video/av{aid}'

    divv: tags.div = div()
    divv.add(h5(a('视频链接', href=f'{video_url}')))

    tablee: tags.table = divv.add(table(cls='table table-hover text-center align-middle'))
    trr = tr()
    trr.add(th('时间轴', scope='col', cls='col-1'))
    trr.add(th('简介', scope='col', cls='col-2'))
    trr.add(th('链接', scope='col', cls='col-2'))
    tablee.add(thead(trr)) 

    time: VideoTime | None
    intro: str | None
    link: str | list[str] | None
    with tablee.add(tbody()) as tbodyy:
        for time, intro, link in itertools.zip_longest(times, introduces, links):
            trr = tr()
            td_time = td()
            td_link = td()

            if time is None:
                td_time.add(a(''))
            else:
                m = time.minutes
                s = time.seconds
                td_time.add(a(f'{m:02d}:{s:02d}', href=f'{video_url}?t={m*60 + s}'))
            
            intro = intro.replace('|', '｜') if intro else ' '
            td_intro = td(intro)

            if link is None:
                td_link.add(a(''))
            elif isinstance(link, list):
                for l in link:
                    td_link.add(a(f'{l}', href=f'{l}'))
            else:
                td_link.add(a(f'{link}', href=f'{link}'))

            trr.add(td_time)
            trr.add(td_intro)
            trr.add(td_link)
            tbodyy.add(trr)

    divv.add(br())
    return divv


def write_html(video_infos: list[VideoInfo]) -> None:
    doc = dominate.document(title='Koala hacker news')
    with doc.head:
        meta(
            charset='utf-8', 
            name='viewport', 
            content='width=device-width, initial-scale=1'
        )
        link(
            href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css',
            rel='stylesheet',
            integrity='sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi',
            crossorigin='anonymous'
        )
        style('a {text-decoration: none}')
    
    doc.body['cls'] = 'bg-light'
    with doc:
        with div(cls='shadow p-3 mt-1 rounded mx-auto bg-light', style='width: 70%') as content:
            h1('Koala hacker news')
            br()
    
        for video_info in video_infos:
            content.add(generate_html_table(video_info))
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write("".join(doc.render()))


def main() -> None:
    video_infos = update_data_json()
    write_md(video_infos)
    write_html(video_infos)


if __name__ == '__main__':
    main()
