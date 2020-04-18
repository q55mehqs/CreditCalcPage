# -*- coding: utf-8 -*-
from flask import Flask, render_template
from json import loads, dumps

from pprint import pprint

from typing import List, Tuple, Union, Dict


app = Flask(__name__)
with open("snctCredit/jugyoList_17s_linear.json", "r", encoding="utf-8") as f:
    items_class_sort = loads(f.read())


def as_dict(base_course: str) -> Dict[str, List[Dict[str, Union[str, bool, int]]]]:
    with open("snctCredit/jugyoList_AS_17s_linear.json", "r", encoding="utf-8") as f:
        items_as_sort = loads(f.read())
    with open("snctCredit/jugyoList_AS_base_linear.json", "r", encoding="utf-8") as f:
        items_base_sort = loads(f.read())
    items_as_sort["AS4"].extend(items_base_sort["%s4" % base_course])
    items_as_sort["AS5"].extend(items_base_sort["%s5" % base_course])

    return items_as_sort

def class_jugyo_data(course_class_list):
    items = []
    for _class in course_class_list:
        items.append(items_class_sort[_class])

    select_list = [[item for item in class_items if not item["必修"]] for class_items in items]
    must_list = [[item for item in class_items if item["必修"]] for class_items in items]

    return must_list, select_list


def as_jugyo_data(base_course: str):
    items = []
    base_class = ["1-1", "%s2" % base_course, "%s3" % base_course]
    must, select = class_jugyo_data(base_class)
    must.extend([[], []])
    select.extend([[], []])

    as_data = as_dict(base_course)

    items.append(as_data["AS4"])
    items.append(as_data["AS5"])

    i = 3
    for class_items in items:
        for item in class_items:
            if item["必修情報"] == "必修":
                must[i].append(item)
            else:
                select[i].append(item)
        i += 1

    return must, select


def must_count(must_list):
    pprint(must_list)
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

    return render_template('./main.html.jinja2', select_credits=select_list, must_credits=must_list,
                           must_general=must_general, must_special=must_special, must_gakushu=must_gakushu,
                           course_name="IS", title="選択計算機 IS")


@app.route('/ie')
def ie_index():
    must_list, select_list = class_jugyo_data(["1-1", "IE2", "IE3", "IE4", "IE5"])
    must_general, must_special, must_gakushu = must_count(must_list)

    return render_template('./main.html.jinja2', select_credits=select_list, must_credits=must_list,
                           must_general=must_general, must_special=must_special, must_gakushu=must_gakushu,
                           course_name="IE", title="選択計算機 IE")


@app.route('/it')
def it_index():
    must_list, select_list = class_jugyo_data(["1-1", "IT2", "IT3", "IT4", "IT5"])
    must_general, must_special, must_gakushu = must_count(must_list)

    return render_template('./main.html.jinja2', select_credits=select_list, must_credits=must_list,
                           must_general=must_general, must_special=must_special, must_gakushu=must_gakushu,
                           course_name="IT", title="選択計算機 IT")


@app.route('/as_is')
def as_is_index():
    must, select = as_jugyo_data("IS")
    must_gen, must_spe, must_gak = must_count(must)

    return render_template('./as_main.html.jinja2', title="選択計算機 AS(IS)", course_name="AS(IS)",
                           select_credits=select, must_credits=must,
                           must_general=must_gen, must_special=must_spe, must_gakushu=must_gak)


@app.route('/as_it')
def as_it_index():
    must, select = as_jugyo_data("IT")
    must_gen, must_spe, must_gak = must_count(must)

    return render_template('./as_main.html.jinja2', title="選択計算機 AS(IT)", course_name="AS(IT)",
                           select_credits=select, must_credits=must,
                           must_general=must_gen, must_special=must_spe, must_gakushu=must_gak)


@app.route('/as_ie')
def as_ie_index():
    must, select = as_jugyo_data("IE")
    must_gen, must_spe, must_gak = must_count(must)

    return render_template('./as_main.html.jinja2', title="選択計算機 AS(IE)", course_name="AS(IE)",
                           select_credits=select, must_credits=must,
                           must_general=must_gen, must_special=must_spe, must_gakushu=must_gak)


if __name__ == '__main__':
    app.run()