import mariadb
import random
import sys
import pandas as pd
import sqlalchemy as sa
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def mariadb_connect(usr="cip_user",pw="cip_pw", db="CIP"):
    """
    Die Funktion wird verwendet, um eine Verbindung zu mariadb herzustellen. Sie benötigt 3 optionale Argumente 'usr', 'pw' und 'db'.
    :param usr: definiert den user für die Verbindung (default ist 'cip_user')
    :param pw: definiert das passwort für die Verbindung (default ist 'cip_pw')
    :param db: definiert die database für die Verbindung (default ist 'CIP')
    :return: Gibt ein Mariadb-Verbindungsobjekt zurück.
    """
    try:
        conn = mariadb.connect(
            user=usr,
            password=pw,
            host="127.0.0.1",
            port=3306,
            database=db
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def create_table(table_name, columns, datatypes):
    """
    Die Funktion wird verwendet, um Tabellen in Mariadb zu erstellen. Sie benötigt 3 Argumente 'table_name', 'columns' und 'datatypes'.
    :param table_name: definiert den namen der zu erstellenden Tabelle
    :param columns: Liste mit allen in der Tabelle benötigten Spalten
    :param datatypes: Liste der Datentypen für jede Spalte
    """
    cur = mariadb_connect().cursor()
    create_table = "CREATE OR REPLACE TABLE" + " " + table_name + " ("
    # zip columns und datatypes
    zipped = list(zip(columns, datatypes))

    for i in range(len(zipped)):
        create_table += zipped[i][0] + " " + zipped[i][1] + ", "
    #die letzten beiden Zeichen des string entfernen (, und space) und ein abschließendes ")" hinzufügen.
    create_table = create_table[:-2] + ")"
    cur.execute(create_table)

def write_to_table(df, table_name, usr="cip_user",pw="cip_pw", db="CIP"):
    """
    Die Funktion wird verwendet, um Dataframes in Tabellen in Mariadb zu schreiben. Dazu erstellt sie eine Sqlalchemy-Engine. Sie benötigt 5 Argumente: 'df', 'table_name', 'usr', 'pw' und 'db'.
    :param df: definiert das dataframe, welches in die Tabelle geschrieben werden soll.
    :param table_name: definiert den Namen der Tabelle, in die die Daten geschrieben werden sollen.
    :param usr: definiert den user für die Verbindung (default ist 'cip_user')
    :param pw: definiert das passwort für die Verbindung (default ist 'cip_pw')
    :param db: definiert die database für die Verbindung (default ist 'CIP')
    """
    #sqlalchemy engine definieren
    engine_str = f'mysql+pymysql://{usr}:{pw}@localhost:3306/{db}'
    engine = sa.create_engine(engine_str)
    #dataframe in die tabelle schreiben
    df.to_sql(con=engine, name=table_name, if_exists='replace')

def get_data_from_mariadb(table_name, columns = "*"):
    """
    Die Funktion wird verwendet, um Daten aus einer Tabelle in Mariadb in ein dataframe zu lesen. Sie nimmt zwei Argumente 'table_name' und 'columns' entgegen.
    :param table_name: Name der Tabelle, von welcher Daten gelesen werden sollen.
    :param columns: Optional. Bestimmt die Spalten, die ausgewählt werden sollen. Wenn nichts definiert ist, werden alle Spalten ausgewählt.
    :return: gibt einen Dataframe zurück, welches die Daten aus der angegebenen Tabelle enthält
    """
    #Verbindung zu mariadb erstellen
    cur = mariadb_connect().cursor()
    #string für auszuwählende Spalten erstellen
    cols = ""
    #wenn columns ungleich "*" ist, werden alle Einträge aus der angegebenen Liste gelesen und dem string cols hinzugefügt. Andernfalls cols ist gleich "*".
    if columns != "*":
        for col in columns:
            cols += col + ", "
        cols = cols[:-2]
    else:
        cols = "*"
    #string für abfrage erstellen
    query = "SELECT " + cols + " FROM " + table_name
    #Abfrage ausführen und Ergebnisse in "results" abrufen
    cur.execute(query)
    results = cur.fetchall()
    #Spaltenüberschriften der Tabelle holen
    headers = pd.DataFrame(cur.description)
    #dataframe mit den "results" erstellen
    df = pd.DataFrame(results)
    #Verwendung der abgerufenen Tabellenüberschriften als Spaltenüberschriften im dataframe
    df.columns = headers[0]
    return df

def to_int(df, column):
    """
    Die Funktion wird verwendet, um eine Spalte in einem dataframe in den Typ "Int" umzuwandeln. Sie benötigt zwei Argumente 'df' und 'column'.
    :param df: dataframe in welchem eine Spalte angepasst werden soll.
    :param column: Spalte, welche angepasst werden soll.
    :return: Gibt einen Dataframe zurück, in dem die angegebene Spalte in den Typ Integer umgewandelt wurde
    """
    #Zunächst müssen wir alle nicht numerischen Zeichen in der angegebenen Spalte ersetzen. Zu diesem Zweck verwenden wir regex mit der Funktion replace()
    df[column] = df[column].replace('[^0-9]', '', regex = True)
    #dann definieren wir die angegebene Spalte als Typ Integer
    df[column] = df[column].astype(int)
    return df

def clean_film_title(df, column):
    """
    Funktion wird verwendet, um die Spalte "Filmtitel" zu bereinigen, um sicherzustellen, dass alle Quellen das gleiche Format haben.
    Insbesondere sollen alle Sonderzeichen wie ":" und "," entfernt werden, und der Titel soll in Kleinbuchstaben umgewandelt werden.
    Die Funktion benötigt zwei Argumente: 'df' und 'column'.
    :param df: Datenframe, in dem eine Spalte geändert werden muss
    :param column: film title Spalte.
    :return: gibt einen Datenframe zurück, in dem die Filmtitelspalte bereinigt und als neue Spalte hinzugefügt wurde
    """
    #Zunächst müssen wir alle Sonderzeichen in der angegebenen Spalte ersetzen. Zu diesem Zweck verwenden wir regex mit der Funktion replace()
    df["film_title_cleaned"] = df[column].replace('[^a-zA-Z0-9]', '', regex=True)
    #dann wird die spalte in lower case transformiert
    df["film_title_cleaned"] = df["film_title_cleaned"].str.lower()
    return df

def extract_id(list_in, list_out):
    """
    Funktion wird verwendet, um die Film-ID von IMDb href Link zu extrahieren
    :param list_in: Liste mit allen href-Werten
    :param list_out: Liste, die nur id's enthält
    :return: Liste, die nur id's enthält
    """
    #go through each element in list_in and split the entries by "/". if a word starts with "tt" it is an id and we want to append it to list_out.
    for i in list_in:
        string = i
        split = string.split("/")
        for word in split:
            if word[0:2] == "tt":
                list_out.append(word)
    return list_out

def get_sentiment_score(text):
    """
    Die Funktion wird verwendet, um den Sentiment-Score für einen gegebenen Text mit Hilfe des SentimentIntensityAnalyzer von NLTK zu berechnen.
    :param text: Der Text, für den der Sentiment-Score berechnet werden soll.
    :return: Der Sentiment-Score des gegebenen Textes, der von -1 (stark negativ) bis 1 (stark positiv) reicht.
    """
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    compund_score = scores['compound']
    return compund_score

def preprocess_text_for_sentiment(text):
    """
    Diese Funktion dient der Tokenisierung von Text und der Entfernung von Sonderzeichen, Symbolen, Satzzeichen, Zahlen und Stoppwörtern. Anschließend werden die Token lemmatisiert und schließlich wieder zu einem String zusammengefügt.
    Dies ist wichtig bei der Vorbereitung von Text für die Stimmungsanalyse. Es benötigt ein Argument 'text'.
    :param text: text, der vorverarbeitet werden muss
    :return: gibt den vorverarbeiteten Text zurück
    """
    #tokenisierung des text
    tokens = word_tokenize(text.lower())
    #Interpunktionszeichen, Symbole, Sonderzeichen und Zahlen aus den Token entfernen
    filtered_tokens = [token for token in tokens if token.isalpha()]
    #Stoppwörter definieren und entfernen
    stopwords = nltk.corpus.stopwords.words("english")
    removed_tokens = [token for token in filtered_tokens if token.lower() not in stopwords]
    #lemmatisierung der Token
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in removed_tokens]
    #Token wieder zu einem String zusammenfügen
    processed_text = ' '.join(lemmatized_tokens)
    #vorverarbeiteten text zurück geben
    return processed_text


def remove_duplicates_in_lists(list1, list2):
    """
    Diese Funktion gleicht zwei Listen  ab und entfernt Elemente welche in beiden Listen vorkommen.
    Anschliessend wird eine neue Liste zurückgegeben.
    :param list1: Beliebige Liste
    :param list2: Beliebige Liste
    :return list3: Liste mit gelöschten "intersections"
    """
    set1 = set(list1)
    set2 = set(list2)
    set3 = set1.intersection(set2)
    list3 = list(set1 - set3)
    return list3

