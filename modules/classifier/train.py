import os, glob, csv
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load


class Trainer():

    def __init__(self):
        self.report = {}
        (abstracts_bib, label_bib, files_list_bib) = self.bib_reader()
        (abstracts_csv, label_csv, files_list_csv) = self.csv_reader()
        label = label_bib+label_csv
        abstracts = abstracts_csv+abstracts_bib
        trained_vectorizer = self.my_vectorizer(abstracts)
        (X_train, X_test, y_train, y_test, clf) = self.my_classifier(abstracts, label, trained_vectorizer)
        self.my_score(X_test, y_test, clf)

    def bib_reader(self):
        folder_path2 = os.getcwd()+"/bib_files"
        extension = 'bib'
        os.chdir(folder_path2)
        files_list = glob.glob('*.{}'.format(extension))
        abstracts_bib=[]; label_bib=[]
        for files_name in files_list:
            with open(files_name, encoding="utf8") as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
                for row in bib_database.entries:
                    if not row.get("abstract"):
                        pass
                    else:
                        clean_abstract=self.stopwords_func(row.get("abstract"))
                        abstracts_bib.append(clean_abstract)
                        label_bib.append(files_name.rsplit(".")[0])
        os.chdir('..')
        return abstracts_bib, label_bib, files_list

    def csv_reader(self):
        folder_path = os.getcwd()+"/bib_files"
        extension = 'csv'
        os.chdir(folder_path)
        files_list = glob.glob('*.{}'.format(extension))
        abstracts_csv=[]; label_csv=[]
        for files_name in files_list:
            with open(files_name, encoding="utf8") as file:
                table = csv.reader(file, delimiter=',')
                for row in table:
                    if not row[10]:
                        pass
                    else:
                        clean_abstract=self.stopwords_func(row[10])
                        abstracts_csv.append(clean_abstract)
                        label_csv.append(files_name.rsplit(".")[0])
        os.chdir('..')
        return abstracts_csv, label_csv, files_list

    def my_vectorizer(self, abstracts):
        vectorizer = TfidfVectorizer(min_df=5, ngram_range=(1,3))
        vectorizer.fit(abstracts)
        os.chdir(os.getcwd()+"/bib_files")
        dump(vectorizer, 'vectorized_abstracts.joblib')
        os.chdir('..')
        return vectorizer

    def my_classifier(self, abstracts, label, vectorizer, percentage_split = 0.33):
        abstracts_vect=self.transform_vect(abstracts, vectorizer)
        X_train, X_test, y_train, y_test = train_test_split(abstracts_vect, label, test_size=percentage_split, random_state=42)
        clf = ComplementNB()
        clf.fit(X_train, y_train)
        os.chdir(os.getcwd()+"/bib_files")
        dump(clf, 'trained_data.joblib')
        os.chdir('..')
        return X_train, X_test, y_train, y_test, clf

    def my_score(self, X_test, y_test, clf):
        clf.predict(X_test)
        result_test = clf.score(X_test, y_test)
        result_percent=result_test*100
        self.report["test_accuracy"] = result_percent
        print("Accuracy :", result_percent)
        return result_percent

    def stopwords_func(self, abstract):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(abstract)
        filtered_sentence = []
        for word in word_tokens:
            if word not in stop_words:
                filtered_sentence.append(word)
        filtered_sentence = self.untokenizer(filtered_sentence)
        return filtered_sentence

    def untokenizer(self, token_sentences):
        sentences = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in token_sentences]).strip()
        return sentences

    def transform_vect(self, list_sentences, vectorizer):
        vecorized_sentences = vectorizer.transform(list_sentences)
        return vecorized_sentences