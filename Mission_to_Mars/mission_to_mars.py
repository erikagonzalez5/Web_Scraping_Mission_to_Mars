#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies

import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


#setup browser 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# In[3]:


#nasa website that will be scraped

url_nasa = 'https://redplanetscience.com/'

#browse red planet science page
browser.visit(url_nasa)
time.sleep(1)


# In[4]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


#scrape News Title

mars_results = soup.find_all('div', class_="content_title")
latest_title = mars_results[0].text


# In[6]:


#scrape paragraph

mars_results = soup.find_all('div', class_="article_teaser_body")
latest_paragraph = mars_results[0].text


# In[7]:


print(latest_title)
print(latest_paragraph)


# In[8]:


#quitting the browser

browser.quit()


# # JPL Mars Space Images - Featured Image

# In[9]:


#setup new browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[10]:


# jpl nasa website that will be scraped

url_image = 'https://spaceimages-mars.com/'

#browse jpl page
browser.visit(url_image)
time.sleep(1)


# In[11]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[12]:


#locate featured image

relative_image_path = soup.find_all('img')[1]["src"]
featured_image_url = url_image + relative_image_path
featured_image_url


# In[13]:


#quitting browser

browser.quit()


# # Mars Facts

# In[14]:


#setup new browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[15]:


# galaxy facts website that will be scraped

url_facts = 'https://galaxyfacts-mars.com/'

#browse galaxy page
browser.visit(url_facts)
time.sleep(1)


# In[16]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[17]:


tables = pd.read_html(url_facts)[0]
tables


# In[18]:


#dropped the first row
tables = tables.iloc[1: , :]
tables


# In[19]:


#renamed the columns
renamed_mars = tables.rename(columns={0:"Comparison", 1:"Mars", 2:"Earth"})
renamed_mars


# In[20]:


#reduced columns to only show Mars data
mars_table_df = renamed_mars[["Comparison", "Mars"]]
mars_table_df


# In[21]:


#generate HTML table from DataFrame
html_table = mars_table_df.to_html()
html_table


# In[22]:


#strip unwanted newlines to clean up the table
html_table.replace('\n', '')


# In[23]:


#quitting browser

browser.quit()


# # Mars Hemispheres

# In[38]:


#setup new browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[39]:


# mars hemispheres website that will be scraped
url_hemispheres = 'https://marshemispheres.com/'
browser.visit(url_hemispheres)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[40]:


#scrape images
hemispheres = soup.find_all("div", class_="item")
hemispheres


# In[49]:


#loop through each hemisphere and use dictionary to store data
title=[]
img_url=[]
for images in hemispheres:
    title = images.find('h3').text
    url = images.find('a')['href']
    hem_url = url_hemispheres+url
    browser.visit(hem_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hem_img= soup.find('div',class_='downloads')
    image_urls=hem_img.find('a')['href']
#append dictionary 
    img_url.append({"title": title, "img_url": image_urls})


# In[50]:


img_url


# In[37]:


#quitting browser

browser.quit()


# In[ ]:




