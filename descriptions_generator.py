# from sentence_transformers import SentenceTransformer
from extractor import extract_data, transform_to_sentence
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse
# import pandas as pd
import re

# transformer = SentenceTransformer('all-MiniLM-L6-v2')
df = extract_data()
sentences = transform_to_sentence(df)

'''
embeddings = transformer.encode(sentences)
print(df['BirthPlace'].tolist())
'''

places = df["BirthPlace"].tolist()

sparqlEndpoint = SPARQLWrapper("https://dbpedia.org/sparql")
sparqlEndpoint.setReturnFormat(JSON)

def get_descriptions(place):
    place = re.sub(r"[,';:\"!?]", "", place)
    
    place = urllib.parse.quote(place)
    
    query = f'''
    SELECT ?desc WHERE {{
        dbr:{place} rdfs:comment ?desc .
        FILTER (lang(?desc) = "en")
    }}    
    LIMIT 1
    '''
    
    sparqlEndpoint.setQuery(query=query)
    try:
        results = sparqlEndpoint.query().convert()
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["desc"]["value"]
        else:
            return None
    except Exception as e:
        print(f"Error in fetching description for {place}:{e}")
        return None

descriptions = []
for place in places:
    desc = get_descriptions(place.replace(" ", "_"))
    descriptions.append(desc if desc else "No description available")

df["Description"] = descriptions