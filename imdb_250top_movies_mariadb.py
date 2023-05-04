import pandas as pd
import cip_library as cip


imdb_df = pd.read_csv("imdb_top_250.csv")

# Cursor für MariaDB holen
cur = cip.mariadb_connect().cursor()

# neue Tabelle definieren
cols = ["id", "rank", "title_en", "year", "rating", "num_votes", "director", "actor1", "actor2"]
dtypes = ["VARCHAR(255)", "INT", "VARCHAR(255)", "INT", "FLOAT", "INT", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)"]

# raw Tabelle erstellen
cip.create_table("imdb_top_250_raw", cols, dtypes)

# DataFrame in neu erstellte Tabelle schreiben
cip.write_to_table(df=imdb_df, table_name="imdb_top_250_raw")

