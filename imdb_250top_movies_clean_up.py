import pandas as pd
import datetime
from cip_library import clean_film_title

# Anzeigeoptionen ändern
pd.set_option("display.max_columns", None)  # Alle Spalten anzeigen
pd.set_option("display.max_rows", None)     # Alle Zeilen anzeigen
pd.set_option("display.expand_frame_repr", False) # Zeilenumbruch verhindern

imdb_df = pd.read_csv("imdb_top_250.csv")

#print(imdb_df)
###########################################################################################################

#Bereinige die Filmnamen
clean_film_title(imdb_df, "title_en")

#Lösche die Reihen mit fehlendem Filmtitel
empty_title_en_indices = imdb_df[imdb_df["title_en"].isnull()].index
imdb_df.drop(empty_title_en_indices, inplace=True)

#Lösche die Reihen wenn der Film neuer als das aktuelle Jahr ist
current_year = datetime.datetime.now().year
future_year_indices = imdb_df[imdb_df["year"] > current_year].index
imdb_df.drop(future_year_indices, inplace=True)

#Lösche die Reihen wenn die Film ID nicht 9 Stellen hat.
#Funktion definiert und mach eine neu Zeile "valid_id" mit True und False
imdb_df["valid_id"] = imdb_df["id"].apply(lambda x: len(str(x)) == 9)
#Wenn False, dann Reihe löschen
invalid_id_indices = imdb_df[imdb_df["valid_id"] == False].index
imdb_df.drop(invalid_id_indices, inplace=True)
# Lösche "valid_id"
imdb_df.drop("valid_id", axis=1, inplace=True)

#Runde num_votes auf volle 100
imdb_df['num_votes'] = imdb_df['num_votes'].apply(lambda num_votes: round(num_votes / 100) * 100)


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
# Regisseur Nolan arbeitete 4 mal mit Schauspieler Bale zusammen, in den 250 besten Imdb-Filmen zusammen.

print(imdb_df)

