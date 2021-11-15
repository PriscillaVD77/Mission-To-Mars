#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
#optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


#use the parent element to find the first ' a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


#visit URL
url= 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


#find and click the full imagine button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


#parse the resulting html with soup
html= browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


#find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


#use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[ ]:





# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[ ]:





# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
html = browser.html
hemi_soup = soup(html,'html.parser')
hemi_soup


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with soup
html = browser.html
hemisphere_soup = soup(html, 'html.parser')

# Find the number of pictures to scan
pics_count = len(hemisphere_soup.select("div.item"))

# for loop over the link of each sample picture
for i in range(pics_count):
    # Create an empty dict to hold the search results
    results = {}
    # Find link to picture and open it
    link_image = hemisphere_soup.select("div.description a")[i].get('href')
    browser.visit(f'https://marshemispheres.com/{link_image}')
    
    # Parse the new html page with soup
    html = browser.html
    image_soup = soup(html, 'html.parser')
    # Get the full image link
    img_url = image_soup.select_one("div.downloads ul li a").get('href')
    # Get the full image title
    img_title = image_soup.select_one("h2.title").get_text()
    # Add extracts to the results dict
    results = {
        'img_url': f'https://marshemispheres.com/{img_url}',
        'title': img_title }
    
    # Append results dict to hemisphere image urls list
    hemisphere_image_urls.append(results)
    
    # Return to main page
    browser.back()


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


# 5. Quit the browser
browser.quit()


# In[ ]:




