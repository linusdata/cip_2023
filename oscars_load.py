import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.chrome.options import Options
import time
import cip_library as cip

baseurl = "https://www.oscars.org/oscars/ceremonies/"


# start the timer
start_time = time.time()


start = 2022 #1929
end = 2023 #2023
number_URLs = end - start
counter = 0

award_winners = []
award_nominees = []

for years in range(number_URLs):
    year = start + counter
    url = baseurl + str(year)
    counter = counter + 1

    driver = webdriver.Chrome()
    driver.get(url)

    categories = driver.find_elements(By.XPATH, '//div[@class="view-grouping"]')  # '//div[@class="view-grouping"]'

    # Extract Oscar Winners from www.Oscars.org

    for category in categories:
        try:
            category_name = category.find_element(By.XPATH,
                                                  './div[@class="view-grouping-header"]/h2').text  # './div[@class="view-grouping-header"]/h2'
        except NoSuchElementException:
            continue

        try:
            winner = category.find_element(By.XPATH,
                                           './/div[@class="views-row views-row-1 views-row-odd views-row-first views-row-last"]')
        except NoSuchElementException:
            continue
        winner_name = winner.find_element(By.XPATH, './div[@class="views-field views-field-field-actor-name"]/h4').text
        winner_movie = winner.find_element(By.XPATH, './div[@class="views-field views-field-title"]/span').text

        award_winners.append({
            "category": category_name,
            "name": winner_name,
            "movie": winner_movie,
            "year": year
        })

        # Extract Oscar Nominees from www.Oscars.org
        nominees = category.find_elements(By.XPATH, './/div[contains(@class,"views-row")]')
        nominee_list = []
        for nominee in nominees:
            nominee_name = nominee.find_element(By.XPATH,
                                                './div[@class="views-field views-field-field-actor-name"]/h4').text
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


oscars_df.to_excel("oscars_load.xlsx", engine='xlsxwriter', index=False)

#Cursor für mariadb holen
cur = cip.mariadb_connect().cursor()

#Spalten und Datentypen für die neue Tabelle definieren
cols = ["category", "name", "movie", "status"]
dtypes = ["VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)"]
#tabelle "movie_reviews_raw" erstellen
cip.create_table("oscars_raw", cols, dtypes)

#dataframe in neu erstellte tabelle schreiben
cip.write_to_table(df=oscars_df, table_name="oscars_raw")





# stop the timer
end_time = time.time()
# calculate the elapsed time
elapsed_time = end_time - start_time
print(elapsed_time)