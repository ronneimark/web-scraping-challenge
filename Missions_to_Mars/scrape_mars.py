from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    # ## Mars News
    browser=init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    news_p=soup.find('div',class_='article_teaser_body').text
    news_date=soup.find('div', class_='list_date').text
    news_title = soup.find('div', class_='content_title').a.text.strip()
    news_link= 'http://mars.nasa.gov' + soup.find('div', class_='content_title').a.get('href')

    # ## Mars Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url) 

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')


    link=soup.find('article').a.get('data-fancybox-href')
    featured_image_url = 'http://jpl.nasa.gov' + link

    # ## Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # mars_weather=soup.find_all('p', {"class":['TweetTextSize', 'TweetTextSize--normal', 'js-tweet-text', 'tweet-text']})[0].text
    mars_weather = soup.find('p', class_='TweetTextSize').text


    # ## Mars Facts

    url = 'https://space-facts.com/mars/'

    mars_facts_df = pd.read_html(url)[0]

    #tablestring='<table><tr><td>Attribute</td><td>Value</td></tr>'

    # x=0
    # for rows in mars_facts.iterrows():
    #     add_to_string=f'<tr><td>{mars_facts.iloc[x,0]}</td><td>{mars_facts.iloc[x,1]}</td>,</tr>'
    #     tablestring += add_to_string
    #     x+=1

    tablestring = mars_facts_df.to_html()

    # tablestring += '</table>'

    # ## Mars Hemispheres

    # url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.visit(url) 

    # html = browser.html
    # soup = BeautifulSoup(html, 'lxml')

    # hemisphere_list = soup.find_all('div',class_='description')

    # link_list=[]
    # title_list=[]

    # for hemisphere in hemisphere_list:
    #     title=hemisphere.a.h3.text.strip("Enhanced").rstrip()
    #     link=hemisphere.a.get('href').strip('/search/map')
    #     url=f'https://astropedia.astrogeology.usgs.gov/download/{link}.tif/full.jpg'
    #     title_list.append(title)
    #     link_list.append(url)
    
    # x=0
    # hemispheres_list=[]
    # for titles in title_list:
    #     hemisphere_dict={}
    #     hemisphere_dict['title']=title_list[x]
    #     hemisphere_dict['img_url']=link_list[x]
    #     hemispheres_list.append(hemisphere_dict)
    #     x+=1

    mars_data={
        "news_title":news_title,
        "news_p":news_p,
        "news_date":news_date,
        "news_link":news_link,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "mars_facts_table": tablestring
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data