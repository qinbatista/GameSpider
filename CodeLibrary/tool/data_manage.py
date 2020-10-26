import json
import os
import xlsxwriter
from collections import defaultdict
STYLES = {
    'c': {'border': 1, 'align': 'center'},
    's': {'border': 1, 'bg_color': 'yellow', 'align': 'center'},
    'e': {'border': 1, 'bg_color': 'green', 'align': 'center'}
}


def manage(path, data, excel=False):
    os.mkdir(path)
    cgd, gcd = build_data(data)
    save_json(f'{path}/channel_game.json', cgd)
    save_json(f'{path}/game_channel.json', gcd)
    not excel or save_excel(f'{path}/data.xls', cgd)


def build_data(data):
    cgd, gcd = defaultdict(dict), defaultdict(dict)
    for d in data:
        cgd[d[0]][d[1]] = {'find_url': d[2], 'exist': d[3], 'url': d[4]}
        gcd[d[1]][d[0]] = {'find_url': d[2], 'exist': d[3], 'url': d[4]}
    return cgd, gcd


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as w:
        json.dump(data, w, ensure_ascii=False, indent=4)


def read_json(path):
    return json.load(open(path, 'r', encoding='utf-8'))


def save_excel(path, data):
    workbook = xlsxwriter.Workbook(path)  # 创建一个excel文件
    sheet1 = workbook.add_worksheet(name="查询结果")
    sheet1.set_column(0, 1, 10)
    sheet1.set_column(2, 2, 80)
    sheet1.set_column(4, 4, 40)
    c = workbook.add_format(STYLES['c'])  # 普通样式
    s = workbook.add_format(STYLES['s'])  # 特殊样式
    e = workbook.add_format(STYLES['e'])  # 存在游戏的样式
    for x, k in enumerate(data[0].keys()):
        sheet1.write(0, x, k, c)
    for y, d in enumerate(data):
        for x, v in enumerate(d.values()):
            sheet1.write(y + 1, x, v if x != 3 else ("✔" if v else "✖"),
                         s if x == 4 and isinstance(v, bool) else (
                             e if x == 3 and v else c))
    workbook.close()
