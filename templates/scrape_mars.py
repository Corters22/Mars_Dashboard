import pandas as pd
import datetime as dt
from flask import Flask
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
# 1. Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

#create empty dictionary for return
    mars_info_dict = {}

# Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_news = 'https://redplanetscience.com/'
    browser.visit(mars_news)

# Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# Retrieve the News Title
    news_title = soup.body.find('div', class_='content_title').text
#add to dictionary
    mars_info_dict['news_title'] = news_title

# Retrieve the paragraph text
    news_para = soup.find('div', class_='article_teaser_body').text
#add to dictionary
    mars_info_dict['news_para'] = news_para


# JPL Mars Space Images - Featured Image

    mars_images = 'https://spaceimages-mars.com/'
    browser.visit(mars_images)

# Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

#Scrape for image url
    image_url = soup.find('img', class_='headerimage')['src']
    featured_image_url = f'https://spaceimages-mars.com/{image_url}'
#add to dictionary
    mars_info_dict['featured_image_url'] = featured_image_url

# Mars Facts
 
#defining target url
    mars_facts =  'https://galaxyfacts-mars.com/'

# use pandas to read in html from previously defined url
    facts = pd.read_html(mars_facts)

# grabbing the second table with only Mars facts
    df = facts[1]
#renaming columns
    df.columns=['Mars Attributes', 'Facts']

#converting df to html table for later use
    df.to_html('mars_facts_table.html')


# Mars Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)

# Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# loop through all four pages to get title and image url
    # create empty list
    hemisphere_image_urls = []
    # scrape for links to click on
    results = soup.find_all('div', class_='item')
    for result in results:
        #create empty dictionary to append to list
        images = {}
        title = result.find('h3').text
        #add title minus the 'enhanced' to dictionary
        images['title'] = title[:-9]
        #link to click on to get url for pic
        browser.find_by_text(title).click()

        #Create BeautifulSoup object; parse with 'html.parser' for new page
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # scrape for image url and add to dictionary
        images['url'] = soup.find('img', class_='wide-image')['src']
        browser.back()
        #add dictionary to list
        hemisphere_image_urls.append(images)  

    browser.quit()

    mars_info_dict['Hemisphere_data'] = hemisphere_image_urls
    
    #return dictionary
    return mars_info_dict



