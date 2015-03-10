# -*- coding: utf-8 -*-

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

