
import requests
from bs4 import BeautifulSoup
import pandas as pd
db_ranking={
    'vleage:2021':'https://bongda24h.vn/vleague/bang-xep-hang-25.html',
    "nghanh":"https://bongda24h.vn/bong-da-anh/bang-xep-hang-1.html",
    "c1":"https://bongda24h.vn/bong-da-chau-au/bang-xep-hang-7.html",
    "laliga":"https://bongda24h.vn/bong-da-tay-ban-nha/bang-xep-hang-5.html"
}

import os
def get_rank(url, cache=True, path="cache.csv"):
    if cache and os.path.isfile(path):
        data = pd.read_csv(path)
        return data
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    a = soup.findAll("div",{"class":"box-bxh"})[0]
    tr  = a.findAll("tr")
    header = [i.text for i in tr[0].findAll("th")]
    data=[]
    for i in tr[1:]:
        d = [k.text for k in i.findAll("td")]
        data.append({c:cx for c,cx in zip(header,d) })
    data = pd.DataFrame(data)
    if cache:
        data.to_csv(path,index=False)
    return data
# crawl(db['nghanh'], path="nghanh.csv")