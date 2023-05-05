import pandas as pd
from cip_library import delete_random_data


# Anzeigeoptionen ändern
pd.set_option("display.max_columns", None)  # Alle Spalten anzeigen
#pd.set_option("display.max_rows", None)     # Alle Zeilen anzeigen
pd.set_option("display.expand_frame_repr", False) # Zeilenumbruch verhindern

# Excel-Datei importieren
top250 = pd.read_csv("imdb_top_250.csv")

# Den DataFrame anzeigen
print(top250)

top250 = delete_random_data(top250)

print(top250)

#Das CSV wird überschrieben.

top250.to_csv("imdb_top_250.csv", index=False)