from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def get_imdb_top_movies():
    url = "https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc"

    # get loads webpages javascript
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    for _ in range(19):  #loads 1000 moviews by pressing the "50 more" button 20 times


        try:
            next_button = driver.find_element(By.CLASS_NAME, 'ipc-see-more__button')


            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)  # Give it a moment to scroll into view

            next_button.click()
            print("buttonpressed:", _)
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    with open('IMDBpage.html', 'w',  encoding="utf-8") as file:
        file.write(str(soup))


    driver.quit()

    movies = []
    for item in soup.select("li.ipc-metadata-list-summary-item"):
        title_tag = item.select_one("h3")
        rating_tag = item.select_one("span.ipc-rating-star--rating")
        date_tag = item.select_one("div.dli-title-metadata > span:first-child")
        MPA_tag = item.select_one("div.dli-title-metadata > span:last-child")

        if title_tag and rating_tag:
            title = title_tag.get_text(strip=True)
            rating = rating_tag.get_text(strip=True)
            date = date_tag.get_text(strip=True)
            MPA = MPA_tag.get_text(strip=True)
            movies.append((title, rating, date, MPA))

    return movies


def get_metacritic_top_movies():
    movies = []

    for page in range(42):
        url = f"https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2025&page={page+1}"

        # get loads webpages javascript
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(2)

        print("page",page)

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            with open(f'metaCriticPage{page+1}.html', 'w', encoding="utf-8") as file:
                file.write(str(soup))


            for item in soup.select("div.c-finderProductCard"):
                title_tag = item.select_one("h3")
                rating_tag = item.select_one("div.c-siteReviewScore")
                date_tag = item.select_one("div.c-finderProductCard_meta > span:first-child")
                MPA_tag = item.select_one("div.c-finderProductCard_meta > span:last-child")

                if title_tag and rating_tag:
                    title = title_tag.get_text(strip=True)
                    rating = rating_tag.get_text(strip=True)
                    date = date_tag.get_text(strip=True)
                    MPA = MPA_tag.get_text(strip=True).replace("Rated","",1)
                    movies.append((title, rating,date,MPA))
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")

        driver.quit()

    return movies


if __name__ == "__main__":

    moviesImdb = get_imdb_top_movies()
    moviesMeta = get_metacritic_top_movies()

    with open('TableIMDB_A.csv', 'w') as file:
        file.write(f"id,title,rating,date,MPA_rating\n")

    with open('TableMeta_B.csv', 'w') as file:
        file.write(f"id,title,rating,date,MPA_rating\n")


    if moviesImdb:
        id=0
        for title, rating, date, MPA in moviesImdb:
            with open('TableIMDB_A.csv', 'a') as file:
                file.write(f'A{id},"{title}",{rating},"{date}",{MPA}\n')
            id+=1

            print(f"{title}: {rating} stars, date: {date} rated: {MPA}")

    if moviesMeta:
        id = 0
        for title, rating, date, MPA in moviesMeta:
            with open('TableMeta_B.csv', 'a') as file:
                file.write(f'B{id},"{title}",{rating},"{date}",{MPA}\n')
            id += 1
            print(f"{title}: {rating} metascore, date: {date} rated: {MPA}")



