import cip_library as cip
import nltk
from nltk.tokenize import word_tokenize

# Downloading necessary NLTK modules
nltk.download("punkt")

#read data from table "movie_reviews_raw" and store the data in a dataframe
pd_reviews_transform = cip.get_data_from_mariadb(table_name = "movie_reviews_raw")


#in order to optimize the sentiment analysis we first need to pre-process the reviews. We do this by tokenizing, lemmetization and removing punctuations, symbols, and stopwords as these do not hold any value when it comes to sentiment analysis.
#tokenization and removing punctuations, symbols, numbers and stopwords
pd_reviews_transform['tokenized_text'] = pd_reviews_transform['review'].apply(cip.tokenize_and_clean)





