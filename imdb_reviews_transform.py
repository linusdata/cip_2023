import cip_library as cip
import nltk
import pandas as pd

# herunterladen der benötigten NLTK module
nltk.download("punkt")
nltk.download('vader_lexicon')
nltk.download('wordnet')

#Lesen von Daten aus dem CSV "review_stage_1" und Speichern der Daten in einem dataframe
pd_reviews_transform = pd.read_csv('review_stage_1.csv')

#Um die sentiment analyse zu optimieren, müssen wir die Reviews zunächst vorverarbeiten. Dies geschieht durch Tokenisierung und das Entfernen von Interpunktionen, Symbolen und Stoppwörtern, da diese für die sentiment analyse keinen Wert haben.
pd_reviews_transform['processed_text'] = pd_reviews_transform['review'].apply(cip.preprocess_text_for_sentiment)

#Berechnung des sentiment score für "processed_text"
pd_reviews_transform['sentiment_score'] = pd_reviews_transform['processed_text'].apply(cip.get_sentiment_score)

#dataframe nach ID gruppieren, berechnung des durchschnittlichen sentiment_score für jeden Film und der Anzahl der Reviews pro Film -> Ergebnis ist ein dataframe mit nur einer Zeile pro Film und aggregiertem sentiment_score und number_of_reviews
pd_reviews_transform = pd_reviews_transform.groupby('id')['sentiment_score'].agg(['mean', 'size']).reset_index()
pd_reviews_transform.columns = ['id', 'mean_sentiment_score', 'number_of_reviews']

#basierend auf der Grundlage des Wertes in "mean_sentiment_score" eine Spalte mit der Bezeichnung "sentiment" mit dem Wert "pos", wenn der Stimmungswert über 0 liegt, und "neg", wenn er unter 0 liegt, erstellen
pd_reviews_transform['sentiment'] = pd_reviews_transform['mean_sentiment_score'].apply(lambda x: 'pos' if x > 0 else 'neg')

#dataframe in IMDb tabelle schreiben
cip.write_to_table(df=pd_reviews_transform, table_name="review_stage_3")

#dataframe als csv abspeichern
pd_reviews_transform.to_csv("review_stage_3.csv", index=False)











