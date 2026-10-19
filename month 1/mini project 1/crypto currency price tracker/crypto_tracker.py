from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import os
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
url = "https://coinmarketcap.com/"
try:
    driver.get(url)

    print("Opening CoinMarketCap...")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table")
        )
    )

    time.sleep(8)

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "table tbody tr"
    )

    print("Rows found:", len(rows))

    crypto_data = []

    for row in rows:
        if len(crypto_data) >= 10:
            break

        try:
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 7:
                continue

            texts = [cell.text.strip() for cell in cells]

            name = ""
            price = ""
            change_24h = ""
            market_cap = ""

            for text in texts:
                if not name and text:
                    if any(c.isalpha() for c in text):
                        name = text.split("\n")[0].strip()

            for text in texts:
                if "$" in text:
                    if not price:
                        price = text.split("\n")[0].strip()

            percentage_values = []

            for text in texts:
                if "%" in text:
                    percentage_values.append(
                        text.split("\n")[0].strip()
                    )

            if percentage_values:
                change_24h = percentage_values[-1]

            for text in texts:
                if "$" in text and text != price:
                    market_cap = text.split("\n")[0].strip()

            if name and price and "index" not in name:
                crypto_data.append({
                    "Name": name,
                    "Price": price,
                    "Change_24h": change_24h,
                    "Market_Cap": market_cap,
                    "Timestamp": datetime.now().strftime(
                                            "%Y-%m-%d %H:%M:%S"
                    )
                })

        except Exception as error:
            print("Error:", error)

finally:
    driver.quit()

if crypto_data:
    df = pd.DataFrame(crypto_data)
    df=df[["Name","Price","Change_24h","Market_Cap","Timestamp"]]

    csv_file = r"C:\Users\subasri\Desktop\cryptocurrency price tracker\month 1\mini project 1\crypto_prices_final.csv"

    if os.path.exists(csv_file):
        df.to_csv(
            csv_file,
            mode="a",
            header=False,
            index=False
        )
    else:
        df.to_csv(
            csv_file,
            index=False
        )

    print("\nData saved successfully!\n")
    print(df.to_string(index=False))
else:
    print("No cryptocurrency data found.")
