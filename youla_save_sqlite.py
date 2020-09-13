# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 23:20:24 2020

@author: dmitrixsha
"""

import requests
import json
from lxml import html
import os
import dataset


db = dataset.connect('sqlite:///youla.db')
table = db['youla']


urlsrs = 'urls.txt'

def get_urllist(urls):
    urllist = []
    with open(urls) as urlfile:
        urllist = urlfile.read().splitlines()
    return urllist

#user_agent = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    
def getrequest(url):
    responses = requests.get(url)
    html1 = responses.text
    tree = html.fromstring(html1)
    return html1, tree

def makedir():
    result = getrequest(url)
#    n = random.randint(0,300) #посмотри может есть какие идентификаторы объявления
    start_json_template = "    window.__YOULA_STATE__ = "

    if start_json_template in result[0]:
        foldername = result[1].xpath('//title/text()')[0].split('–')[0]
        if os.path.exists(foldername) == False:     
            foldername = result[1].xpath('//title/text()')[0].split('–')[0]
            os.mkdir(foldername)        
        else:
            foldername = result[1].xpath('//title/text()')[0].split('–')[0]
#            os.rename(foldername, foldername+str(n))
            os.mkdir(foldername)
        os.chdir(foldername)


def get_json():
    result_to_json = getrequest(url)
    start_json_template = "    window.__YOULA_STATE__ = "
    if start_json_template in result_to_json[0]:    
        start = result_to_json[0].index(start_json_template) + len(start_json_template)
        end = result_to_json[0].index('    window.__YOULA_TEST__ = ', start)
        json_raw = result_to_json[0][start:end].strip()[:-1]
        json1 = json.loads(json_raw)
        return json1    
    
def save_photo():
    photos = []
    for photo in get_json()['entities']['products'][0]['images']:
        photos.append(photo['url'])
    print(photos)
    photos_to_save = ', '.join(photos)
    return photos_to_save
#    table.insert(dict(Photos=photos_to_save))

def save_description():
    desc_raw = get_json()['entities']['products'][0]['description']
    desc = desc_raw.encode('utf-8').decode('utf-8')
    return desc
#    table.insert(dict(Description=desc))

def save_name():
    result = getrequest(url)
    name_query = result[1].xpath('//title/text()')[0].split('–')[0]
    return name_query
#    table.insert(dict(Name=name_query))


#def saveinfo():
#    save_name()
#    save_description()
#    save_photo()

def saveinfo():
    table.insert(dict(Name=save_name(), Description=save_description(),Photo=save_photo()))



for url in get_urllist(urlsrs):
    saveinfo()
