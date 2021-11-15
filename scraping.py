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
            "last_modified":dt.datetime.now(),
            "hemisphere title": hemisphere_data()
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
## Hemisphere data
def hemisphere_data():
    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    Browser.visit(url)
    html = Browser.html
    hemi_soup = soup(html,'html.parser')
    hemi_soup

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with soup
    html = Browser.html
    hemisphere_soup = soup(html, 'html.parser')

    # Find the number of pictures to scan
    pics_count = len(hemisphere_soup.select("div.item"))

    # for loop over the link of each sample picture
    for i in range(pics_count):
        # Create an empty dict to hold the search results
        results = {}
        # Find link to picture and open it
        link_image = hemisphere_soup.select("div.description a")[i].get('href')
        Browser.visit(f'https://marshemispheres.com/{link_image}')
        
        # Parse the new html page with soup
        html = Browser.html
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
        Browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    Browser.quit()

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())



