#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
字符串左对齐格式化输出
----借鉴自 urwid 的解决方案
"""

__author__ = 'xylx'

# 字符宽度表
widths = [
    (126, 1), (159, 0), (687, 1), (710, 0), (711, 1),
    (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
    (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1),
    (8426, 0), (9000, 1), (9002, 2), (11021, 1), (12350, 2),
    (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1),
    (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]


# 获取字符宽度
def get_width(o):
    global widths
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if ord(o) <= num:
            return wid
    return 1


# 返回以指定宽度右侧补齐空格的字符串，超出指定宽度将原样返回
def align_left(string, width):
    w = 0
    for s in string:
        w += get_width(s)
    delt = int(width) - w
    if delt >= 0:
        return '' + string + ' ' * delt
    else:
        return string


# 返回以指定宽度右侧补齐空格的字符串，超出指定宽度将丢弃多余部分
def align_left_cut(string, width):
    w = 0
    for i, s in enumerate(string):
        ws = get_width(s)
        # 超出指定宽度丢弃多余部分
        if w + ws > int(width):
            return string[:i] + ' ' * (int(width) - w)
        else:
            w += ws
    return string + ' ' * (int(width) - w)


if __name__ == '__main__':

    res = [{
        'date': '2014-10-20',
        'name': 'ha哈哈gfgggfgf发的地方发呆发呆发呆',
        'info': 'sdfs<>《》==--k翻到发光的'
    }, {
        'date': '2014-10-21',
        'name': 'ha哈哈',
        'info': 'sdfs<>《》==--kko  翻到翻到的'
    }, {
        'date': '2014-10-20',
        'name': 'ha哈哈短发短发的',
        'info': 'sdfs<>--kko  翻到翻到发光的'
    }, {
        'date': '2014-1-1',
        'name': 'ha哈哈递归',
        'info': 'sdfs<>光的'
    }, {
        'date': '2014-01-01',
        'name': 'ha哈哈5353535短发更多',
        'info': 'sdfs<>《》==--kko  翻到翻到发光的'
    }]

    for r in res:
        print(align_left_cut(r['date'], 20), align_left_cut(r['name'], 10), align_left_cut(r['info'], 10))
