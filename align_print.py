#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
字符串左对齐格式化输出

借鉴自 urwid 的解决方案

"""

__author__ = 'xylx'

# 获取字符串字节数
def get_str_width(string):
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
    width = 0
    for each in string:
        if ord(each) == 0xe or ord(each) == 0xf:
            continue
        elif ord(each) <= 1114109:
            for num, wid in widths:
                if ord(each) <= num:
                    each_width = wid
                    width += each_width
                    break
            continue

        else:
            each_width = 1
        width += each_width

    if string.encode('UTF-8').isalpha():
        width = width + 1

    return width


# 字符串按指定宽度对齐
def align_string(string, width):
    string_width = get_str_width(string)
    if width > string_width:
        return string + ' ' * (width - string_width)
    else:
        return string


if __name__ == '__main__':

    res = [{
        'date': '2014-10-20',
        'name': 'ha哈哈',
        'info': 'sdfs<>《》==--k翻到发光的'
    }, {
        'date': '2014-10-21',
        'name': 'ha哈gf哈',
        'info': 'sdfs<>《》==--kko  翻到翻到的'
    }, {
        'date': '2014-10-20',
        'name': 'ha哈',
        'info': 'sdfs<>--kko  翻到翻到发光的'
    }, {
        'date': '2014-1-1',
        'name': 'h哈',
        'info': 'sdfs<>光的'
    }, {
        'date': '2014-01-01',
        'name': 'ha哈哈',
        'info': 'sdfs<>《》==--kko  翻到翻到发光的'
    }]

    for r in res:
        print(align_string(r['date'], 20), align_string(r['name'], 30), align_string(r['info'], 50))
