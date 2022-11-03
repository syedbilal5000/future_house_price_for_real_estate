
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

location_dha_house=location_dha_flat=location_bahria_house=location_bahria_flat=[]
title_dha_house=title_dha_flat=title_bahria_house=title_bahria_flat=[]
price_dha_house=price_dha_flat=price_bahria_house=price_bahria_flat=[]
bedroom_dha_house=bedroom_dha_flat=bedroom_bahria_house=bedroom_bahria_flat=[]
area_dha_house=area_dha_flat=area_bahria_house=area_bahria_flat=[]

def string_conversion(string):
    """ Getting numbers from string """
    if type(string) is not str:
        return '0'
    x=0
    s=''
    for r in string:
        if r==' ':
            x=1
        if x==0:
            s+=r
    return s

def url2content(url):
    """ Getting url, returning html tree after finding specific css class for scraping """
    response=requests.get(url)
    soup=BeautifulSoup(response.text, 'html.parser')
    content=soup.findAll("div",attrs={'class':'l body pl-10'})
    return content

def html_miner(content, society_type, house_type):
    for r in content:
        t=r.div.div.span.get('title')
        p=r.div.select("div")[1].font.text.strip()
        pr=p[3:]
        if (r.find("div",attrs={'class':'l ls_desc'})) is None:
            loc=''
        else:
            loc=r.find("div",attrs={'class':'l ls_desc'}).div.div.div.text
        if ((r.find("div",attrs={'class':'l ls_desc'})).div.div.select("div")[1].div.span) is None:
            bed=''
        else:
            bed=(r.find("div",attrs={'class':'l ls_desc'})).div.div.select("div")[1].div.span.text.strip()
            bed=int(re.search(r'\d+', bed).group())
        try:
            area=((r.find("div",attrs={'class':'l ls_desc'})).div.div.select("div")[1].div.select("span")[2].text.strip())
        except IndexError:
            area=np.NaN
        if society_type==1:
            if house_type==1:
                title_dha_house.append(t)
                price_dha_house.append(float(string_conversion(pr)))
                location_dha_house.append(loc)
                bedroom_dha_house.append(bed)
                area_dha_house.append(int(string_conversion(area).replace(',','')))
            else:
                title_dha_flat.append(t)
                price_dha_flat.append(float(string_conversion(pr)))
                location_dha_flat.append(loc)
                bedroom_dha_flat.append(bed)
                area_dha_flat.append(int(string_conversion(area).replace(',','')))
        else:
            if house_type==1:
                title_bahria_house.append(t)
                price_bahria_house.append(float(string_conversion(pr)))
                location_bahria_house.append(loc)
                bedroom_bahria_house.append(bed)
                area_bahria_house.append(int(string_conversion(area).replace(',','')))
            else:
                title_bahria_flat.append(t)
                price_bahria_flat.append(float(string_conversion(pr)))
                location_bahria_flat.append(loc)
                bedroom_bahria_flat.append(bed)
                area_bahria_flat.append(int(string_conversion(area).replace(',','')))

urls={'DHA': {'House': 'https://www.zameen.com/Houses_Property/Karachi_DHA_Defence-213-.html',
              'Flat': 'https://www.zameen.com/Flats_Apartments/Karachi_DHA_Defence-213-.html'},
    'Bahria': {'House': 'https://www.zameen.com/Houses_Property/Karachi_Bahria_Town_Karachi-8298-.html',
               'Flat': 'https://www.zameen.com/Flats_Apartments/Karachi_Bahria_Town_Karachi-8298-.html'}}
dha_house_url=urls['DHA']['House']
dha_flat_url=urls['DHA']['Flat']
bahria_house_url=urls['Bahria']['House']
bahria_flat_url=urls['Bahria']['Flat']

''' This loop will iterate two times, and for each iteration it will go to four different links, 
also there are more than 15 data points in each html page ... So, 2*4*15 '''
for i in range(1,3):
    print('Scraping Page: ',i)
    link_dha_hosue=dha_house_url[:-5]+str(i)+dha_house_url[-5:]
    link_dha_flat=dha_house_url[:-5]+str(i)+dha_house_url[-5:]
    link_bahria_hosue=bahria_house_url[:-5]+str(i)+bahria_house_url[-5:]
    link_bahria_flat=bahria_house_url[:-5]+str(i)+bahria_house_url[-5:]
    content_dha_house=url2content(link_dha_hosue)
    content_dha_flat=url2content(link_dha_flat)
    content_bahria_house=url2content(link_bahria_hosue)
    content_bahria_flat=url2content(link_bahria_flat)
    html_miner(content_dha_house, 1, 1)
    html_miner(content_dha_flat, 1, 2)
    html_miner(content_bahria_house, 2, 1)
    html_miner(content_bahria_flat, 2, 2)

df_dha_house=pd.DataFrame({ 'title': title_dha_house, 'bed': bedroom_dha_house, 
                           'area': area_dha_house, 'type': 'House', 'society': 'DHA', 
                           'location': location_dha_house, 'price': price_dha_house })
df_dha_flat=pd.DataFrame({ 'title': title_dha_flat, 'bed': bedroom_dha_flat, 
                           'area': area_dha_flat, 'type': 'Flat', 'society': 'DHA', 
                           'location': location_dha_flat, 'price': price_dha_flat })
df_bahria_house=pd.DataFrame({ 'title': title_bahria_house, 'bed': bedroom_bahria_house, 
                              'area': area_bahria_house, 'type': 'House', 'society': 'Bahria', 
                           'location': location_bahria_house, 'price': price_bahria_house })
df_bahria_flat=pd.DataFrame({ 'title': title_bahria_flat, 'bed': bedroom_bahria_flat, 
                              'area': area_bahria_flat, 'type': 'Flat', 'society': 'Bahria', 
                           'location': location_bahria_flat, 'price': price_bahria_flat })

df=pd.concat([df_dha_house, df_dha_flat, df_bahria_house, df_bahria_flat])
df.to_csv('F://Web Scraping/scrape_data.csv', index=False)
