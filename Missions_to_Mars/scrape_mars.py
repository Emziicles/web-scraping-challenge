# import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# set the path


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    header_title, content_paragraph = mars_news(browser)
    img_urls_title = hemispheres(browser)
    
    data = {
        'Title': header_title,
        'Paragraph': content_paragraph,
        'Image': featured_image(browser),
        'Facts': mars_facts(),
        'Hemispheres': img_urls_title,
        'Modified': dt.datetime.now()
        
    }
    browser.quit()
    return data


def mars_news(browser):
    url = "https://redplanetscience.com/"
    
    browser.visit(url)
    html = browser.html
    soup1 = bs(html, 'html.parser')
    
    try:
    
        slide_elem = soup1.select_one('div.list_text')
        header_title = slide_elem.find('div', class_='content_title').get_text()
        content_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return header_title, content_paragraph
    
def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    
    browser.visit(url)
    
    html = browser.html
    soup2 = bs(html, 'html.parser')
    
    try:
        
        image = [i.get("src") for i in soup2.find_all("img", class_= "headerimage fade-in")]
    
    except AttributeError:
        return None
    
    featured_image_url = url + image[0]
    
    return featured_image_url

def mars_facts():
    try:
         facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
        
    facts_df.columns = ['Fact', 'Mars', 'Earth']
    facts_df.set_index('Fact', inplace=True)
    
    return facts_df.to_html()

def hemispheres(browser):
    url = "https://marshemispheres.com/"
    
    browser.visit(url)
    
    hemisphere_image_urls = []
    for images in range(4):
        html = browser.html
        soup4 = bs(html, 'html.parser')
        title = soup4.find("h2", class_="title").text
        img_url = soup4.find("li").a.get('href')
        hemispheres_dict = {}
        hemispheres_dict["img_url"] = f'https://marshemispheres.com/{img_url}'
        hemispheres_dict["title"] = title
        hemisphere_image_urls.append(hemispheres_dict)
        
        browser.back()
    return hemisphere_image_urls
    
browser.quit()
    
if __name__ == "__main__":
    print(scrape())