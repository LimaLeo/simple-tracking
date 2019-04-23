#!/usr/bin/env python3

import requests
import json
from lxml import html
import re


def run(_event, _context):
    prices = []
    data = get_data()
    for _ in data:
        prices.append(get_price(_['url'],_['tag']))
    return {'statusCode': 201,
            'body': json.dumps(prices)}


def get_price(_url, _tag):
    page = requests.get(_url)
    tree = html.fromstring(page.content)
    price = tree.xpath(get_xpath_to_tag(_tag))
    return price[0]


def get_data():
    data = [
        {
            'url': 'https://www.submarino.com.br/produto/134195747/game-days-gone-ps4?DCSext.recom=RR_category_page.rr1-CategoryTopSellers&nm_origem=rec_category_page.rr1-CategoryTopSellers&nm_ranking_rec=2',
            'tag': '<span class="sales-price main-offer__SalesPrice-sc-1oo1w8r-1 fiWaea TextUI-sc-1hrwx40-0 hbVZKK">R$ 179,99</span>'
        },
        {
            'url': 'https://www.americanas.com.br/produto/132733871/lavadora-de-roupas-brastemp-11kg-bwk11-branco?pfm_carac=Eletrodom%C3%A9sticos&pfm_index=0&pfm_page=category&pfm_pos=grid&pfm_type=vit_product_grid&sellerId',
            'tag': '<p class="sales-price buy-box-from-price__SalesPrice-sc-128pnyu-1 hQRdfE ParagraphUI-sc-15adr4q-0 hwhytb">R$ 1.349,99</p>'
        }
    ]
    return data


def get_xpath_to_tag(_tag):
    tag_group = re.search('<.+?>', _tag).group()
    tag_name = re.search(r'<(\w+)(\s)', tag_group).group().replace('<', '').replace(' ', '')
    atribute = re.search(r'(\w+)\=.+?"', tag_group).group()
    return '//' + tag_name + '[@' + atribute + ']/text()'

