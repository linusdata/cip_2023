import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import cip_library as cip


# Timer starten (für die das scrapen nicht notwendig -> aus eigenem Interesse ergänzt)
start_time = time.time()

#leere listen erstellen, in welchen die gescrapten Daten gespeichert werden.
award_winners = []
award_nominees = []

# Chrome Browser festlegen
driver = webdriver.Chrome()
#Base-URL definieren, von der die Daten zu den Oscars gescraped werden sollen (ohne Jahreszahl)
baseurl = "https://www.oscars.org/oscars/ceremonies/"
# Definieren für welchen Zeitraum die daten gescraped werden sollen. Dieser kann im Zeitraum 1929 - 2023 beliebig definiert werden.
start = 1929
end = 2023

# Anzahl Jahre berechnen die gescraped werden sollen
number_URLs = end - start + 1
#Counter für "for-Schleife" erstellen und auf 0 setzen
counter = 0


# Mit "for-Schleife" wird jedes Jahr im gewählten Zeitfenster ("start" = ..., "end" = ...) durchlaufen und die Daten gescraped.
for years in range(number_URLs):
    year = start + counter      #Jahr hochrechnen
    url = baseurl + str(year)   #URL zusammensetzen
    counter = counter + 1       #Counter hochsetzen

    # erstellte URL öffnen
    #driver = webdriver.Chrome()
    driver.get(url)

    # Mit XPATH sämtliche "div" Elemente der Klasse "view-grouping" extrahieren und in Liste "catagories" speichern.
    categories = driver.find_elements(By.XPATH, '//div[@class="view-grouping"]')

    # Mit "for-Schleife" Liste "catagories" durchlaufen und daten extrahieren.
    for category in categories:

        #Name der Kategorie extrahieren und in "category_name" zwischenspeichern.
        ## Falls kein "h2"-Element (welches unter einem "div"-Element liegt) in der Klasse "view-grouping-header" gefunden wird,
        ## wird die Fehlermeldung mit except/continue aufgefangen.
        try:
            category_name = category.find_element(By.XPATH, './div[@class="view-grouping-header"]/h2').text
        except NoSuchElementException:
            continue

        # Informationen zum Gewinner extrahieren und in "winner" zwischenspeichern.
        ## Falls kein div"-Element in der Klasse "views-row views-row-1 views-row-odd views-row-first views-row-last" gefunden wird,
        ## wird die Fehlermeldung mit except/continue aufgefangen.
        try:
            winner = category.find_element(By.XPATH, './/div[@class="views-row views-row-1 views-row-odd views-row-first views-row-last"]')
        except NoSuchElementException:
            continue

        # Gewinner und Filmtitel extrahieren und in "winner_name" und "winner_movie" zwischenspeichern.
        winner_name = winner.find_element(By.XPATH, './div[@class="views-field views-field-field-actor-name"]/h4').text
        winner_movie = winner.find_element(By.XPATH, './div[@class="views-field views-field-title"]/span').text

        # Gescrapte Informationen als Dictionary an Liste "award_winners" appenden.
        award_winners.append({
            "category": category_name,
            "name": winner_name,
            "movie": winner_movie,
            "year": year
        })

        # Informationen zum den Nominierten extrahieren und in "nominees" zwischenspeichern.
        nominees = category.find_elements(By.XPATH, './/div[contains(@class,"views-row")]')

        # Nominierte und Filmtitel extrahieren und in "nominee_name" und "nominee_movie" zwischenspeichern.
        for nominee in nominees:
            nominee_name = nominee.find_element(By.XPATH, './div[@class="views-field views-field-field-actor-name"]/h4').text
            nominee_movie = nominee.find_element(By.XPATH, './div[@class="views-field views-field-title"]/span').text

            # Gescrapte informationen als Dictionary an Liste "award_nominees" appenden.
            award_nominees.append({
                "category": category_name,
                "name": nominee_name,
                "movie": nominee_movie,
                "year": year
            })

    # Nach erfolgreichem scrapen die Jahreszahl ausgeben (Status-Update für den User)
    print(year)

# driver beenden.
driver.quit()

# Listen ind pandas Dataframe konvertieren.
df_winners = pd.DataFrame(award_winners)
df_nominees = pd.DataFrame(award_nominees)

# Dataframes mit Spalte "status" ergänzen.
df_winners['status'] = 'winner'
df_nominees['status'] = 'nominee'

# Dataframes vereinigen.
concat_list = [df_winners, df_nominees]
oscars_df = pd.concat(concat_list)

# Daten in Excel und CSV schreiben
oscars_df.to_csv("oscars_stage_1.csv", index=False)
oscars_df.to_excel("oscars_stage_1.xlsx", engine='xlsxwriter', index=False)

# Timer beenden & Dauer ausgeben
end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)
