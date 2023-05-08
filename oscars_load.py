import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import cip_library as cip

# Timer starten
start_time = time.time()

# Chrome Browser festlegen
driver = webdriver.Chrome()

#URL definieren, von der die Daten zu den Oscars gescraped werden sollen
baseurl = "https://www.oscars.org/oscars/ceremonies/"

#leere listen erstellen, in welcher die ID's dann gespeichert werden
award_winners = []
award_nominees = []

#Definieren für welchen Zeitraum die daten gescraped werden sollen (1929 - 2023)
start = 1929
end = 2023
# Anzahl Jahre ausrechnen welche gescraped werden sollen
number_URLs = end - start + 1
#Counter für "for-Schleife" erstellen
counter = 0



# Mit der "for-Schleife" wird durch jedes Jahr zwischen 1929 - 2023 iteriert und die daten gescraped.
for years in range(number_URLs):
    year = start + counter      #Jahr hochrechnen
    url = baseurl + str(year)   #URL zusammensetzen
    counter = counter + 1       #Counter hochsetzen

    # erstellte URL öffnen und warten
    driver = webdriver.Chrome()
    driver.get(url)

    ################### Daten von www.Oscars.org extrahieren ###################

    # Die Daten können mit XPATH blockweise für jede Oscar Kategorie gescraped werden. Dazu werden die Klassen genommen welche "view-grouping" enthalten
    # Diese Einträge werden in die Liste "categories" gespeichert.
    categories = driver.find_elements(By.XPATH, '//div[@class="view-grouping"]')  # '//div[@class="view-grouping"]'

    # Mit "for-Schleife" durch die einzelnen "Blöcke" welche in der Liste "categories" gespeichert sin iterieren.
    for category in categories:


        # Weil in der liste "categories" weitere werte abgespeichert werden als die "grouping-header" muss mit "try,except,continue"
        # in die nächste iteration deszählers gesprungen werden
        try:
            category_name = category.find_element(By.XPATH, './div[@class="view-grouping-header"]/h2').text
        except NoSuchElementException:
            continue

        # Weil dieser XPAth in vereinzelten Jahren nicht gefunden wurde, muss hier auch mit einem "try,except,continue" gearbeitet werden
        try:
            winner = category.find_element(By.XPATH, './/div[@class="views-row views-row-1 views-row-odd views-row-first views-row-last"]')
        except NoSuchElementException:
            continue

        # "winner_name" und "winner_movie" extrahieren
        winner_name = winner.find_element(By.XPATH, './div[@class="views-field views-field-field-actor-name"]/h4').text
        winner_movie = winner.find_element(By.XPATH, './div[@class="views-field views-field-title"]/span').text

        # Alle informationen zum Oscar Gewinner in ein Dictionarry schreiben
        award_winners.append({
            "category": category_name,
            "name": winner_name,
            "movie": winner_movie,
            "year": year
        })

        # Extract Oscar Nominees from www.Oscars.org
        nominees = category.find_elements(By.XPATH, './/div[contains(@class,"views-row")]')

        for nominee in nominees:
            nominee_name = nominee.find_element(By.XPATH, './div[@class="views-field views-field-field-actor-name"]/h4').text
            nominee_movie = nominee.find_element(By.XPATH, './div[@class="views-field views-field-title"]/span').text

            award_nominees.append({
                "category": category_name,
                "name": nominee_name,
                "movie": nominee_movie,
                "year": year
            })

    driver.quit()
    print(year)

# convert the list into a dataframe
df_winners = pd.DataFrame(award_winners)

# convert the list into a dataframe
df_nominees = pd.DataFrame(award_nominees)

df_winners['status'] = 'winner'
df_nominees['status'] = 'nominee'

concat_list = [df_winners, df_nominees]
oscars_df = pd.concat(concat_list)

oscars_df.to_csv("oscars_stage_1.csv", index=False)
oscars_df.to_excel("oscars_stage_1.xlsx", engine='xlsxwriter', index=False)

#Cursor für mariadb holen
##cur = cip.mariadb_connect().cursor()

#Spalten und Datentypen für die neue Tabelle definieren
##cols = ["category", "name", "movie", "status"]
##dtypes = ["VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)"]


#tabelle "movie_reviews_raw" erstellen
##cip.create_table("oscars_raw", cols, dtypes)


##oscars_df.to_csv("oscars_load.csv", index=False)
##oscars_df.to_excel("oscars_load.xlsx", engine='xlsxwriter', index=False)

#dataframe in neu erstellte tabelle schreiben
##cip.write_to_table(df=oscars_df, table_name="oscars_raw")


# stop the timer
end_time = time.time()
# calculate the elapsed time
elapsed_time = end_time - start_time
print(elapsed_time)