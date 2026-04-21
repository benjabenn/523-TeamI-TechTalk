from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

os.makedirs("apple", exist_ok=True)

# Set up the Chrome WebDriver
driver = webdriver.Chrome()

# URL of the Apple product pdfs
url = "https://www.apple.com/environment/"

driver.get(url)
time.sleep(6)  # Wait for initial page load


# Find all links that contain 'PCF' or 'pcf' in their href and download them

links = driver.find_elements(
    By.XPATH, "//a[contains(@href, '.pdf') and contains(@href, 'product')]"
)
for link in links:
    pcf_url = link.get_attribute("href")

    # Ensure the URL is correctly formatted
    if pcf_url.startswith("http"):
        response = requests.get(pcf_url)
        if response.status_code == 200:
            file_name = os.path.join("apple", pcf_url.split("/")[-1])
            with open(file_name, "wb") as f:
                f.write(response.content)
    else:
        print(f"Invalid URL: {pcf_url}")

    pdf_url = link.get_attribute("href")

    # Ensure the URL is correctly formatted
    if pdf_url.startswith("http"):
        response = requests.get(pdf_url)
        if response.status_code == 200:
            file_name = os.path.join("apple", pdf_url.split("/")[-1])
            with open(file_name, "wb") as f:
                f.write(response.content)
    else:
        print(f"Invalid URL: {pdf_url}")


driver.quit()
