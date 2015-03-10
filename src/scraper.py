# -*- coding: utf-8 -*-

import sys
import requests
from pattern import web

'''
get all categories and subcategories from main page
'''
def get_categories():
    page = requests.get("http://siempremujer.com/").text.encode('UTF-8')
    dom = web.Element(page)
    potentials = dom('div[class="nav"] div[class="sub"] > a')
    attributes = [elem.attrs for elem in potentials]
    #categories_moda = ['/category/moda/', '/category/tendencias-moda/', '/category/actualidad-moda/', '/category/disenadores-moda/']
    #categories = [d['href'] for d in attributes if d['href'].startswith('/category/') and d['href'] not in categories_moda]
    categories = [d['href'] for d in attributes if d['href'].startswith('/category/')]

    return categories

'''
get all article urls for the first 10 pages of a given category
'''
def get_article_urls(category):
    article_urls = []
    for i in xrange (1,11):
        if (i == 1):
            url = "http://siempremujer.com%s" % category
        else:
            url = "http://siempremujer.com%spage/%d/" % (category,i)

        #print (url)
        page = requests.get(url).text.encode('UTF-8')
        dom = web.Element(page)
        potentials = dom('div[class="thumb"] > a')
        attributes = [elem.attrs for elem in potentials]
        article_urls_page = [d['href'] for d in attributes]
        article_urls.extend(article_urls_page)
        #print article_urls

    return article_urls


'''
get all article ids for the first 10 pages of a given category
'''
def get_article_ids(category):
    article_urls = get_article_urls(category)
    article_ids = [url.split('/')[-2] for url in article_urls]
    return article_urls


'''
get the text for an article given its url, save it to file
'''
def get_article_text(url):
    r = requests.get(url).text.encode('UTF-8')
    dom = web.Element(r)
    title = dom.by_class('post-post-title')[0].source.encode('UTF-8')
    text = dom.by_class('post-post-entry')[0].source.encode('UTF-8')
    file_name = url.split('/')[-2] # parse out article id from url for file name
    file_path = 'articles/%s' % file_name

    f = open(file_path, 'w')
    f.write(title + '\n')
    f.write(text)
    f.close()



'''
main
'''
def main():
    categories = get_categories()

    # scrape them into files!
    #for c in categories:
    #    print('category: ', c)
    #    article_urls = get_article_urls(c)
    #    for au in article_urls:
    #        print ('article url: ', au)
    #        get_article_text(au)

    # make a dict of categories and articles in them
    classified_articles = {}

    # TODO: make the write line by line
    # find a way to convert array to writable stuff
    for c in categories:
        print('category:', c)
        article_ids = get_article_ids(c)
        classified_articles[c] = article_ids
        print classified_articles[c]

    #ff = open('class_articles', 'w')
    #ff.write(classified_articles)
    #ff.close()

if __name__ == '__main__':
    status = main()
    sys.exit(status)
