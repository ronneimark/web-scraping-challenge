#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


# ## Mars News

# In[11]:


#Use splinter-browser to open NASA 

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)


# In[12]:


try:

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    articles = soup.find_all('div', class_='content_title')
    news_ps=soup.find_all('div',class_='article_teaser_body')
    dates=soup.find_all('div', class_='list_date')
    
    y=0
    article_list=[]

    for article in articles:
        item_dict = {}
        item_dict['date']=dates[y].text
        item_dict['news_title'] = article.a.text.strip()
        item_dict['news_p']=news_ps[y].text
        linktext=article.a.get('href')
        item_dict['link']='http://mars.nasa.gov' + linktext
        article_list.append(item_dict)
        y+=1
        
except:
    print('DONE')
        


# In[13]:


len(article_list)


# In[15]:


article_df = pd.DataFrame(article_list)
article_df.head()


# ## Mars Image

# In[6]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url) 

html = browser.html
soup = BeautifulSoup(html, 'lxml')


link=soup.find('article').a.get('data-fancybox-href')
featured_image_url = 'http://jpl.nasa.gov' + link

featured_image_url


# ## Mars Weather

# In[7]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'lxml')

mars_weather=soup.find_all('p', {"class":['TweetTextSize', 'TweetTextSize--normal', 'js-tweet-text', 'tweet-text']})[0].text

mars_weather


# ## Mars Facts

# In[8]:


url = 'https://space-facts.com/mars/'

mars_facts = pd.read_html(url)[0]

mars_facts


# In[9]:


tablestring='<table><tr><td>Attribute</td><td>Value</td></tr>'

x=0
for rows in mars_facts.iterrows():
    add_to_string=f'<tr><td>{mars_facts.iloc[x,0]}</td><td>{mars_facts.iloc[x,1]}</td>,</tr>'
    tablestring += add_to_string
    x+=1

tablestring += '</table>'

tablestring


# ## Mars Hemispheres

# In[10]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url) 

html = browser.html
soup = BeautifulSoup(html, 'lxml')

hemisphere_list = soup.find_all('div',class_='description')

link_list=[]
title_list=[]

for hemisphere in hemisphere_list:
    title=hemisphere.a.h3.text.strip("Enhanced").rstrip()
    link=hemisphere.a.get('href').strip('/search/map')
    url=f'https://astropedia.astrogeology.usgs.gov/download/{link}.tif/full.jpg'
    title_list.append(title)
    link_list.append(url)
    
x=0
hemispheres_list=[]
for titles in title_list:
    hemisphere_dict={}
    hemisphere_dict['title']=title_list[x]
    hemisphere_dict['img_url']=link_list[x]
    hemispheres_list.append(hemisphere_dict)
    x+=1

hemispheres_list
    


# In[ ]:




