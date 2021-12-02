import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import pymysql
from encar import to_db,add_info
from encar_for import add_info_for
from kcar import get_all_k


info = add_info('etc')
encar_for = add_info_for('etc')
kcar = get_all_k()

to_db(encar_for,'warehouse')
# to_db(info,'warehouse')
to_db(kcar,'warehouse1')

# info1 = add_info_for('etc')
# info2 = get_all_k()

# to_db(info1,'warehouse')
# to_db(info2,'warehouse1')