
#Dependencies

import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager

def initial_browser():
#setup browser 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = initial_browser()
    mars_data= {}

# # NASA Mars News
def mars_news():
#     browser = initial_browser

#nasa website that will be scraped

    url_nasa = 'https://redplanetscience.com/'

#browse red planet science page
    browser.visit(url_nasa)
    time.sleep(1)
#html object and parsing
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


#scrape News Title

    mars_results = soup.find_all('div', class_="content_title")
    latest_title = mars_results[0].text


# In[6]:


#scrape paragraph

    mars_results = soup.find_all('div', class_="article_teaser_body")
    latest_paragraph = mars_results[0].text


    mars_data['latest_title'] = latest_title
    mars_data['latest_paragraph'] = latest_paragraph



# # JPL Mars Space Images - Featured Image
def mars_image():
#     browser = initial_browser

# jpl nasa website that will be scraped

    url_image = 'https://spaceimages-mars.com/'

#browse jpl page
    browser.visit(url_image)
    time.sleep(1)
#html object and parsing
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

#locate featured image

    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url_image + relative_image_path
    
    mars_data['featured_image_url'] = featured_image_url


# # Mars Facts
def mars_facts():

    # galaxy facts website that will be scraped

    url_facts = 'https://galaxyfacts-mars.com/'

    #browse galaxy page
    browser.visit(url_facts)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    tables = pd.read_html(url_facts)[0]
    
    #dropped the first row
    tables = tables.iloc[1: , :]
    

    #renamed the columns
    renamed_mars = tables.rename(columns={0:"Comparison", 1:"Mars", 2:"Earth"})
    renamed_mars


    #reduced columns to only show Mars data
    mars_table_df = renamed_mars[["Comparison", "Mars"]]
    mars_table_df


    #generate HTML table from DataFrame
    html_table = mars_table_df.to_html()
    html_table

    #strip unwanted newlines to clean up the table
    html_table.replace('\n', '')

    mars_data['facts'] = html_table


# # Mars Hemispheres

def mars_hemi():

    # mars hemispheres website that will be scraped
    url_hemispheres = 'https://marshemispheres.com/'
    browser.visit(url_hemispheres)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #scrape images
    hemispheres = soup.find_all("div", class_="item")
    hemispheres


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
    mars_data['img_url'] = img_url

    browser.quit()
    return mars_data






