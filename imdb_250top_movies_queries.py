import pandas as pd
import cip_library as cip

# Cursor-MariaDB
cur = cip.mariadb_connect().cursor()

# SQL-Abfrage, welcher Schauspieler wird am meisten oft erwähnt in den besten 250 Filmen?
#Actor 1 und Actor 2 zusammenfassen als all_actors
sql_query1 = '''
    SELECT actor, COUNT(*) AS num_movies
    FROM (
        SELECT actor1 AS actor FROM imdb_top_250_raw
        UNION ALL
        SELECT actor2 AS actor FROM imdb_top_250_raw
    ) AS all_actors
    GROUP BY actor
    ORDER BY num_movies DESC
'''

cur.execute(sql_query1)
result = cur.fetchall()
column_names = [desc[0] for desc in cur.description]
actor_counts_df = pd.DataFrame(result, columns=column_names)

print(actor_counts_df)