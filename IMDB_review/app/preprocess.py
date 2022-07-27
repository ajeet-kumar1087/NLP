import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import string

class DataPreprocessing:
    def __init__(self):
        pass

    def lower_(self, text):
        return text.lower()

    def remove_urls(self, text):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text =  url_pattern.sub(r'', text)
        return text

    def remove_punctuation(self, text):
        text =  text.translate(str.maketrans('', '', string.punctuation))
        return text

    def remove_emoji(self, text):
        text = re.sub('<[^>]*.', '', text)
        emojis = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
        text=re.sub('[\W]+',' ',text.lower()) +\
                    ' '.join(emojis).replace('-','')

        return text.translate(str.maketrans('', '', string.punctuation))

    def lemmatize(self, text):
        words = nltk.word_tokenize(text)
        words = [WordNetLemmatizer().lemmatize(word) for word in words if word not in set(stopwords.words('english')) ]
        text = ' '.join(words)
        return text

    
    def apply_all(self,text):
        text = self.lower_(text)
        text = self.remove_urls(text)
        text = self.remove_emoji(text)
        text = self.lemmatize(text)
        return text