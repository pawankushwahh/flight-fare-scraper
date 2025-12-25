import time
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver import get_driver

# ---------------- CONFIG ----------------
ORIGIN = "DEL"
DESTINATION = "BOM"
TRAVEL_DATE = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

URL = (
    "https://www.goindigo.in/booking/"
    f"?origin={ORIGIN}&destination={DESTINATION}"
    f"&date={TRAVEL_DATE}&tripType=ONE_WAY&passengers=1"
)

print("🔗 URL:", URL)

# --------------------------------------

driver = get_driver(headless=False)
wait = WebDriverWait(driver, 40)

try:
    print("🌐 Opening IndiGo search page...")
    driver.get(URL)

    # Let page JS settle
    time.sleep(10)

    print("🔍 Waiting for fare element...")

    # Try multiple possible price selectors (fallback strategy)
    price_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//span[contains(text(),'₹')]")
        )
    )

    print(f"💡 Found {len(price_elements)} price elements")

    for p in price_elements[:5]:
        print("💰 Price candidate:", p.text)

except Exception as e:
    print("❌ Error occurred:", e)

finally:
    print("⏳ Waiting before closing browser...")
    time.sleep(20)
    driver.quit()
