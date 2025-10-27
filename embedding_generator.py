from sentence_transformers import SentenceTransformer
from extractor import extract_data, transform_to_sentence

transformer = SentenceTransformer('all-MiniLM-L6-v2')
df = extract_data()
sentences = transform_to_sentence(df)

embeddings = transformer.encode(sentences)
print(df['BirthPlace'].tolist())