import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import pymysql
from sqlalchemy import create_engine
def color(c):
    color = []; choice = c
    color.append('Or.Color.%EA%B0%88%EB%8C%80%EC%83%89._.Color.%EC%B2%AD%EC%83%89._.Color.%EB%B9%A8%EA%B0%84%EC%83%89._.Color.%EC%A3%BC%ED%99%A9%EC%83%89._.Color.%ED%95%98%EB%8A%98%EC%83%89._.Color.%EC%97%B0%EA%B8%88%EC%83%89._.Color.%EA%B0%88%EC%83%89._.Color.%EA%B0%88%EC%83%89%ED%88%AC%ED%86%A4._.Color.%EA%B8%88%EC%83%89._.Color.%EC%B2%AD%EC%98%A5%EC%83%89._.Color.%EC%97%B0%EB%91%90%EC%83%89._.Color.%EB%85%B9%EC%83%89._.Color.%EB%8B%B4%EB%85%B9%EC%83%89._.Color.%EC%9E%90%EC%A3%BC%EC%83%89._.Color.%EB%B3%B4%EB%9D%BC%EC%83%89._.Color.%EB%85%B8%EB%9E%80%EC%83%89._.Color.%EB%B6%84%ED%99%8D%EC%83%89.')
    color.append('Or.Color.%EC%A5%90%EC%83%89._.Color.%EC%9D%80%EC%83%89._.Color.%EC%9D%80%ED%9A%8C%EC%83%89._.Color.%EC%9D%80%EC%83%89%ED%88%AC%ED%86%A4._.Color.%EC%9D%80%ED%95%98%EC%83%89._.Color.%EB%AA%85%EC%9D%80%EC%83%89.')
    color.append('Or.Color.%EA%B2%80%EC%A0%95%EC%83%89._.Color.%EA%B2%80%EC%A0%95%ED%88%AC%ED%86%A4.')
    color.append('Or.Color.%ED%9D%B0%EC%83%89._.Color.%EC%A7%84%EC%A3%BC%EC%83%89._.Color.%ED%9D%B0%EC%83%89%ED%88%AC%ED%86%A4._.Color.%EC%A7%84%EC%A3%BC%ED%88%AC%ED%86%A4.')
    if choice == 'black': color = color[2]
    elif choice == 'white': color = color[3]
    elif choice == 'gray': color = color[1]
    else: color = color[0]
    return color

def get_page(i,option):
    c = color(option)
    url = f'http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y._.Trust.Warranty._.({c}))&sr=%7CModifiedDate%7C{i * 50}%7C50'
    res = requests.get(url)
    return res



def get_last(res):
    page = []
    page = int(round(res.json()['Count'] / 50))
    return page


def get_info(res):
    desc = []
    try:
        for i in range(0, 49):
            soup = res.json()
            box = soup["SearchResults"]
            brand = box[i]['Manufacturer']
            km = box[i]['Mileage']
            name = box[i]['Model']
            fuel = box[i]['FuelType']
            price = box[i]['Price']
            year = box[i]['FormYear']
            model = box[i]['Badge']
            location = box[i]['OfficeCityState']
            photo = 'http://ci.encar.com/carpicture'+box[i]['Photo']+'001.jpg?'
            try:
                trim = box[i]['BadgeDetail']
            except:
                trim = 'x'
            link = 'http://www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid='+box[i]['Id']
            desc.append({'brand': brand, 'name': name, 'model': model, 'trim':trim,'fuel': fuel, 'km': km,
                         'year': year, 'location': location, 'price': price, 'link':link,'photo':photo})
    except:
        pass
    return desc


def get_all(option):
    res = get_page(1,option)
    p = get_last(res)
    try:
        information = []
        for i in range(p):
            res1 = get_page(i,option)
            information.append(get_info(res1))
    except:
        pass
    return information



def add_info(option):
    info = get_all(option)
    a = sum(info, [])
    info = []
    for i in a:
        i['color'] = option
        i['accident'] = '무사고'
        info.append(i)
    return info

def to_db(info1,table):
    car_db = pymysql.connect(
        user='root',
        passwd='0000',
        host='127.0.0.1',
        db='data',
        charset='utf8'
    )
    cursor = car_db.cursor(pymysql.cursors.DictCursor)
    info = info1
    insert_sql2 = f"INSERT INTO {table} VALUES (%(brand)s,%(name)s,%(model)s,%(trim)s,%(fuel)s,%(km)s,%(year)s,%(location)s,%(price)s,%(link)s,%(photo)s,%(color)s,%(accident)s);"
    cursor.executemany(insert_sql2, info)
    car_db.commit()



