from splinter import Browser
import pandas as pd


def init_browser():
    # exec_path = {'executable_path': '/usr/local/bin/chromedriver'}
    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}

    return Browser('chrome', headless=True, **exec_path)


def scrape():
    url1 = 'https://mars.nasa.gov/news/'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url3 = 'https://twitter.com/marswxreport?lang=en'
    url4 = 'http://space-facts.com/mars/'
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    mars_collection = {}

    browser = init_browser()
    browser.visit(url1)
    news_title = browser.find_by_css('.content_title').first.text
    news_p = browser.find_by_css('.article_teaser_body').first.text

    mars_collection['news_title'] = news_title
    mars_collection['news_p'] = news_p

    browser = init_browser()
    browser.visit(url2)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']

    mars_collection['featured_image_url'] = featured_image_url

    browser = init_browser()
    browser.visit(url3)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break

    mars_collection['mars_weather'] = mars_weather

    df = pd.read_html(url4, attrs={'id': 'tablepress-mars'})[0]
    df = df.set_index(0).rename(columns={1: "value"})
    del df.index.name
    mars_facts = df.to_html(justify='left')

    mars_collection['mars_facts'] = mars_facts

    browser = init_browser()
    browser.visit(url5)
    first = browser.find_by_tag('h3')[0].text
    second = browser.find_by_tag('h3')[1].text
    third = browser.find_by_tag('h3')[2].text
    fourth = browser.find_by_tag('h3')[3].text

    browser.find_by_css('.thumb')[0].click()
    first_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']

    hemisphere_image_urls = [
        {'title': first, 'img_url': first_img},
        {'title': second, 'img_url': second_img},
        {'title': third, 'img_url': third_img},
        {'title': fourth, 'img_url': fourth_img}
    ]

    mars_collection['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_collection