import cip_library as cip
import pandas as pd

# Lesen von Daten aus dem CSV -File "oscars_stage_1" und speichern der Daten in einem dataframe.
df_oscars_transform = pd.read_csv('oscars_stage_1.csv')

# Daten nach absteigender Reihenfolge in der Spalte "status" sortieren.
df_oscars_transform_sort = df_oscars_transform.sort_values(by= ['status'], ascending=False)

# Duplikate löschen (das erste Element wird behalten, die übrigen gelöscht)
df_oscars_transform_1 = df_oscars_transform_sort.drop_duplicates(subset=['category', 'name', 'movie', 'year'], keep = 'first')

# Liste erstellen mit allen unterschiedlichen Kategorien
categories = list(df_oscars_transform_1['category'].unique())

# Festlegen bei welchen Kategorien die Spalten "category" & "name" nicht getauscht werden sollen.
categories_to_keep = ['ACTOR', 'ACTOR IN A LEADING ROLE', 'ACTOR IN A SUPPORTING ROLE','ACTRESS',
                      'ACTRESS IN A LEADING ROLE', 'ACTRESS IN A SUPPORTING ROLE']

# Festlegen bei welchen Kategorien die Spalten "category" & "name" getauscht werden sollen.
categories_to_swap = cip.remove_duplicates_in_lists(categories,categories_to_keep)

# Spalten "category" & "name" tauschen.
for cat in categories_to_swap:
    df_temp = df_oscars_transform_1['category'] == cat
    df_oscars_transform_1.loc[df_temp, ['name', 'movie']] = df_oscars_transform_1.loc[df_temp, ['movie', 'name']].values

# Kopie des Dataframe erstellen (Verhindert Fehlermeldung beim bereinigen der Filmtitel).
df_oscars_transform_2 = df_oscars_transform_1.copy()

# Film Titel bereinigen.
cip.clean_film_title(df_oscars_transform_2, "movie")

# Einträge mit denselben Werten in «year», «status» & «film_title» zählen und zusammenfassen.
df_count = pd.DataFrame(df_oscars_transform_2[['year','status','film_title_cleaned']].value_counts()).reset_index()

# Spalten umbenennen
df_count_1 = df_count.rename(columns={0:'number', 'film_title_cleaned':'movie'})

# Dataframe mit allen "winner"" erstellen
df_win = df_count_1.loc[df_count['status'] == 'winner'].rename(columns={'number':'number_W'})

# Dataframe mit allen "nominees"" erstellen
df_nom = df_count_1.loc[df_count['status'] == 'nominee'].rename(columns={'number':'number_N'})

# Status aus Dataframes entfernen.
df_win_dropped = df_win.drop('status', axis=1)
df_nom_dropped = df_nom.drop('status', axis=1)

# Dataframe nach "movie" & "year" mergen
df_oscars_final = pd.merge(df_win_dropped, df_nom_dropped, how = 'outer', on=['year', 'movie'])

# Alla NaN Werte mit 0 auffüllen.
df_oscars_final.fillna(0, inplace=True)

# Spalten umbenennen
df_oscars_final = df_oscars_final.rename(columns={'count_x':'number_W'})
df_oscars_final = df_oscars_final.rename(columns={'count_y':'number_N'})

# Datentyp zu integer ändern
df_oscars_final['number_W'] = df_oscars_final['number_W'].astype(int)
df_oscars_final['number_N'] = df_oscars_final['number_N'].astype(int)

# Neue spalte mit demder Summevon Nominationen und Gewinnen erstellen
df_oscars_final['number_W+N'] =  df_oscars_final['number_W'] + df_oscars_final['number_N']

# Daten in Excel und CSV schreiben
df_oscars_final.to_csv("oscars_stage_3.csv", index=False)
df_oscars_final.to_excel("oscars_stage_3.xlsx", engine='xlsxwriter', index=False)

# Cursor für mariadb holen
cur = cip.mariadb_connect().cursor()

#S palten und Datentypen für die neue Tabelle definieren
cols = ["year", "movie", "number_W", "number_N", "number_WN"]
dtypes = ["INT", "VARCHAR(50)", "INT", "INT", "INT"]

# Tabelle "oscars_stage_3" erstellen
cip.create_table("oscars_stage_3", cols, dtypes)
# Dataframe in neu erstellte tabelle schreiben
cip.write_to_table(df=df_oscars_final, table_name="oscars_stage_3")