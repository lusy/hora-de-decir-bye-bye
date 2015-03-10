# -*- coding: utf-8 -*-

from nltk.corpus import PlaintextCorpusReader

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

    dicts_root = 'data/dictionaries-clean'
    file_pattern = 'es_.*'
    dicts = PlaintextCorpusReader(dicts_root, file_pattern)

    # compute intersection of all Spanish dictionaries
    common_dict = set(dicts.words('es_AR'))

    for d in dicts.fileids():
        common_dict = common_dict.intersection(set(dicts.words(d)))

    # write intersection to file
    file_common = open('data/dictionaries-common/es_ALL', 'w')

    for item in list(common_dict):
        file_common.write('%s\n' % item)

    file_common.close()

    # compute regional dictionaries
    for d in dicts.fileids():
        print "Computing regional dictionary for %s...." % d
        regional_dict = set(dicts.words(d)) - common_dict
        regional_path = 'data/dictionaries-common/%s_reg' % d
        file_regional = open(regional_path, 'w')
        regional_sorted = sorted(list(regional_dict))

        for item in regional_sorted:
            file_regional.write('%s\n' % item)

        file_regional.close()

