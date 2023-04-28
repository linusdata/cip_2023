import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

chrome_options = Options()
chrome_options.add_argument("--lang=en")    #Es sind die englischen Filmtitel gewünscht.

driver = webdriver.Chrome(options=chrome_options)   #Starte Chrome auf englisch wegen den Filmtitel.
driver.get(url)

movies_list = []

table_rows = driver.find_elements(By.XPATH, '//tbody[@class="lister-list"]/tr')


#HTML-Code von dem ersten Eintrag der table_rows

#     <td class="posterColumn">
#
#     <span name="rk" data-value="1"></span>
#     <span name="ir" data-value="9.235893283491029"></span>
#     <span name="us" data-value="7.791552E11"></span>
#     <span name="nv" data-value="2728737"></span>
#     <span name="ur" data-value="-1.7641067165089712"></span>
# <a href="/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&amp;pf_rd_p=1a264172-ae11-42e4-8ef7-7fed1973bb8f&amp;pf_rd_r=HEYP96JN5R0EJFPA8P74&amp;pf_rd_s=center-1&amp;pf_rd_t=15506&amp;pf_rd_i=top&amp;ref_=chttp_tt_1"> <img src="https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_UX45_CR0,0,45,67_AL_.jpg" alt="The Shawshank Redemption" width="45" height="67">
# </a>    </td>
#     <td class="titleColumn">
#       1.
#       <a href="/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&amp;pf_rd_p=1a264172-ae11-42e4-8ef7-7fed1973bb8f&amp;pf_rd_r=HEYP96JN5R0EJFPA8P74&amp;pf_rd_s=center-1&amp;pf_rd_t=15506&amp;pf_rd_i=top&amp;ref_=chttp_tt_1" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">The Shawshank Redemption</a>
#         <span class="secondaryInfo">(1994)</span>
#     </td>
#     <td class="ratingColumn imdbRating">
#             <strong title="9,2 based on 2.728.737 user ratings">9,2</strong>
#


for row in table_rows:
    #Die Einfachen
    rank = row.find_element(By.XPATH, './td[@class="posterColumn"]/span[@name="rk"]').get_attribute("data-value")
    year = row.find_element(By.XPATH, './td[@class="titleColumn"]/span[@class="secondaryInfo"]').text.strip("()")
    rating = row.find_element(By.XPATH, './td[@class="ratingColumn imdbRating"]/strong').text
    num_votes = row.find_element(By.XPATH, './td[@class="posterColumn"]/span[@name="nv"]').get_attribute("data-value")

    #Die verschiedenen Namen auslesen.
    #Der Regisseur und die Schauspieler sind in einem String zusammengeschrieben und werden dann gesplitet.
    title_element = row.find_element(By.XPATH, './td[@class="titleColumn"]/a')
    title = title_element.text
    persons = title_element.get_attribute("title")
    director, actors = persons.split(" (dir.),") #Frank Darabont (dir.), Tim Robbins, Morgan Freeman
    actor1, actor2 = actors.strip().split(", ") #Tim Robbins, Morgan Freeman


    movie_info = {
        "rank": rank,
        "title_en": title,
        "year": year,
        "rating": rating,
        "num_votes": num_votes,
        "director": director,
        "actor1": actor1,
        "actor2": actor2,
    }

    movies_list.append(movie_info)

driver.quit()

movies_df = pd.DataFrame(movies_list)
movies_df.to_excel("imdb_top_250.xlsx", index=False)