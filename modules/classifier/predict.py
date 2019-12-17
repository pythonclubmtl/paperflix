from joblib import dump, load
import os

class Oracle():

    def __init__(self, sentence):
        self.category, self.proba, self.classes = self.my_predict(sentence)

    def my_predict(self, text):
        clf=load(os.getcwd()+'/bib_files/trained_data.joblib')
        vectorizer=load(os.getcwd()+'/bib_files/vectorized_abstracts.joblib')
        text_vect=self.transform_vect([text], vectorizer)
        predicted_category=clf.predict(text_vect)
        predicted_proba=clf.predict_proba(text_vect)
        classes=clf.classes_
        return predicted_category, predicted_proba, classes

    def transform_vect(self, list_sentences, vectorizer):
        vecorized_sentences = vectorizer.transform(list_sentences)
        return vecorized_sentences