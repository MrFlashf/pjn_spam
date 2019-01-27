# zrodlo: https://towardsdatascience.com/spam-classifier-in-python-from-scratch-27a98ddd8e73
from MessageProcessor import MessageProcessor
from math import log, sqrt

class SpamClassifier(object):
  def __init__(self, trainData):
    self.mails, self.labels = trainData['message'], trainData['labels']
    self.train()

  def train(self):
    self.calc_TF_and_IDF()
    self.calc_TF_IDF()

  def calc_TF_and_IDF(self):
    numberOfMessages = self.mails.shape[0]
    self.spamMails, self.hamMails = self.labels.value_counts()[1], self.labels.value_counts()[0]
    self.total_mails = self.spamMails + self.hamMails
    self.spamWords = 0
    self.hamWords = 0
    self.tfSpam = dict()
    self.tfHam = dict()
    self.idfSpam = dict()
    self.idfHam = dict()

    for i in range(numberOfMessages):
      message_processed = MessageProcessor().process_message(self.mails[i])
      count = list()

      for word in message_processed:
        if self.labels[i]:
          self.tfSpam[word] = self.tfSpam.get(word, 0) + 1
          self.spamWords += 1
        else:
          self.tfHam[word] = self.tfHam.get(word, 0) + 1
          self.hamWords += 1
        if word not in count:
          count += [word]

      for word in count:
        if self.labels[i]:
          self.idfSpam[word] = self.idfSpam.get(word, 0) + 1
        else:
          self.idfHam[word] = self.idfHam.get(word, 0) + 1 

  def countIDF(self, allMessages, mesasgesContainingWord):
    return log(allMessages / mesasgesContainingWord)

  def calc_TF_IDF(self):
    self.probSpam = dict()
    self.probHam = dict()
    self.sumOfTFIDFForSpam = 0
    self.sumOfTFIDFForHam = 0
    self.IDFTimesTFForSpam = dict()
    self.IDFTimesTFForHam = dict()

    for word in self.tfSpam:
      wordIDF = self.countIDF(self.total_mails, (self.idfSpam[word] + self.idfHam.get(word, 0)))
      wordIDFTimesTF = wordIDF * self.tfSpam[word]

      self.IDFTimesTFForSpam[word] = wordIDFTimesTF

      self.sumOfTFIDFForSpam += wordIDFTimesTF

    for word in self.tfSpam:
      self.probSpam[word] = (self.IDFTimesTFForSpam[word] + 1) / (self.sumOfTFIDFForSpam + len(list(self.IDFTimesTFForSpam.keys())))
        
    for word in self.tfHam:
      wordIDF = self.countIDF(self.total_mails, (self.idfSpam.get(word, 0) + self.idfHam[word]))
      wordIDFTimesTF = wordIDF * self.tfHam[word]

      self.IDFTimesTFForHam[word] = wordIDFTimesTF

      self.sumOfTFIDFForHam += wordIDFTimesTF

    for word in self.tfHam:
      self.probHam[word] = (self.IDFTimesTFForHam[word] + 1) / (self.sumOfTFIDFForHam + len(list(self.IDFTimesTFForHam.keys())))
        

    self.probSpamMail, self.probHamMail = self.spamMails / self.total_mails, self.hamMails / self.total_mails

  
  def classify(self, processed_message):
    pSpam, pHam = 0, 0
    for word in processed_message:                
      if word in self.probSpam:
        pSpam += log(self.probSpam[word])
      else:
        pSpam -= log(self.sumOfTFIDFForSpam + len(list(self.probSpam.keys())))

      if word in self.probHam:
        pHam += log(self.probHam[word])
      else:
        pHam -= log(self.sumOfTFIDFForHam + len(list(self.probHam.keys())))

      pSpam += log(self.probSpamMail)
      pHam += log(self.probHamMail)
    return pSpam >= pHam