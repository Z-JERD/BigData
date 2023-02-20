import time
import requests
from lxpy import copy_headers_dict
import pandas as pd

list_url = []
list_response = []
list_data = []


def make_url():
    i = 0
    while i <= 6000:
        url = f'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100:90&action=&start={i}&limit=20'
        list_url.append(url)
        i += 20
    return list_url


def get_url(list_url):
    for i in list_url:
        url = i
        headers = copy_headers_dict(
            '''
            Accept: */*
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
        Connection: keep-alive
        Cookie: viewed="26981817"; bid=QSKM9Yjr-Sg; gr_user_id=a025bf74-3347-4c17-9141-7fc987a8e10e; ll="118254"; douban-fav-remind=1; __yadk_uid=Js7LqneLfDOKqURYHtamSGZzQK8rURo0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1676191710%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1676191772; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1676192319; _pk_id.100001.4cf6=58815857a710be0d.1665037605.6.1676192523.1674135268.
        Host: movie.douban.com
        Referer: https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85%E7%89%87&type=11&interval_id=100:90&action=
        sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        Sec-Fetch-Dest: empty
        Sec-Fetch-Mode: cors
        Sec-Fetch-Site: same-origin
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41
        X-Requested-With: XMLHttpRequest
            '''
        )
        response = requests.get(url, headers=headers)
        res = response.json()
        list_response.append(res)
    return list_response


def get_data(list_response):
    rank = []
    title = []
    regions = []
    release_date = []
    vote_count = []
    score = []
    actors = []
    actor_count = []
    types = []

    for j in list_response:
        for i in j:
            rank.append(i['rank'])  # 排名
            title.append(i['title'])  # 标题
            regions.append(i['regions'])  # 地区
            release_date.append(i['release_date'])  # 播放时间
            vote_count.append(i['vote_count'])  # 投票人数
            score.append(i['score'])  # 评分
            actors.append(i['actors'])  # 演员
            actor_count.append(i['actor_count'])  # 演员人数
            types.append(i['types'])  # 电影类型

    for m in [rank, title, regions, release_date, vote_count, score, actors, actor_count, types]:
        list_data.append(m)
    return list_data


def save_data(list_data):
    data = pd.DataFrame({'排名': list_data[0], '电影标题': list_data[1], '地区': list_data[2],
                         '播放时间': list_data[3], '投票人数': list_data[4], '评分': list_data[5],
                         '演员': list_data[6], '演员人数': list_data[7], '电影类型': list_data[8]})
    data.to_excel("豆瓣评分数据.xlsx", index=False)
    print("爬取成功")


if __name__ == '__main__':
    start = time.time()
    make_url()
    get_url(list_url)
    get_data(list_response)
    save_data(list_data)
    end = time.time()
    print(f"一共用时{end - start}秒")
