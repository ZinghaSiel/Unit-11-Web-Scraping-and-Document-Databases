# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
#from splinter.exceptions import ElementDoesNotExist

# Define scrape function
def scrape():
    ## Create a library that holds Mars' Data
    Mars_Data = {}

    ## Execute Chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    #NASA Mars News
    ##Scraping headlines from NASA site
    News_URL = "https://mars.nasa.gov/news/"
    browser.visit(News_URL)
    ##Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    News_Title = soup.find("div",class_="content_title").text
    News_Paragraph = soup.find("div", class_="article_teaser_body").text
    News_Date = soup.find("div", class_="list_date").text
    Mars_Data["News_Date"] = News_Date
    Mars_Data["News_Title"] = News_Title
    Mars_Data["News_Paragraph"] = News_Paragraph

    # JPL Mars Space Images - Featured Image
    ##Visit the url for JPL Featured Space Image
    ##Find the image url for the current Featured Mars Image
    ##Use splinter to navigate the site
    Image_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(Image_URL)
    ##Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    Img_URL  = soup.find("article")["style"].replace("background-image: url(','').replace(');", "")[1:-1]
    Main_URL = "https://www.jpl.nasa.gov"
    ##Assign the url string to a variable called Featured_Image_URL
    Featured_Image_URL = Main_URL + Img_URL
    Mars_Data["Featured_Image_URL"] = Featured_Image_URL

    # Mars Weather
    ##Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page
    Weather_URL = "https://twitter.com/marswxreport?lang=en"
    browser.visit(Weather_URL)
    ##Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    ##Save the tweet text for the weather report as a variable called Mars_Weather
    Mars_Weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    Mars_Data["Mars_Weather"] = Mars_Weather

    # Mars Facts
    ##Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc
    Facts_URL = "https://space-facts.com/mars/"
    ##Use Pandas to convert the data to a HTML table string
    Mars_Planet_Profile = pd.read_html(Facts_URL, attrs = {'id': 'tablepress-mars'})[0]
    Mars_Facts = Mars_Planet_Profile.to_html()
    Mars_Data["Mars_Facts"] = Mars_Facts

    # Mars Hemispheres
    ##Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    USGS_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(USGS_URL)
    ##Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    ##Retreive all Items that contain mars hemispheres information
    Items = soup.find_all('div', class_='item')
    ##Create empty 'Hemisphere Image URLs' list
    Hemisphere_Image_URLs = []
    ##Main Astrogeology URL
    Main_URL = 'https://astrogeology.usgs.gov'
    ##Loop through the items previously stored
    for i in Items: 
        # Store title
        Title = i.find('h3').text
        # For every item, store link to full resolution image
        Img_URL = i.find('a', class_='itemLink product-item')['href']
        # Follow the link to the full image website 
        browser.visit(Main_URL + Img_URL)
        # HTML Object for each hemisphere's information 
        Img_html = browser.html
        # Parse HTML with Beautiful Soup for each hemisphere's information 
        soup = BeautifulSoup(Img_html, 'html.parser')
        # Retrieve full image source 
        Full_Img_URL = Main_URL + soup.find('img', class_='wide-image')['src']
        # Append the retreived information into a list of python dictionaries 
        Hemisphere_Image_URLs.append({"Title" : Title, "Img_url" : Full_Img_URL})
    Mars_Data["Hemisphere_Image_URLs"] = Hemisphere_Image_URLs

    #Return Library
    return Mars_Data