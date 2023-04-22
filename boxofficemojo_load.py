from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import cip_library as cip

# Open the website in Chrome browser
driver = webdriver.Chrome()
#define the baseurl (as only 200 entries are shown per page we will work with the offset part of the url to  navigate through pages and get 1000 entries.
baseurl = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW&offset="
#create empty lists where data from website will be stored
rank_list = []
title_list = []
gross_list = []
#with the for loop we will create values to be inserted into the offset part of the url (values are 0,200,400,600,800)
for i in range(0,1000,200):
    #create url with dynamic offset part
    url = baseurl + str(i)
    #open the url and wait
    driver.get(url)
    driver.implicitly_wait(2)
    # Find the ranks on the site
    ranks = driver.find_elements(by=By.XPATH,
                                 value='//td[@class="a-text-right mojo-header-column mojo-truncate mojo-field-type-rank"]')
    #find the titles on the site
    titles = driver.find_elements(by=By.XPATH,
                                 value='//td[@class="a-text-left mojo-field-type-title"]')
    #find gross income on the site
    gross = driver.find_elements(by=By.XPATH,
                                  value='//td[@class="a-text-right mojo-field-type-money"]')
    #write text values from rank into previously created list
    for r in range(len(ranks)):
        rank_list.append(ranks[r].text)
    # write text values from titles into previously created list
    for t in range(len(titles)):
        title_list.append(titles[t].text)
    # write text values from gross into previously created list (as the gross income is listed three times (worldwide, domestic and foreign) and we are only interested in the worldwide gross we work with a loop to get every third value
    for g in range(0,len(gross),3):
        gross_list.append(gross[g].text)
#quit driver
driver.quit()

#create pandas dataframe containing the three lists in one column each
pd_boxofficemojo = pd.DataFrame({
    "rank": rank_list,
    "film_title": title_list,
    "gross": gross_list
})

#get Cursor
cur = cip.mariadb_connect().cursor()

#define columns and datatypes needed in new table
cols = ["id", "rank", "film_title", "gross"]
dtypes = ["INT AUTO_INCREMENT PRIMARY KEY", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)"]
#create table "boxofficemojo_raw"
cip.create_table("boxofficemojo_raw", cols, dtypes)

#write dataframe to newly created table
cip.write_to_table(df=pd_boxofficemojo, table_name="boxofficemojo_raw")

