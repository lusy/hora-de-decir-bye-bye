# Hora de decir bye-bye

## Aim of this project
Analyze usage of English in Spanish language women's magazines (and usage of Spanish in English language women's magazines) in the US.

## Outline

1. Get some data: scrape magazine articles from
  * siempremujer.com
  * latina.com

2. Text pre-processing
  * convert to plain text

3. Dictionary pre-processing
  * we want to annotate tokens in articles according to their language
  * use [open offices dictionaries](http://archive.services.openoffice.org/pub/mirror/OpenOffice.org/contrib/dictionaries/)
  * we need simple word lists, so clean up annotation here and convert to utf-8!
  * make a common Spanish dictionary (intersection of all Spanish dictionaries)
  * and regional specific Spanish dictionaries for the different countries

4. Annotate text
  * look up all the words in Spanish/English dictionaries
  * annotate language (multiple labels possible)

5. Get n-grammes with alternating language use

6. Try to generalize some contexts where such n-grammes appear

## Tools

* webscraping: request and pattern
* natural language processing: nltk
