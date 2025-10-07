from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def extract_data():
    ## Create a SPARQL endpoint
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    ## Create the query
    query = '''
    SELECT ?person ?personLabel ?birthPlace ?birthPlaceLabel
    WHERE{
        ?person a dbo:Person;
                dbo:birthPlace ?birthPlace.
        ?person rdfs:label ?personLabel.
        ?birthPlace rdfs:label ?birthPlaceLabel.
        FILTER (lang(?personLabel) = "en")
        FILTER (lang(?birthPlaceLabel) = "en")
    }
    LIMIT 200
    '''

    ## Send the query to the endpoint
    sparql.setQuery(query=query)

    ## Get the results
    results = sparql.query().convert()

    ## Parse through the results
    data = []
    for res in results["results"]["bindings"]:
        data.append({
            "Person": res["personLabel"]["value"],
            "BirthPlace": res["birthPlaceLabel"]["value"]
        })
    
    return pd.DataFrame(data)

def transform_to_sentence(df):
    sentences = []
    for index, row in df.iterrows():
        sentence = f"{row['Person']} was born in {row['BirthPlace']}."
        sentences.append(sentence)
    
    return sentences