import time as t
import random
import bs4 as bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os
image_list=[]
price_list=[]

if not os.path.exists('images/'): os.makedirs('images/') 

def money(x):
  try:
    return int(x.get_text().split('US$')[1].split('Pre-sale')[0].replace(',',''))
  except:
    try:
      return int(x.get_text().split('US$')[1].split('+')[0].replace(',',''))
    except:
      try:
        return int(x.get_text().split('US$')[1].split('-')[0].replace(',',''))
      except:
        return -1

for i in range(1,5000):
  if i%100==0:
    print(f'{i} pictures are parsed')
  URL=f"https://www.artsy.net/auction-result/{i}"
  resp = requests.request("GET",URL)
  soup = bs4.BeautifulSoup(resp.text, "html.parser")
  t.sleep(random.randint(1,6))

  image = soup.find('img')
  webs = requests.get(requests.compat.urljoin(URL, image.get('src')))
  t.sleep(random.randint(1,6))
  body=soup.find('body')
  price = money(body)
  if price>0:
    name = 'images/' + str(i)+'.png'
    open(name, 'wb').write(webs.content)
    price_list.append(price)
    image_list.append(name)

data = pd.DataFrame({'price':price_list,'image':image_list})
data.to_csv('output.csv',sep=',',index=False)

os.system("zip -r data.zip images/ output.csv")