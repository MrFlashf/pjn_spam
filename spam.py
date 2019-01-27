import pandas as pd
import numpy as np
from SpamClassifier import SpamClassifier
from MessageProcessor import MessageProcessor
from CheckDomain import CheckDomain
from CheckTime import CheckTime

def testMode():
  goodHits = 0
  missedHits = 0
  messages = testData['message']
  labels = testData['labels']
  allMessages = messages.shape[0]

  for i in range(allMessages):
    message = messages[i]
    processed = MessageProcessor().process_message(message)
    isSpam = spamClassifier.classify(processed)
    if isSpam == labels[i]:
      goodHits += 1
    else:
      missedHits += 1

  print('Ilość prób:' + str(allMessages))
  print('Próby poprawne: ' + str(goodHits))
  print('Próby niepoprawne: ' + str(missedHits))
  print('Procent udanych prób:', str((goodHits / allMessages) * 100))

def userMode():
  print("Podaj wiadomość")
  message = input()

  print("Podaj adres, z którego wiadomość została wysłana")
  adress = input()

  print("Podaj godzinę, o której otrzymałeś wiadomość (format 24h)")
  time = input()

  spamClassifierClassification = spamClassifier.classify(MessageProcessor().process_message(message))

  emailDomainClassification = CheckDomain().isEmailDomainBlackListed(adress)

  timeClassification = CheckTime().isTimeSuspicious(time)

  chanceForSpam = spamClassifierClassification + emailDomainClassification + timeClassification

  if chanceForSpam == 0:
    print('Wiadomość to nie spam')
  elif chanceForSpam == 3:
    print('Wiadomość na pewno jest spamem')
  else:
    chanceForSpamPercentage = chanceForSpam / 3 * 100
    print('Szansa iż wiadomość to spam jest równa ' + str(chanceForSpamPercentage) + '%')


mails = pd.read_csv('spam.csv', encoding='latin-1')
mails.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
mails.rename(columns={'v1': 'labels', 'v2': 'message'}, inplace=True)
di = {'ham': 0, 'spam': 1}
mails = mails.replace({'labels': di})

totalMails = mails['message'].shape[0]
trainIndex, testIndex = list(), list()

for i in range(mails.shape[0]):
  if np.random.uniform(0, 1) < 0.75:
    trainIndex += [i]
  else:
    testIndex += [i]

trainData = mails.loc[trainIndex]
testData = mails.loc[testIndex]

trainData.reset_index(inplace = True)
trainData.drop(['index'], axis = 1, inplace = True)

testData.reset_index(inplace = True)
testData.drop(['index'], axis = 1, inplace = True)

spamClassifier = SpamClassifier(trainData)

# userMode()
testMode()