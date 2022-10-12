import requests

headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'buvid3=6F20F486-40C7-426B-AF1D-A987B123EF10185003infoc; rpdid=|(u)Y~ukkYJu0J\'uYu)|RmY~|; LIVE_BUVID=AUTO9616204633342486; video_page_version=v_old_home; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; fingerprint_s=5b6d239bd0bef78c27751fee31cbb320; buvid4=3FBB5645-FC55-1E31-438B-50B58A04414968561-022012015-3qW7PFZQ+ONHKz3jqZTfDQ%3D%3D; nostalgia_conf=-1; hit-dyn-v2=1; _uuid=E101C76FF-D26D-5E102-734E-2F77FAF1684F56908infoc; fingerprint3=d4e5aed0143b24edfba50fc3ac142151; blackside_state=0; buvid_fp_plain=undefined; DedeUserID=473647028; DedeUserID__ckMd5=39d47de2f545fc95; buvid_fp=8b4239572876f94c4699e37a7dceafa8; b_ut=5; go_old_video=1; SESSDATA=7e2ae271%2C1669906128%2Cd222d%2A61; bili_jct=84514007f3040c4b8a4780a029c8b4c0; sid=hty29hoq; fingerprint=79c1f0b659baca3a884ae8ea5e253394; b_nut=100; i-wanna-go-feeds=-1; CURRENT_QUALITY=64; bp_video_offset_473647028=715757678747451400; innersign=1; CURRENT_FNVAL=4048; b_lsid=F473378E_183C9F2B6E5; PVID=2',
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

params = {
    'mid': '489667127',
    'season_id': '249279',
    'sort_reverse': 'false',
    'page_num': '1',
    'page_size': '30',
}

response = requests.get('https://api.bilibili.com/x/polymer/space/seasons_archives_list', params=params, headers=headers)
print(response.json())