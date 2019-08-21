from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # # NASA Mars News

    browser= init_browser()
    mars_collection = {}


    url_nasa = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_collection["title"] = soup.find('div', class_='content_title').text
    mars_collection["content"] = soup.find(class_='article_teaser_body').text
        
   
    # # Mars Weather
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_collection["mars_weather"] = mars_weather
            
    # Mars Facts
    url_fact = "https://space-facts.com/mars/"
    tables = pd.read_html(url_fact)
    df = tables[1]
    df.columns = ['description','values']
    df.set_index('description', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    mars_collection["fact_table"] = html_table


    # # JPL Mars Space Images - Featured Image
    url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # pull images from website
    images = soup.find_all('a', class_="fancybox")
    # pull image link
    pic_src = []
    for image in images:
        pic = image['data-fancybox-href']
        pic_src.append(pic)
    #featured_pic = pic_src[0]
    mars_collection["featured_image_url"] = 'https://www.jpl.nasa.gov' + pic_src[1]
    
    # # Mars Hemispheres
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    # HTML Object
    html_hemispheres = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # Store the main_ul 
    hemispheres_main_url = 'https://web.archive.org'
    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls
    mars_collection["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_collection



