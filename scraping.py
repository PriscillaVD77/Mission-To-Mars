# Import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
def scrape_all():
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in a dictionary
    data= {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified":dt.datetime.now()
    }
    #stop webdriver and return data
    browser.quit()
    return data
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text') 
        # Use the parent element to find the first a tag and save
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the first a tag and save
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p
# ### JPL Space Images Featured Images
def featured_image(browser):
    #visit URL
    url= 'https://spaceimages-mars.com'
    browser.visit(url)

    # Fnd and click the full imagine button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html= browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url
## Mars Facts
def mars_facts():
    # add try/except for error handling
    try:
        #use 'read_html' to scrape facts table into datafram
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    #assign columns and set index of datafram
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    #convert dataframe into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())



