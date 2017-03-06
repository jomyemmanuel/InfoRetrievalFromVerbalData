import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn import cross_validation
from sklearn.metrics import classification_report
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
import cPickle

csv_path = '/home/jomy/Code/mec/mainpro/webapp/InfoRetrievalFromVerbalData/django/irapp/classifier/out.csv'

class Sentimental:
    def load_file(self):
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file,delimiter="\t",quotechar='"')
            reader.next()
            data =[]
            target = []
            for row in reader:
                # skip missing data
                if row[0] and row[1]:
                    data.append(row[0])
                    target.append(row[1])

            return data,target


    # preprocess creates the term frequency matrix for the review data set
    def preprocess(self):
        data,target = self.load_file()
        self.count_vectorizer = CountVectorizer(binary='true')
        data = self.count_vectorizer.fit_transform(data)
        tfidf_data = TfidfTransformer(use_idf=False).fit_transform(data)

        return tfidf_data

    def learn_model(self,data,target):
        # preparing data for split validation. 60% training, 40% test
        data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,target,test_size=0.1,random_state=43)
        self.classifier = BernoulliNB().fit(data_train,target_train)
        # count_vectorizer = CountVectorizer(binary='true')
        predicted = self.classifier.predict(data_test)
        # self.evaluate_model(target_test,predicted)

    # read more about model evaluation metrics here
    # http://scikit-learn.org/stable/modules/model_evaluation.html
    def evaluate_model(self,target_true,target_predicted):
        print classification_report(target_true,target_predicted)
        print "The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted))

    def main(self):
        data,target = self.load_file()
        tf_idf = self.preprocess()
        self.learn_model_svm(tf_idf,target)

    def use_model(self,review):
        review=self.count_vectorizer.transform(review)
        return self.classifier_rbf.predict(review)

    def learn_model_svm(self,data,target):
        data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,target,test_size=0.1,random_state=43)
        self.classifier_rbf = svm.LinearSVC()
        # self.classifier_svm = BernoulliNB().fit()
        self.classifier_rbf.fit(data_train,target_train)
        with open('my_dumped_classifier.pkl', 'wb') as fid:
            cPickle.dump(self.classifier_rbf, fid)    
        prediction_rbf = self.classifier_rbf.predict(data_test)
        # self.evaluate_model(target_test,prediction_rbf)



if __name__ == "__main__":
    m = sentimental()
    m.main()
    # m.use_model(['food is really bad and worse ever, never try'])

   

    # load it again
    # with open('my_dumped_classifier.pkl', 'rb') as fid:
    #     gnb_loaded = cPickle.load(fid)