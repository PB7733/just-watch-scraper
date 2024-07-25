import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()  

options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
# options.add_argument("--headless") headless mode work but not able to fetch genre and imdb

driver = webdriver.Chrome(options=options)
driver.get("https://www.justwatch.com/in/movies?release_year_from=2000")
geners=[]
release_year=[]
movie_url=[]
imdb=[]
platform=[]
movie_title=[]
try:
    start=driver.find_elements(by=By.CLASS_NAME,value="title-list-grid__item--link")
    for i in range(50):
        start[i].click()
        try:
            driver.implicitly_wait(10)
            year=driver.find_elements(by=By.CLASS_NAME,value="release-year")
            name1=driver.find_elements(by=By.CLASS_NAME,value="title-detail-hero__details__title")
            url=driver.current_url
            imdb_1=driver.find_elements(by=By.CLASS_NAME,value="imdb-score")
            plat=driver.find_elements(by=By.CLASS_NAME,value="offer__icon")
            genre=driver.find_elements(by=By.CLASS_NAME,value="detail-infos")
            #lists_making_for_csv
            release_year.append((year[0].text)[1:5])
            movie_title.append((name1[0].text)[:-6])
            movie_url.append(str(url))
            imdb.append((imdb_1[0].text)[0:3])
            plat_temp=[]
            for k in range(len(plat)):
                plat_temp.append(plat[k].get_attribute("alt"))
            platform.append(plat_temp)
            if len(genre)==10:
                geners.append((genre[6].text)[7:])
            elif len(genre)==12:
                geners.append((genre[7].text)[7:])
            else:
                geners.append("unable to fetch genre")
            driver.back()
        except:
            release_year.append("")
            movie_title.append("")
            movie_url.append("")
            imdb.append("")
            platform.append("")
            geners.append("")
            driver.back()
    # print(release_year,movie_title,movie_url,imdb,platform,geners,sep="\n")
    information={"release_year":release_year,"movie_title":movie_title,"movie_url":movie_url,"imdb":imdb,"platform":platform,"geners":geners}
    df=pd.DataFrame(information)
    df.to_csv("output.csv",index=False)
except: 
    print("except")
    driver.close()   
   
