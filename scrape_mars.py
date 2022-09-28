import pandas as pd
from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup as bs



def getFullHemiImage(site_url, img_name):
    browser = Browser('chrome', headless=True)
    browser.visit(site_url + img_name)
    
    bSoup = bs(browser.html, 'html.parser')
    
    imageList = bSoup.find_all('li')
    
    return site_url + imageList[0].a['href']

def scrape():
    return_dict = {}
    
    ### Website Scraping from https://redplanetscience.com
    
    redplanetsceience_browser = Browser('chrome', headless=True)
    redplanetsceience_browser.visit('https://redplanetscience.com')
    
    # Create a Beautiful Soup object
    soup = bs(redplanetsceience_browser.html, 'html.parser')
    
    redplanetsceience_divImg = soup.find_all('div', {'class': 'list_image'})
    redplanetsceience_divDate = soup.find_all('div', {'class': 'list_date'})
    redplanetsceience_divContentTitle = soup.find_all('div', {'class': 'content_title'})
    redplanetsceience_divArticleText = soup.find_all('div', {'class': 'article_teaser_body'})
    redplanetsceience_column_names = ["ArticleTitle","ArticleDate","SummaryText","Image"]
    redplanetscience_df = pd.DataFrame(columns = redplanetsceience_column_names)

    redplanetscience_list = []
    for idx in range(len(redplanetsceience_divImg)):
        new_row =[redplanetsceience_divContentTitle[idx].text,redplanetsceience_divDate[idx].text,redplanetsceience_divArticleText[idx].text,redplanetsceience_divImg[idx].img['src']]
        new_row_dict = {'ArticleTitle':redplanetsceience_divContentTitle[idx].text,'ArticleDate':redplanetsceience_divDate[idx].text,
                    'SummaryText':redplanetsceience_divArticleText[idx].text,'Image':redplanetsceience_divImg[idx].img['src']}
    
        # Use loc to add new rows
        redplanetscience_df.loc[idx] = new_row
        redplanetscience_list.append(new_row_dict)
    return_dict["redplanet_info"] = redplanetscience_list
    
    ### Website Scraping from https://spaceimages-mars.com/
    
    jpl_site_url = 'https://spaceimages-mars.com/'
    jpl_browser = Browser('chrome', headless=True)
    jpl_browser.visit(jpl_site_url)
    
    jpl_soup = bs(jpl_browser.html, 'html.parser')
    jpl_featured_images = jpl_soup.find_all('img',{'class': 'headerimage'})
    
    jpl_featured_image = jpl_site_url + jpl_featured_images[0]['src']
    
    return_dict['featured_image'] = jpl_featured_image
    
    ### Website Scraping from https://galaxyfacts-mars.com/
    
    mars_facts_browser = Browser('chrome', headless=True)
    mars_facts_browser.visit('https://galaxyfacts-mars.com/')
    
    mars_facts_df = pd.read_html(mars_facts_browser.html)
    
    earth_mars_facts_df = mars_facts_df[0]
    
    earth_mars_facts_json = earth_mars_facts_df.to_json()
    
    return_dict['earth_mars_facts'] = earth_mars_facts_df.to_html()
    
    ### Website Scraping from https://marshemispheres.com/
    
    mars_hemi_url = 'https://marshemispheres.com/'
    mars_hemi_browser = Browser('chrome', headless=True)
    mars_hemi_browser.visit(mars_hemi_url)

    mars_hemi_soup = bs(mars_hemi_browser.html, 'html.parser')
    
    div_hemi = mars_hemi_soup.find_all('div', {'class':'item'})
    
    hemisphere_image_urls = []

    for divItem in div_hemi:
        #print('div: ', divItem.a['href'])
        #print('Title: ', divItem.h3.text)
        imageUrl = getFullHemiImage(mars_hemi_url, divItem.a['href'])
        #print('Image URL: ', imageUrl)
        row = {'title': divItem.h3.text, 'img_url': imageUrl}
        hemisphere_image_urls.append(row)
        
    return_dict['hemispheres'] = hemisphere_image_urls
    
    print(return_dict)
    
    ### Set up return dictionary
    return return_dict

    