# -*- coding: utf-8 -*-

import os
import nltk
from os import path

def cats_to_dict():
    '''
    converts the list of categories and urls to a dictionary
    with format {cat1:[id1, id2, id3], cat2:[id34, id21]...}
    so that we can easily look up all the articles of a category
    and be able to determine whether there are common (linguistic)
    patterns within a category.

    note: we can easily look up all the articles for a category
    but not necessarily the category of a specific article
    '''

    class_file = open('class_articles', 'r')

    classification = {}

    for line in class_file:
        # get category name
        if line.startswith('('):
            category = line.split('/')[2]

        # higher level categories are empty
        elif line == '[]\n':
            classification[category] = []
            category = ''

        # parse article ids from urls for lower level categories
        else:
            article_ids = [url.split('/')[-2] for url in line.split(', ')]

            classification[category] = article_ids
            category = ''

    class_file.close()

    return classification

def customize_esp_dicts():
    '''
    helper function which constructs a common Spanish dictionary
    for all LA countries;
    and specific regional dictionaries for each country;
    all saved to data/dictionaries-common
    '''

    dicts_root = 'data/dictionaries-clean/es/'

    # compute intersection of all Spanish dictionaries

    ## initialize intersection with Argentinian dictionary
    ar_path = dicts_root + 'es_AR'
    common_file = open(ar_path, 'r')
    common_file_read = common_file.read()
    common_dict = set(nltk.word_tokenize(common_file_read))
    common_file.close()

    print "Len(common_dict) init: ", len(common_dict)

    dicts_ids = [f for f in os.listdir(dicts_root) if path.isfile(path.join(dicts_root, f))]

    for dict_id in dicts_ids:
        dict_path = dicts_root + dict_id
        dict_file = open(dict_path, 'r')
        dict_file_read = dict_file.read()
        dict_tokens = nltk.word_tokenize(dict_file_read)
        common_dict = common_dict.intersection(set(dict_tokens))
        dict_file.close()


    print "Len(common_dict) end: ", len(common_dict)


    ## write intersection to file
    common_dict_sorted = sorted(list(common_dict))
    file_common = open('data/dictionaries-common/es_ALL', 'w')

    for item in common_dict_sorted:
        file_common.write('%s\n' % item)

    file_common.close()


    # compute regional dictionaries and write them to files

    for dict_id in dicts_ids:
        print "Computing regional dictionary for %s...." % dict_id
        source_path = dicts_root + dict_id
        source_file = open(source_path, 'r')
        source_file_read = source_file.read()
        source_tokens = nltk.word_tokenize(source_file_read)
        source_file.close()

        regional_dict = set(source_tokens) - common_dict
        regional_path = 'data/dictionaries-common/%s_reg' % dict_id
        file_regional = open(regional_path, 'w')
        regional_sorted = sorted(list(regional_dict))

        for item in regional_sorted:
            file_regional.write('%s\n' % item)

        file_regional.close()


customize_esp_dicts()
