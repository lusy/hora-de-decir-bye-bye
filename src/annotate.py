#-*- coding: utf-8 -*-

import sys
import codecs
import os
import nltk
from os import path
from nltk.corpus import PlaintextCorpusReader
import text_local

def annotate(a_path, punctuation, ignore_en, tokens_en, tokens_common, reg_dicts_tokens):
    '''
    annotates each word for an article according
    to the dictionary in which it was found
    input: article_id --> tokenized article
    output: csv? format?
    intermediate representation: [(token,[annotations])]
    annotations:
    EN
    ES_ALL
    ES_AR
    ....
    '''
    annotated_article = []

    # read articles as utf-8!
    with codecs.open(a_path, encoding='utf-8') as article_plain_file:
        article_plain= article_plain_file.read()

        # remove special spanish punctuation characters which are treated
        # as a part of the upcoming word by the nltk word tokenizer (default lang: en)
        # add blank in front of '.' so that it's recognized as a separate token
        translations = (
                (u'¡', ''),
                (u'¿', ''),
                (u'…', ''),
                (u'.', ' .')
                )
        for from_str, to_str in translations:
            article_plain = article_plain.replace(from_str, to_str)

        # tokenize
        tokens_article = nltk.word_tokenize(article_plain)

    for token in tokens_article:
        annotation = []

        # convert tokens to lower case for lookup
        # possibly named entities loss but simplest way;
        # eliminate short words which are far more likely to be
        # articles, prepositions, etc in Spanish;
        # eliminate some longer words which are far more likely to be esp
        if token.lower() in tokens_en and len(token.lower()) > 2 and token.lower() not in ignore_en:
            # add EN to annotation
            annotation.append('EN')

        if token.lower() in tokens_common:
            # add ES_ALL to annotation
            annotation.append('ES_ALL')
        else:
            if token in punctuation:
                annotation.append('PUNKT')

            # look up in all the regional dicts
            else:
                for rd_id in reg_dicts_tokens:
                    if token.lower() in reg_dicts_tokens[rd_id]:
                        annotation.append(rd_id)


        # if at the end annotation empty, append unknown
        if annotation == []:
            annotation.append('UNK')

        annotated_article.append((token,annotation))

    #TODO: write annotated article to file in an appropriate format
    # what is an appropriate format? (csv, text: token/ANN1_ANN2_ANN3..., xml)?

    # build concordances for the whole article
    concordanceIndex = text_local.ConcordanceIndex(tokens_article, key=lambda s:s.lower())

    a_id = a_path.split('/')[-1]

    ''' Comment out for concordances of all tokens with EN in annotations
    # write selected concordances to a file
    # (which contains concordances for the whole corpus)
    with codecs.open('data/concordances', 'a', encoding='utf-8') as out_file:
        out_file.write("Article # %s\n" % a_id)

        # we want to print the concordances for a give token just once
        # if the token appears multiple times in an article
        # en_tokens is a cache for the concordances we already printed
        en_tokens = []

        # bypass the Text() class for writing concordances to file
        #test_text = nltk.Text(tokens_article)
        for (token,annotation) in annotated_article:
            # filter all tokens where EN among annotations
            if 'EN' in annotation and token not in en_tokens:
                en_tokens.append(token)
                ta = '[%s, %s]\n' % (token, annotation)
                out_file.write(ta)
                out_file.write(concordanceIndex.return_concordance(token, width=79, lines=25))
                out_file.write("\n")

        out_file.write("-" * 60)
        out_file.write("\n\n")
    '''

    ''' Block for computing concordances for EN annotations only and UNK annotations'''
    # write selected concordances to files
    # (which contain concordances for the whole corpus)
    out_file_EN = codecs.open('data/concordances_EN', 'a', encoding='utf-8')
    out_file_UNK = codecs.open('data/concordances_UNK', 'a', encoding='utf-8')

    out_file_EN.write("Article # %s\n" % a_id)
    out_file_UNK.write("Article # %s\n" % a_id)

    # we want to print the concordances for a give token just once
    # if the token appears multiple times in an article
    # en_tokens is a cache for the EN concordances we already printed
    en_tokens = []
    # unk_tokens is a cache for the UNK concordances we already printed
    unk_tokens = []

    for (token,annotation) in annotated_article:
        # filter all tokens with annotation EN only
        if 'EN' in annotation and token not in en_tokens and len(annotation) == 1:
            en_tokens.append(token)
            ta = '[%s, %s]\n' % (token, annotation)
            out_file_EN.write(ta)
            out_file_EN.write(concordanceIndex.return_concordance(token, width=79, lines=25))
            out_file_EN.write("\n")
        # filter all tokens with annotation UNK
        if 'UNK' in annotation and token not in unk_tokens:
            unk_tokens.append(token)
            ta_unk = '[%s, %s]\n' % (token, annotation)
            out_file_UNK.write(ta_unk)
            out_file_UNK.write(concordanceIndex.return_concordance(token, width=79, lines=25))
            out_file_UNK.write("\n")

    out_file_EN.write("-" * 60)
    out_file_EN.write("\n\n")

    out_file_UNK.write("-" * 60)
    out_file_UNK.write("\n\n")

    out_file_EN.close()
    out_file_UNK.close()


    #test_text = nltk.Text(tokens_article)
    #test_text.concordance(u'balance')
    #test_text.concordance(u'pero')
    #test_text.similar(u'balance')



