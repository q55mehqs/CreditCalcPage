# -*- coding: utf-8 -*-
from flask import Flask, render_template
from json import loads

app = Flask(__name__)
with open("snctCredit/jugyoList_17s_linear.json", "r", encoding="utf-8") as f:
    items_class_sort = loads(f.read())


def class_jugyo_data(course_class_list):
    items = []
    for _class in course_class_list:
        items.append(items_class_sort[_class])

    select_list = [[item for item in class_items if not item["必修"]] for class_items in items]
    must_list = [[item for item in class_items if item["必修"]] for class_items in items]

    return must_list, select_list


def must_count(must_list):
    must_general = 0
    must_special = 0
    must_gakushu = 0
    for must_class_list in must_list:
        for must_credit in must_class_list:
            if must_credit["専門"]:
                must_special += must_credit["単位数"]
            else:
                must_general += must_credit["単位数"]

            if must_credit["学修"]:
                must_gakushu += must_credit["単位数"]

    return must_general, must_special, must_gakushu


@app.route('/')
def index():
    must_list, select_list = class_jugyo_data(["1-1", "IS2", "IS3", "IS4", "IS5"])
    must_general, must_special, must_gakushu = must_count(must_list)

    return render_template('./main.html', select_credits=select_list, must_credits=must_list,
                           must_general=must_general, must_special=must_special, must_gakushu=must_gakushu,
                           course_name="IS", title="選択計算機 IS")


@app.route('/ie')
def ie_index():
    must_list, select_list = class_jugyo_data(["1-1", "IE2", "IE3", "IE4", "IE5"])
    must_general, must_special, must_gakushu = must_count(must_list)

    return render_template('./main.html', select_credits=select_list, must_credits=must_list,
                           must_general=must_general, must_special=must_special, must_gakushu=must_gakushu,
                           course_name="IE", title="選択計算機 IE")


@app.route('/it')
def it_index():
    must_list, select_list = class_jugyo_data(["1-1", "IT2", "IT3", "IT4", "IT5"])
    must_general, must_special, must_gakushu = must_count(must_list)

    return render_template('./main.html', select_credits=select_list, must_credits=must_list,
                           must_general=must_general, must_special=must_special, must_gakushu=must_gakushu,
                           course_name="IT", title="選択計算機 IE")


if __name__ == '__main__':
    app.run()