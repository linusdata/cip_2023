import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

url = "https://www.oscars.org/oscars/ceremonies/2023"

chrome_options = Options()
chrome_options.add_argument("--lang=en")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

award_categories = []

categories = driver.find_elements(By.XPATH, '//div[@class="view-grouping"]')

for category in categories:
    try:
        category_name = category.find_element(By.XPATH, './div[@class="view-grouping-header"]/h2').text
    except NoSuchElementException:
        continue

    winner = category.find_element(By.XPATH, './/div[@class="views-row views-row-1 views-row-odd views-row-first views-row-last"]')
    winner_name = winner.find_element(By.XPATH, './div[@class="views-field views-field-field-actor-name"]/h4').text
    winner_movie = winner.find_element(By.XPATH, './div[@class="views-field views-field-title"]/span').text

    award_categories.append({
        "category": category_name,
        "winner_name": winner_name,
        "winner_movie": winner_movie
    })

driver.quit()

awards_df = pd.DataFrame(award_categories)
awards_df.to_excel("oscar_winners_2023.xlsx", index=False)