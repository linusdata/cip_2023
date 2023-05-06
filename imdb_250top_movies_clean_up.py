import pandas as pd
import datetime
from cip_library import clean_film_title
from cip_library import to_int

# Anzeigeoptionen
pd.set_option("display.max_columns", None)  # Alle Spalten anzeigen
pd.set_option("display.max_rows", None)     # Alle Zeilen anzeigen
pd.set_option("display.expand_frame_repr", False) # Zeilenumbruch verhindern

imdb_df = pd.read_csv("imdb_top_250_raw.csv")

print(imdb_df)

###########################################################################################################

#Bereinigung

#Bereinige die Filmnamen
clean_film_title(imdb_df, "title_en")

#Bereinige die Jahre
imdb_df['year'] = imdb_df['year'].str.replace(r'\(|\)', '', regex=True)
to_int(imdb_df,'year')


#Die Anzahl Bewertungen
imdb_df['num_votes'] = imdb_df['rating'].str.extract(r'(\d[\d,]*\d)')
imdb_df['num_votes'] = imdb_df['num_votes'].str.replace(',', '')
to_int(imdb_df,'num_votes')

#Die durchschnittliche Bewertung
imdb_df['rating'] = imdb_df['rating'].str.extract(r'(\d\.\d)')
imdb_df['rating'] = imdb_df['rating'].astype(float)

#Der Regisseur und der Schauspieler 1 und Schauspieler 2
directors_and_actors = imdb_df['persons'].str.split(' \(dir.\),', expand=True)
imdb_df['director'] = directors_and_actors[0]
actors = directors_and_actors[1].str.split(', ', expand=True)
imdb_df['actor1'] = actors[0]
imdb_df['actor2'] = actors[1]
imdb_df = imdb_df.drop(columns=['persons'])




###########################################################################################################
#Spalten ergänzen

#Wie alt ist der Film?
current_year = datetime.datetime.now().year
imdb_df["film_age"] = current_year - imdb_df["year"]


#Wie oft hat der Regisseur mit dem Schauspieler zusammen gearbeitet bei den 250 besten Filmen.

#Zusammenarbeit wird gesplit dies wegen actor1 und actor2
imdb_df['collaboration1'] = ''
imdb_df['collaboration2'] = ''

#Loope alle Regisseure und Schauspieler pro Reihe durch.
for index, row in imdb_df.iterrows():
    director = row['director']
    actors = [row['actor1'], row['actor2']]

    # Suche alle Zusammenarbeiten vom Schauspieler 1 mit dem Regisseur und mach einen String
    collaborations1 = imdb_df[(imdb_df['director'] == director) & ((imdb_df['actor1'] == actors[0]) | (imdb_df['actor2'] == actors[0]))].shape[0]
    imdb_df.loc[index, 'collaboration1'] = f"{director} - {actors[0]} - {collaborations1}"

    # Suche alle Zusammenarbeiten vom Schauspieler 2 mit dem Regisseur und mach einen String
    collaborations2 = imdb_df[(imdb_df['director'] == director) & ((imdb_df['actor1'] == actors[1]) | (imdb_df['actor2'] == actors[1]))].shape[0]
    imdb_df.loc[index, 'collaboration2'] = f"{director} - {actors[1]} - {collaborations2}"

#Hilfe bei der Intepretation
#"Christopher Nolan - Christian Bale - 4"
# Regisseur Nolan arbeitete 4 mal mit Schauspieler Bale zusammen, in den 250 besten Imdb-Filmen.


print(imdb_df)
imdb_df.to_csv("imdb_top_250.csv", index=False)