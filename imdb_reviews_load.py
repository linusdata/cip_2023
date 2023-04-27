from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import cip_library as cip

# Open the website in Chrome browser
driver = webdriver.Chrome()
#define the url where we get the id's of the movies
id_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_1000"
#create an empty list where the id's will be stored
id_list = []
# open the url and wait
driver.get(id_url)
driver.implicitly_wait(2)
# Find the CSS elements (href) containing the links of the movies -> id's are part of the links.
elems = driver.find_elements(by=By.CSS_SELECTOR, value=".titleColumn [href]")
#create list containing all extracted href values.
links = [elem.get_attribute('href') for elem in elems]
#extract id's from the href values using the function "extract_id()"
cip.extract_id(links, id_list)

#create an empty list where the id's will be stored
reviews = []
#create the url where the reviews are listed for each id extracted before
for i in id_list:
    review_url = "https://www.imdb.com/title/" + i + "/criticreviews/?ref_=tt_ov_rt"
    #open the created url and wait
    driver.get(review_url)
    driver.implicitly_wait(2)
    #using XPATH we are going to extract all review elements for each url
    review_texts = driver.find_elements(by=By.XPATH, value='//*[@id="__next"]/main/div/section/div/section/div/div[1]/div[1]/section/div/div[2]/ul/li/div/div/div[2]/div[2]')
    #append the id and review text values to the review list and
    for review_text in review_texts:
        reviews.append([i, review_text.text])
#quit the driver
driver.quit()

#create pandas dataframe containing the three lists in one column each
pd_reviews = pd.DataFrame(columns=["id", "review"])
for movie in reviews:
    pd_reviews = pd_reviews.append({'id': movie[0], 'review': movie[1]}, ignore_index=True)

#get Cursor for mariadb
cur = cip.mariadb_connect().cursor()

#define columns and datatypes needed in new table
cols = ["id", "review"]
dtypes = ["VARCHAR(255)", "VARCHAR(255)"]
#create table "boxofficemojo_raw"
cip.create_table("movie_reviews_raw", cols, dtypes)

#write dataframe to newly created table
cip.write_to_table(df=pd_reviews, table_name="movie_reviews_raw")





