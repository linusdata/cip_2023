from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import cip_library as cip

# Chrome Browser festlegen
driver = webdriver.Chrome()
#URL definieren, von der die ID's der Filme geholt werden sollen
id_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_1000"
#leere liste erstellen, in welcher die ID's dann gespeichert werden
id_list = []
#URL öffnen und warten
driver.get(id_url)
driver.implicitly_wait(2)
# CSS elements(href), welche die links der Filme enthalten finden -> die IDs sind Teil der Links
elems = driver.find_elements(by=By.CSS_SELECTOR, value=".titleColumn [href]")
#Liste mit allen extrahierten href-Werten erstellen
links = [elem.get_attribute('href') for elem in elems]
#extrahieren der id's durch die Verwendung der definierten Funktion "extract_id()"
cip.extract_id(links, id_list)

#leere liste erstellen, in welcher die reviews dann gespeichert werden
reviews = []
#die URL erstellen, in der die Reviews für jede zuvor extrahierte ID aufgeführt sind
for i in id_list:
    review_url = "https://www.imdb.com/title/" + i + "/criticreviews/?ref_=tt_ov_rt"
    #erstellte URL öffnen und warten
    driver.get(review_url)
    driver.implicitly_wait(2)
    #Mit XPATH alle Review-Elemente für jede URL extrahieren
    review_texts = driver.find_elements(by=By.XPATH, value='//*[@id="__next"]/main/div/section/div/section/div/div[1]/div[1]/section/div/div[2]/ul/li/div/div/div[2]/div[2]')
    #die Werte für ID und Reviewtext an die reviews liste "appenden"
    for review_text in review_texts:
        reviews.append([i, review_text.text])
#driver beenden
driver.quit()

#pandas dataframe erstellen, welches die zwei listen in jeweils einer Spalte enthält
pd_reviews = pd.DataFrame(columns=["id", "review"])
for movie in reviews:
    pd_reviews = pd_reviews.append({'id': movie[0], 'review': movie[1]}, ignore_index=True)

#Cursor für mariadb holen
cur = cip.mariadb_connect().cursor()

#Spalten und Datentypen für die neue Tabelle definieren
cols = ["id", "review"]
dtypes = ["VARCHAR(255)", "VARCHAR(255)"]
#tabelle "movie_reviews_raw" erstellen
cip.create_table("movie_reviews_raw", cols, dtypes)

#dataframe in neu erstellte tabelle schreiben
cip.write_to_table(df=pd_reviews, table_name="movie_reviews_raw")

#dataframe als csv abspeichern
pd_reviews.to_csv("review_stage_1.csv", index=False)