def main():
    '''
    import all plaintext articles as a nltk plaintext corpus
    '''
    #esp_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

    # punctuation list; we need it later to annotate punctuation as such
    punctuation = [u'.', u'!', u'?', u':', u',', u';', u'-', u'"', u"'", u'(', u')']

    # ignore from English dictionary (words that are far more probable to be in esp)
    ignore_en = [u'para', u'las', u'nos', u'con', u'vive', u'persona', u'peso', u'lee', u'mis', u'dos', u'etc', u'hombre',
                 u'placer', u'hoy', u'perfecta', u'mil', u'dolor']

    # import dictionaries (as utf-8!) --> should be done here, not importing dictionaries 2000 times
    with codecs.open('data/dictionaries-common/es_ALL', encoding='utf-8') as common_dict_file:
        common_dict = common_dict_file.read()
        tokens_common = nltk.word_tokenize(common_dict)

    with codecs.open('data/dictionaries-common/en_US', encoding='utf-8') as en_dict_file:
        en_dict = en_dict_file.read()
        tokens_en = nltk.word_tokenize(en_dict)

    # import all the regional dicts
    reg_dicts_ids = [f for f in os.listdir('data/dictionaries-common/') if path.isfile(path.join('data/dictionaries-common/', f)) and f.endswith('reg')]
    #print reg_dicts_ids

    reg_dicts_tokens = {}
    for dict_id in reg_dicts_ids:
        path_reg_dict = 'data/dictionaries-common/%s' % dict_id
        with codecs.open(path_reg_dict, encoding='utf-8') as reg_dict_file:
            reg_dict = reg_dict_file.read()
            tokens_reg = nltk.word_tokenize(reg_dict)
            reg_dicts_tokens[dict_id] = tokens_reg # maybe prettify key: es_AR_reg -> es_AR

    #print reg_dicts_tokens.keys()
    #print reg_dicts_tokens['es_AR_reg']

    #with codecs.open('data/dictionaries-common/es_AR_reg', encoding='utf-8') as ar_dict_file:
    #    ar_dict = ar_dict_file.read()
    #    tokens_ar = nltk.word_tokenize(ar_dict)
    #print tokens_ar


    # should it get dictionaries as param?

    # TODO: annotate all articles
    articles_ids = [f for f in os.listdir('data/articles-plain/') if path.isfile(path.join('data/articles-plain/', f))]
    for a_id in articles_ids:
        print "Annotating article #%s" % a_id
        a_path = 'data/articles-plain/%s' % a_id
        annotate(a_path, punctuation, ignore_en, tokens_en, tokens_common, reg_dicts_tokens)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
