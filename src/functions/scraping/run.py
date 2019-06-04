#!/usr/bin/env python3

import requests
import json
from lxml import html
import re
import os


def run(_event, _context):
    print(_event)
    response = main(_event)
    print(response)
    return {"statusCode": 201,
            "body": json.dumps(response)}


def main(_event):
    rule_name = get_rule_name(_event)
    print(rule_name)
    groups_id = get_groups_by_rule_name(rule_name)
    groups_id = [151]
    print(groups_id)
    products  = get_products_by_group_id(groups_id)
    print(products)
    data_to_request_prices = price_insert_object_mount(products)
    print(data_to_request_prices)
    response_insert_prices = insert_prices(data_to_request_prices)
    return response_insert_prices


def get_rule_name(_event):
    resources = _event['resources']
    return get_rule_name_by_resource(resources)


def get_rule_name_by_resource(_resources):
    return re.search(r"/.+", _resources[0]).group()\
        .replace('/', '')


def price_to_float(_value):
    if _value == "":
        _value = 0
    else:
        _value = re.search("\d.+", _value).group()
        _value = _value.replace(".","")
        _value = _value.replace(",",".")
        _value = float(_value)
    return _value

def get_products_by_group_id(_groups_id):
    products = []

    for _ in _groups_id:
        group_id=_
        product_list = get_product_by_group_id(group_id)
        print(product_list)

        for _ in product_list:
            print(_)
            price = get_price(_["link"],_["tag"])
            print(price)
            _['price'] = price_to_float(price)
            print(_['price'])
            products.append(_)

    return products


def price_insert_object_mount(_products):
    items = []

    for _ in _products:
        items.append({
            "value": _["price"],
            "product_id": _["id_product"]
        })
    return items


def get_price(_url, _tag):
    page = requests.get(_url)
    print(page)
    tree = html.fromstring(page.content)
    print(tree)
    price = tree.xpath(get_xpath_to_tag(_tag))
    return price[0]


def get_product_by_group_id(_group_id):
    url = "{url}/products/list?groupId={group_id}"\
        .format(url=os.environ["TRACKING_API"], group_id=_group_id)
    headers = {
        "x-api-key": os.environ["X_API_KEY_TRACKING_API"],
        "Content-Type": "application/json",
    }
    return (requests.get(url, headers=headers)).json()


def get_groups_by_rule_name(_rule_name):
    url = "{url}/monitoring/rules?ruleName={rule_name}"\
        .format(url=os.environ["TRACKING_API"], rule_name=_rule_name)
    headers = {
        "x-api-key": os.environ["X_API_KEY_TRACKING_API"],
        "Content-Type": "application/json",
    }
    return (requests.get(url, headers=headers)).json()


def insert_prices(_prices):
    url = "{url}/prices"\
        .format(url=os.environ["TRACKING_API"])
    headers = {
        "x-api-key": os.environ["X_API_KEY_TRACKING_API"],
        "Content-Type": "application/json",
    }
    return (requests.post(url, data=json.dumps(_prices), headers=headers)).json()


def get_xpath_to_tag(_tag):
    _tag = _tag.replace('.', ' ')
    print(_tag)
    _tag = _tag.replace('//', '/')
    tag_group = re.search("<.+?>", _tag).group()
    tag_name = re.search(r"<(\w+)(\s)", tag_group).group().replace("<", "").replace(" ", "")
    atribute = re.search(r"(\w+)\=.+?'", tag_group).group()
    return "//" + tag_name + "[@" + atribute + "]/text()"

