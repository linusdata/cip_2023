import pandas as pd
import cip_library as cip

#daten aus den drei csv files holen und sie je in ein pandas dataframe speichern
pd_imdb = pd.read_csv('imdb_top250_stage_3.csv')
pd_reviews = pd.read_csv('review_stage_3.csv')
pd_oscars = pd.read_csv('oscars_stage_3.csv')

#da einige filme mehrmals verfilmt wurden müssen wir die nicht relevanten filme aus dem dataframe pd_oscars löschen. zudem müssen wir für einzelfälle die namen im pd_oscars anpassen, damit sie mit denen des pd_imdb übereinstimmen
pd_oscars = pd_oscars.drop(pd_oscars[(pd_oscars['movie'] == 'up') & (pd_oscars['year'] == 1985)].index)
pd_oscars = pd_oscars.drop(pd_oscars[(pd_oscars['movie'] == 'thelionking') & (pd_oscars['year'] == 2020)].index)
pd_oscars = pd_oscars.drop(pd_oscars[(pd_oscars['movie'] == 'rashomon') & (pd_oscars['year'] == 1953)].index)
pd_oscars = pd_oscars.drop(pd_oscars[(pd_oscars['movie'] == 'thebattleofalgiers') & (pd_oscars['year'] == 1969)].index)
pd_oscars = pd_oscars.drop(pd_oscars[(pd_oscars['movie'] == 'tobeornottobe') & (pd_oscars['year'] == 1984)].index)
pd_oscars['movie'] = pd_oscars['movie'].replace('theempirestrikesback', 'starwarsepisodevtheempirestrikesback')
pd_oscars['movie'] = pd_oscars['movie'].replace('seven', 'se7en')
pd_oscars['movie'] = pd_oscars['movie'].replace('starwars', 'starwarsepisodeivanewhope')
pd_oscars['movie'] = pd_oscars['movie'].replace('returnofthejedi', 'starwarsepisodevireturnofthejedi')
pd_oscars['movie'] = pd_oscars['movie'].replace('thebicyclethief', 'bicyclethieves')

#dataframes joinen
pd_joined = pd.merge(pd_imdb, pd_reviews, on = 'id', how = 'left')
pd_joined = pd.merge(pd_joined, pd_oscars, left_on='film_title_cleaned', right_on='movie', how = 'left')

#dataframe in MariaDB tabelle schreiben
cip.write_to_table(df=pd_joined, table_name="movie_data_merged_stage")

#dataframe als csv abspeichern
pd_joined.to_csv("movie_data_merged_stage.csv", index=False)

#beantwortung der Forschungsfragen
#Welcher Film war hat den besten sentiment score?
max_index = pd_joined['mean_sentiment_score'].idxmax() #index des films mit dem höchsten sentiment score finden
movie_title = pd_joined.loc[max_index, 'title_en'] # film title finden
print("Der Film mit dem besten Sentiment Score ist: " + movie_title)

#Welcher Film wird auf IMDb am besten bewertet und wie viele Bewertungen wurden abgegeben? 
max_index = pd_joined['rating'].idxmax() #index des films mit dem höchsten sentiment score finden
movie_title = pd_joined.loc[max_index, 'title_en'] # film title finden
votes = pd_joined.loc[max_index, 'num_votes'] # anzahl votes finden
print("Der Film mit der Besten Bewertung auf IMDb ist: " + movie_title + ", dieser ist " + str(votes) + " mal bewertet worden von Usern.")

#Gibt es eine Korrelation zwischen sentiment Score der Reviews und der Anzahl gewonnenen Oscars?
cor_sentiment_oscars = pd_joined['mean_sentiment_score'].corr(pd_joined['number_W'])
print("Der Korrelationskoeffizient zwischen 'mean_sentiment_score' und der Anzahl gewonnenen Oscars ist: " + str(cor_sentiment_oscars) + ". Dies deutet darauf hin, dass es keine Korrelation gibt.")

#Gibt es eine Korrelation zwischen Rating und der Anzahl gewonnenen Oscars?
cor_rating_oscars = pd_joined['rating'].corr(pd_joined['number_W'])
print("Der Korrelationskoeffizient zwischen 'Rating' und der Anzahl gewonnenen Oscars ist: " + str(cor_rating_oscars) + ". Dies deutet darauf hin, dass es keine Korrelation gibt.")

#Gibt es eine Korrelation zwischen Rating und der sentiment Score der Reviews?
cor_sentiment_rating = pd_joined['rating'].corr(pd_joined['mean_sentiment_score'])
print("Der Korrelationskoeffizient zwischen 'Rating' und der 'mean_sentiment_score' ist: " + str(cor_sentiment_rating) + ". Dies deutet darauf hin, dass es keine Korrelation gibt.")

#demo test

