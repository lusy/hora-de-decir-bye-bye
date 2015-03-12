#-*- coding: utf-8 -*-

import sys
import nltk
import codecs
import os
from os import path
from nltk.corpus import PlaintextCorpusReader

def annotate(punctuation, tokens_en, tokens_common):
    '''
    annotates each word for an article according
    to the dictionary in which it was found
    input: article_id --> tokenized article
    output: csv? format?
    annotations:
    EN
    ES_ALL
    ES_AR
    ....
    '''
    annotated_article = []

    # read articles as utf-8!
    with codecs.open('test_plain', encoding='utf-8') as article_plain_file:
        article_plain= article_plain_file.read()

        # remove special spanish punctuation characters which are treated
        # as part of the upcoming word by the nltk word tokenizer (default lang: en)
        # add blank in front of '.' so that it's recognized as a separate token
        translations = (
                (u'¡', ''),
                (u'¿', ''),
                (u'…', ''),
                (u'.', ' .')
                )
        for from_str, to_str in translations:
            article_plain = article_plain.replace(from_str, to_str)
        #print article_plain

        # tokenize
        tokens_article = nltk.word_tokenize(article_plain)
        #tokens = esp_tokenizer.word_tokenize(article_plain)
        #print tokens

    for token in tokens_article:
        annotation = []

        # convert tokens to lower case for lookup
        # possibly named entities loss but simplest way
        if token.lower() in tokens_en:
            # add EN to annotation
            annotation.append('EN')

        if token.lower() in tokens_common:
            # add ES_ALL to annotation
            annotation.append('ES_ALL')
        else:
            if token in punctuation:
                annotation.append('PUNKT')

            # look up in all the regional dicts
            # temporarily append unknown
            else:
                annotation.append('UNK')

        annotated_article.append((token,annotation))


    #print tokens_article[0].lower() in tokens_common
    #print tokens_article[0].lower() in tokens_en
    print tokens_article
    print annotated_article

    #TODO: write to file in an appropriate format


def main():
    '''
    import all plaintext articles as a nltk plaintext corpus
    '''
    #esp_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

    # punctuation list; we need it later to annotate punctuation as such
    punctuation = [u'.', u'!', u'?', u':', u',', u';', u'-', u'"', u"'", u'(', u')']

    # import dictionaries (as utf-8!) --> should be done here, not importing dictionaries 2000 times
    with codecs.open('data/dictionaries-common/es_ALL', encoding='utf-8') as common_dict_file:
        common_dict = common_dict_file.read()
        tokens_common = nltk.word_tokenize(common_dict)

    with codecs.open('data/dictionaries-common/en_US', encoding='utf-8') as en_dict_file:
        en_dict = en_dict_file.read()
        tokens_en = nltk.word_tokenize(en_dict)

    # import all the regional dicts
    reg_dicts_ids = [f for f in os.listdir('data/dictionaries-common/') if path.isfile(path.join('data/dictionaries-common/', f)) and f.endswith('reg')]
    print reg_dicts_ids

    reg_dicts_tokens = {}
    for dict_id in reg_dicts_ids:
        path_reg_dict = 'data/dictionaries-common/%s' % dict_id
        with codecs.open(path_reg_dict, encoding='utf-8') as reg_dict_file:
            reg_dict = reg_dict_file.read()
            tokens_reg = nltk.word_tokenize(reg_dict)
            reg_dicts_tokens[dict_id] = tokens_reg

    #print reg_dicts_tokens.keys()
    #print reg_dicts_tokens['es_AR_reg']

    #with codecs.open('data/dictionaries-common/es_AR_reg', encoding='utf-8') as ar_dict_file:
    #    ar_dict = ar_dict_file.read()
    #    tokens_ar = nltk.word_tokenize(ar_dict)
    #print tokens_ar


    # should it get dictionaries as param?
    #annotate(punctuation, tokens_common, tokens_en)

    # TODO: annotate all articles

    #print tokens[0].lower() in tokens_ar
    #print tokens[0].lower() in tokens_common
    #print tokens

    #test_text = nltk.Text(tokens)
    #test_text.concordance('sueños')
    #test_text.concordance('pero')
    #test_text.similar('sueños')





if __name__ == '__main__':
    status = main()
    sys.exit(status)
