#-*- coding: utf-8 -*-

import sys
import os
from os import path
from pattern import web
from nltk.corpus import PlaintextCorpusReader

def to_plaintext(article_id):
    '''
    clears the html formatting from an article
    '''

    file_article = open(article_id, 'r')
    article = file_article.read()
    article_plain = web.plaintext(article)
    file_article.close()
    return article_plain

def all_to_plaintext():
    '''
    applies to_plaintext() to all articles in articles-raw/
    and saves the plaintext artivles to articles-plain/
    '''

    articles_raw = [f for f in os.listdir('data/articles-raw/') if path.isfile(path.join('data/articles-raw/', f))]
    for article_id in articles_raw:
        print "Cleaning article %s" % article_id
        file_path_raw = 'data/articles-raw/%s' % article_id
        article_plain = to_plaintext(file_path_raw)
        file_path_plain = 'data/articles-plain/%s' % article_id
        f = open(file_path_plain, 'w')
        f.write(article_plain.encode('utf-8'))
        f.close()


def clean_dicts():
    '''
    cleans annotations from dictionaries
    so that we obtain plain word lists
    dictionaries raw: blabla/XYZ
    dictionaries clean: blabla
    '''

    dicts_root = 'dictionaries'
    file_pattern_raw = '.*/.*\.dic\.utf8'
    dicts = PlaintextCorpusReader(dicts_root, file_pattern_raw)

    for d in dicts.fileids():
        print "Cleaning dict %s" % d
        file_path_clean = 'data/dictionaries-clean2/%s' % d.split('/')[0]
        f_raw = dicts.open(d)
        f_clean = open(file_path_clean, 'w')
        for line in f_raw:
            f_clean.write(line.split('/')[0])
            f_clean.write('\n')

        f_clean.close()


def main():
    all_to_plaintext()
    clean_dicts()


if __name__ == '__main__':
    status = main()
    sys.exit(status)
