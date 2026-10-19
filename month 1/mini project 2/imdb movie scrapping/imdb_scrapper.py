from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.imdb.com/chart/top/")

print("IMDb page opened.")
print("Waiting 30 seconds...")
time.sleep(30)

print("Loading IMDb movies...")

for i in range(30):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(1)

time.sleep(5)

movies = driver.execute_script("""
return Array.from(
    document.querySelectorAll('li.ipc-metadata-list-summary-item')
).map(li => {

    const text = li.innerText.trim();

    const imageAlts = Array.from(
        li.querySelectorAll('img')
    ).map(img => img.alt || "");

    return {
        text: text,
        imageAlts: imageAlts
    };
});
""")

print("Movie links detected:", len(movies))

data = []
seen = set()

for movie in movies:

    text = movie["text"]
    image_alts = movie["imageAlts"]

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        continue

    rank_match = re.search(r"#(\d+)", lines[0])

    if not rank_match:
        continue

    rank = int(rank_match.group(1))

    title = ""

    for line in lines:

        if line.startswith("#"):
            continue

        if re.fullmatch(r"(19|20)\d{2}", line):
            continue

        if re.fullmatch(r"\d+\s*min", line):
            continue

        if re.fullmatch(r"[0-9]\.[0-9]", line):
            continue

        if line.startswith("("):
            continue

        if line in ["Rate", "Mark as watched"]:
            continue

        title = line
        break

    year = ""

    for alt in image_alts:

        year_match = re.search(
            r"\((19\d{2}|20\d{2})\)\s*$",
            alt
        )

        if year_match:
            year = year_match.group(1)
            break

    if not year:

        year_match = re.search(
            r"\b(19\d{2}|20\d{2})\b",
            text
        )

        if year_match:
            year = year_match.group(1)

    rating = ""

    for line in lines:

        rating_match = re.fullmatch(
            r"[0-9]\.[0-9]",
            line
        )

        if rating_match:
            rating = line
            break

    if title and title not in seen:

        seen.add(title)

        data.append({
            "Rank": rank,
            "Title": title,
            "Year": year,
            "Rating": rating
        })

    if len(data) >= 250:
        break

data.sort(key=lambda x: x["Rank"])

df = pd.DataFrame(
    data,
    columns=["Rank", "Title", "Year", "Rating"]
)

df.to_csv("movies.csv", index=False)

print("IMDb Movie Rating Scraper completed successfully!")
print("Total movies scraped:", len(df))
print("CSV file created successfully.")

driver.quit()
