from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Open the website in Chrome browser
driver = webdriver.Chrome()
baseurl = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW&offset="
rank_list = []
title_list = []
gross_list = []
for i in range(0,1000,200):
    url = baseurl + str(i)
    driver.get(url)
    driver.implicitly_wait(2)
    # Find the ranks on the site
    ranks = driver.find_elements(by=By.XPATH,
                                 value='//td[@class="a-text-right mojo-header-column mojo-truncate mojo-field-type-rank"]')
    titles = driver.find_elements(by=By.XPATH,
                                 value='//td[@class="a-text-left mojo-field-type-title"]')
    gross = driver.find_elements(by=By.XPATH,
                                  value='//td[@class="a-text-right mojo-field-type-money"]')
    for r in range(len(ranks)):
        rank_list.append(ranks[r].text)
    for t in range(len(titles)):
        title_list.append(titles[t].text)
    for g in range(0,len(gross),3):
        gross_list.append(gross[g].text)
driver.quit()

print(rank_list)
print(title_list)
print(gross_list)

pd_boxofficemojo = pd.DataFrame({
    "Rank": rank_list,
    "Film Title": title_list,
    "Gross": gross_list
})

print(pd_boxofficemojo)

