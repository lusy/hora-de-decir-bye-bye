#-*- coding: utf-8 -*-

import sys
import os
from os import path
from pattern import web

def to_plaintext(article_id):
    '''
    clears the html formatting from an article
    '''
    file_article = open(article_id, 'r')
    article = file_article.read()
    article_plain = web.plaintext(article)
    file_article.close()
    return article_plain


def main():
    '''
    applies to_plaintext() to all articles in articles-raw/
    and saves the plaintext artivles to articles-plain/
    '''
    articles_raw = [f for f in os.listdir('articles-raw/') if path.isfile(path.join('articles-raw/', f))]
    for article_id in articles_raw:
        print "Cleaning article %s" % article_id
        file_path_raw = 'articles-raw/%s' % article_id
        article_plain = to_plaintext(file_path_raw)
        file_path_plain = 'articles-plain/%s' % article_id
        f = open(file_path_plain, 'w')
        f.write(article_plain.encode('utf-8'))
        f.close()

if __name__ == '__main__':
    status = main()
    sys.exit(status)
