from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class MessageProcessor:
  def process_message(self, message):
    message = message.lower()
    words = word_tokenize(message)
    words = [w for w in words if len(w) > 2]
    w = []
    gram = 2
    for i in range(len(words) - gram + 1):
      w += [' '.join(words[i:i + gram])]

    sw = stopwords.words('english')
    words = [word for word in words if word not in sw]

    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return words