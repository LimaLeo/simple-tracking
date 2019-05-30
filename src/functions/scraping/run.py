#!/usr/bin/env python3

import requests
import json
from lxml import html
import re
import os

def run(_event, _context):
    prices = []
    group_id=136
    data = get_data(group_id)
    for _ in data:
        prices.append(get_price(_["link"],_["tag"]))
    return {"statusCode": 201,
            "body": json.dumps(prices)}


def get_price(_url, _tag):
    page = requests.get(_url)
    tree = html.fromstring(page.content)
    price = tree.xpath(get_xpath_to_tag(_tag))
    return price[0]


def get_data(_group_id):
    url = "{url}/products/list?groupId={group_id}"\
        .format(url=os.environ["TRACKING_API"], group_id=_group_id)
    headers = {
        "x-api-key": os.environ["X_API_KEY_TRACKING_API"],
        "Content-Type": "application/json",
    }
    return (requests.get(url, headers=headers)).json()


def get_xpath_to_tag(_tag):
    tag_group = re.search("<.+?>", _tag).group()
    tag_name = re.search(r"<(\w+)(\s)", tag_group).group().replace("<", "").replace(" ", "")
    atribute = re.search(r"(\w+)\=.+?'", tag_group).group()
    return "//" + tag_name + "[@" + atribute + "]/text()"

