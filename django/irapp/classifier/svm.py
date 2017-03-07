import numpy as np
import re
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sentimental import *
import os

oldfile = os.getcwd() + '/irapp/classifier/new_reviews_yaa.txt'

d={'SPEAKER: M1': 'I was in the United Kingdom when I was told I could be closer.', 'SPEAKER: M3': 'That the rules and regulations governing the whole. Are people moving with you on a pension basis so people moving to other countries.', 'SPEAKER: M2': "Brian thank you very much. She's obviously tough living out there Sandra Humphries in SC. What do you think.It's out freezing now is the cold is based on the world.You said how much should you simplify the pensions and everyone gets the same I don't care how you distinguish between somebody living in Scotland and somebody living in the south of Spain.", 'SPEAKER: F1': "No I don't think they should get it because is my idol out there than it is over here.Can they really do get when they get cold weather. But I don't see why anybody in Spain should get it. They're not paying for fuel in this country.", 'summary': "I was in the United Kingdom when I was told I could be closer.Brian thank you very much. She's obviously tough living out there Sandra Humphries in SC. What do you think.No I don't think they should get it because is my idol out there than it is over here.It's out freezing now is the cold is based on the world.Can they really do get when they get cold weather. But I don't see why anybody in Spain should get it. They're not paying for fuel in this country.You said how much should you simplify the pensions and everyone gets the same I don't care how you distinguish between somebody living in Scotland and somebody living in the south of Spain.That the rules and regulations governing the whole. Are people moving with you on a pension basis so people moving to other countries."}


class Svm:

    def __init__(self):
        self.total=[]
        self.categories=[]
        self.sentiments=[]
        self.review_category_split()

    def review_category_split(self): 
      with open(oldfile, 'r') as infile:
        category_array = []
        review_array = []
        for line in infile:
          review, topics = line.split('&&&&')
          review_array.append(review)
          category = topics.split('+')
          x = []
          if(len(category) > 0):
            for j in category:
              x.append(j.strip('\n ').lower())
            category_array.append(x)

      self.X_train = np.array(review_array)
      self.y_train_text = category_array
      self.train_load_classifier()

    def make_opinion_unit(self,string):
      string_array = []
      string_array.append(re.split('[.!;:]|but|then',string))
      return string_array[0]

    def train_load_classifier(self):
      
      self.mlb = MultiLabelBinarizer()
      Y = self.mlb.fit_transform(self.y_train_text)
      self.classifier = Pipeline([
          ('vectorizer', CountVectorizer()),
          ('tfidf', TfidfTransformer()),
          ('clf', OneVsRestClassifier(LinearSVC()))])

      self.classifier.fit(self.X_train, Y)


    def category_prediction(self,sentence):
      opinion_units=self.make_opinion_unit(sentence)
      self.X_test = np.array(opinion_units)
      predicted = self.classifier.predict(self.X_test)
      self.all_labels = self.mlb.inverse_transform(predicted)
      # for item, labels in zip(self.X_test, all_labels):
      #     print('{0} => {1}'.format(item, ', '.join(labels)))


    def sentiment_prediction(self,string):
      s = Sentimental()
      s.main()
      self.sentiment_value=s.use_model([string])
      self.sentiments.append(self.sentiment_value[0])


    def sentiment_category_merge(self):
      m = {}
      for ele in self.all_labels:
          for values in ele :
              if values not in m.keys():
                  m[values] = self.sentiment_value[0]
                  self.categories.append(values)

      self.total.append(m)

    def call_multiple(self,d):

      for ele in d:
        if ele != 'summary':
          self.category_prediction(d[ele])
          self.sentiment_prediction(d[ele])
          self.sentiment_category_merge()


string = "Strictly an average place. They got a big menu but most of the things are overpriced when compare to other cafes in Cochin. Nice calm and quite ambience with ample seating. They also got wide variety of deserts with decent pricing."

if __name__=="__main__":
  obj = Svm()
  obj.category_prediction(string)
  obj.sentiment_prediction(string)
  obj.sentiment_category_merge()

  print string
  print obj.categories
  print obj.sentiments
  # print obj.total
# y_test = [[]]

# print accuracy_score(y_test, predicted)

# print d