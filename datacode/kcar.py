import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import pymysql
def get_res(i):
    url = 'https://www.kcar.com/search/api/getCarSearchWithCondition.do'
    data = {'car_kind': '전체',
            'price_tab_flag': 1,
            'v_sell_cl_cd': 'ALL',
            'limit': 60,
            'orderFlag': 'true',
            'orderby': 'n_order:desc',
            'v_trust_flag': 'A',
            'acmPageno': i}

    res = requests.get(url,data)
    return res

def get_info(res):
    desc = []
    # try:
    for i in range(0, 59):
        box = res.json()
        soup = box["DRCT"]['result']['rows']
        price = soup[i]['n_price']
        year = soup[i]['v_begin_year']
        color = soup[i]['v_exterior_colornm']
        location = soup[i]['v_center_region']
        color = soup[i]['v_exterior_colornm']
        fuel = soup[i]['v_fuel_typecd_name']
        brand = soup[i]['v_makenm']
        photo = soup[i]['v_middle_img']
        name = soup[i]['v_model_grp_nm']
        accident = soup[i]['v_rec_comment']
        model = soup[i]['v_class_headnm']
        trim = soup[i]['v_class_detailnm']
        km = soup[i]['n_mileage']
        link = 'https://www.kcar.com/'+soup[i]['v_car_url']
        desc.append({'brand': brand, 'name': name, 'model': model, 'trim':trim,'fuel': fuel, 'km': km,
                     'year': year, 'location': location, 'price': price, 'link':link,'photo':photo,'accident':accident,'color':color})
    # except:
    #     pass
    return desc



def get_all_k():
    information = []
    for i in range(134):
        res1 = get_res(i)
        information.append(get_info(res1))
    info = sum(information, [])

    return info

