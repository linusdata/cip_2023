import cip_library as cip
import nltk


# Downloading necessary NLTK modules
nltk.download("punkt")
nltk.download('vader_lexicon')
nltk.download('wordnet')

#read data from table "movie_reviews_raw" and store the data in a dataframe
pd_reviews_transform = cip.get_data_from_mariadb(table_name = "movie_reviews_raw")


#in order to optimize the sentiment analysis we first need to pre-process the reviews. We do this by tokenizing, and removing punctuations, symbols, and stopwords as these do not hold any value when it comes to sentiment analysis.
#tokenization and removing punctuations, symbols, numbers and stopwords
pd_reviews_transform['processed_text'] = pd_reviews_transform['review'].apply(cip.preprocess_text_for_sentiment)

#calculate sentiment score for "processed_text"
pd_reviews_transform['sentiment_score'] = pd_reviews_transform['processed_text'].apply(cip.get_sentiment_score)

#based on the value in "sentiment_score" create a column called "sentiment" with value 'pos' if sentiment score is above 0 and 'neg' if it is below 0
pd_reviews_transform['sentiment'] = pd_reviews_transform['sentiment_score'].apply(lambda x: 'pos' if x > 0 else 'neg')

print(123)








