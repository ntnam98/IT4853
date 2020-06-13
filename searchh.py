from pyvi import ViTokenizer
import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/tktdtt', always_commit=True)

def search1(p, name_input):

    words = ViTokenizer.tokenize(name_input)
    list_word = words.split()

    a = []
    for word in list_word:
        word = word.replace("_", " ")
        a.append(word)

    query =""
    for word in a:
        query = query +p +': "' + word + '" '

    results = solr.search(query,**{
        'rows': 10000,
        'fl': '*, score'
    })
    return results

def search2(p, name_input, options):

    words = ViTokenizer.tokenize(name_input)
    list_word = words.split()

    a = []
    for word in list_word:
        word = word.replace("_", " ")
        a.append(word)

    query =""
    for word in a:
        query = query +p +': "' + word + '" '

    results = solr.search(query,**{
        'rows': 10000,
        'fq': {'tag : "' + options +'"'},
        'fl': '*, score'
    })
    return results