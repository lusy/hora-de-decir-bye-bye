#-*- coding: utf-8 -*-

from pattern import web

def to_plaintext(article_id):
    '''
    clears the html formatting from an article
    '''
    file_article = open(article_id, 'r')
    article = file_article.read()
    print web.plaintext(article)
    return web.plaintext(article)

def verticalize(plaintext):
    '''
    verticalizes the article
    '''

to_plaintext('test-article')
