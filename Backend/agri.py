import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

df = pd.read_excel("agri_schemes_dataset.xlsx")

class SearchEngine:
    def __init__(self):
        self.lemmatizer=WordNetLemmatizer()
        self.stop_words=set(stopwords.words("english"))
    
    def get_pos_wordnet(self, word):
        tag=pos_tag([word])[0][1][0].upper()
        tags_dict={"N":wordnet.NOUN,
                   "V":wordnet.VERB,
                   "J":wordnet.ADJ,
                   "R":wordnet.ADV
                   }
        return tags_dict.get(tag, wordnet.NOUN)
    
    def content_preprocessing(self, content):
        content=content.lower()
        content=re.sub(r"[^a-zA-Z\s]", "", str(content))
        tokens=word_tokenize(content)
        processed_token=[]
        for token in tokens:
            if token not in self.stop_words and len(token)>2:
                pos=self.get_pos_wordnet(token)
                lemma=self.lemmatizer.lemmatize(token, pos=pos)
                processed_token.append(lemma)
        return processed_token
        
    def similarity_calculation(self,query,document):
        query_term=set(self.content_preprocessing(query))
        doc_term=set(self.content_preprocessing(document))
        if not query_term:
            return 0
        return len(query_term.intersection(doc_term))/len(query_term.union(doc_term))
        
    def search(self, query, top_n=5):
        results = []
        for idx, row in df.iterrows():
            document = f"{row['Scheme Name']} {row['Description']} {row['Eligibility']} {row['Benefits']} {row['Application Process']} {row['Tags']}"
            similarity = self.similarity_calculation(query, document)
            if similarity > 0:
                 results.append({
                    "scheme": row["Scheme Name"],
                    "similarity": similarity,
                    "description": row["Description"],
                    "eligibility": row["Eligibility"],
                    "benefits": row["Benefits"],
                    "application_process": row["Application Process"]
                })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_n]
        
