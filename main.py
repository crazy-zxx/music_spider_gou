#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""酷狗音乐搜索下载"""

__author__ = 'xylx'

import align_print
import requests
import json
import time
import re
import execjs


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
}
cookie = 'ACK_SERVER_10011={"list"%3A[["fanxing.kugou.com"]%2C["sparefx2.kugou.com"]]}; ACK_SERVER_10014={"list"%3A[["service.fanxing.kugou.com"]%2C["servicefx2.kugou.com"]]}; ACK_SERVER_10020={"list"%3A[["fx.service.kugou.com"]%2C["fxservice1.kugou.com"]%2C["fxservice2.kugou.com"]]}; ACK_SERVER_10022={"list"%3A[["fx1.service.kugou.com"]%2C["fxservice3.kugou.com"]%2C["fx2.service.kugou.com"]%2C["fxservice4.kugou.com"]]}; ACK_SERVER_10023={"list"%3A[["service1.fanxing.kugou.com"]%2C["service3.fanxing.kugou.com"]%2C["service2.fanxing.kugou.com"]%2C["service4.fanxing.kugou.com"]]}; ACK_SERVER_10028={"list"%3A[["p1.fx.kgimg.com"]%2C["p3fx.service.kugou.com"]]}; ACK_SERVER_10029={"list"%3A[["p3.fx.kgimg.com"]%2C["p3fx.service.kugou.com"]]}; ACK_SERVER_10030={"list"%3A[["p3fx.kgimg.com"]%2C["p3fx.service.kugou.com"]]}; ACK_SERVER_10033={"list"%3A[["s3.fx.kgimg.com"]%2C["s3fx.kgimg.com"]]}; ACK_SERVER_10034={"list"%3A[["image.fanxing.kugou.com"]%2C["s3fx.kgimg.com"]]}; ACK_SERVER_10035={"list"%3A[["fxsong.kugou.com"]%2C["fxsong2.kugou.com"]%2C["fxsong3.kugou.com"]%2C["fxsong4.kugou.com"]]}; ACK_SERVER_10036={"list"%3A[["gateway.kugou.com"]%2C["gatewayretry.kugou.com"]]}; KuGooRandom=66501617588838439; kg_dfid=2T1heZ3FBhFk3We18X1VAP9Q; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid=eeeae79c51c3c2fd30b8c51262f1213c'


# 由js生成的的signature参数
def get_signature(text):
    with open("kugou.js", "r", encoding='utf-8') as f:
        js_str = f.read()
    if js_str is not None:
        js_obj = execjs.compile(js_str)
        return js_obj.call('faultylabs.MD5', text)
    return None


# 返回搜索url
def get_search_url(keyword):
    KEY_CODE = "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwtbitrate=0callback=callback123clienttime={time}clientver=2000dfid=-inputtype=0iscorrection=1isfuzzy=0keyword={keyword}mid={time}page=1pagesize=30platform=WebFilterprivilege_filter=0srcappid=2919tag=emuserid=-1uuid={time}NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    URL_SEARCH = "https://complexsearch.kugou.com/v2/search/song?callback=callback123&keyword={keyword}&page=1&pagesize=30&bitrate=0&isfuzzy=0&tag=em&inputtype=0&platform=WebFilter&userid=-1&clientver=2000&iscorrection=1&privilege_filter=0&srcappid=2919&clienttime={time}&mid={time}&uuid={time}&dfid=-&signature={signature}"
    millis = str(round(time.time() * 1000))
    p = KEY_CODE.format(time=millis, keyword=keyword)
    signature = get_signature(p)
    url = URL_SEARCH.format(keyword=keyword, time=millis, signature=signature)
    return url


# 格式化歌曲时长
def get_song_time(songtime):
    return str(int(songtime) // 60) + ':' + str(int(songtime) % 60)


# 按歌曲名称搜索，并返回搜索结果的list
def music_search():
    key = input('请输入搜索的歌名（无输入将退出）：')
    if key is None or key.strip() == '':
        exit(0)
    key = key.strip()

    url = get_search_url(key)
    response = requests.get(url=url, headers=headers)
    search_json = json.loads(response.text[12:-2].encode('utf-8'))
    data = search_json.get('data').get('lists')
    result = []
    for d in data:
        result.append({
            'name': re.sub(r'[<\\/em>]', '', d.get('FileName')),  # 歌曲名
            'album': d.get('AlbumName'),  # 歌曲专辑
            'artist': d.get('SingerName'),  # 歌手
            'songTimeMinutes': get_song_time(d.get('Duration')),  # 时长
            'FileHash': d.get('FileHash'),
            'AlbumID': d.get('AlbumID')
        })

    return result


# 格式化输出搜索到的歌曲信息
def music_show(result):
    if len(result) > 0:
        print('序号\t歌名\t\t\t\t\t\t\t\t\t\t\t专辑\t\t\t\t\t\t\t\t\t\t\t歌手\t\t\t\t\t时长')
        i = 0  # 计数
        for r in result:
            i += 1
            # 获取指定长度且末尾补齐空格的字符串
            mid = align_print.align_string(str(i), 4)
            name = align_print.align_string(r['name'], 50)
            album = align_print.align_string(r['album'], 50)
            artist = align_print.align_string(r['artist'], 20)
            song_time_minutes = align_print.align_string(r['songTimeMinutes'], 10)
            print(mid + ' ' + name + ' ' + album + ' ' + artist + ' ' + song_time_minutes)

        music_download(result)

    else:
        print('没有找到！')


# 从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies
def extract_cookies(cookie):
    cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookies


# 下载音乐
def music_download(result):
    select = input('输入下载的序号（0返回搜索；多个序号用逗号隔开）：')
    s_list = re.split(r'[,，]', select)

    try:
        for s in s_list:
            index = int(s.strip())
            if index == 0:
                return
            if index < 1 or index > len(result):
                raise ValueError()

            url = 'https://wwwapi.kugou.com/yy/index.php?'
            data = {
                'r': 'play/getdata',
                'hash': result[index - 1]['FileHash'],
                'album_id': result[index - 1]['AlbumID']
            }
            response = requests.get(url=url, params=data, headers=headers, cookies=extract_cookies(cookie))
            download_url = json.loads(response.text.encode('utf-8')).get('data').get('play_url')
            download_response = requests.get(url=download_url)
            with open(result[index - 1]['name'] + '.mp3', 'wb') as f:
                f.write(download_response.content)
            print(str(index) + ' 下载完成！')

    except ValueError as e:
        print('无效输入！')
        music_download(result)


if __name__ == "__main__":
    while True:
        result = music_search()
        music_show(result)
