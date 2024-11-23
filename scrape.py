import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def scrape_website(website):
    print("Launching Chrome browser...")

    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Check if running locally or in a cloud environment
    if os.name == 'nt':  # Running on Windows (local environment)
        print("Running on Windows (local). Using chromedriver.exe.")
        chrome_driver_path = "./chromedriver.exe"  # Path to ChromeDriver for Windows
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    else:  # Running on Linux (cloud environment)
        print("Running in cloud environment. Using chromedriver-autoinstaller.")
        chromedriver_autoinstaller.install()  # Automatically install correct version
        driver = webdriver.Chrome(options=options)

    try:
        driver.get(website)
        print("Page Loaded...")
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_don_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]

def extract_images(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    images = soup.find_all("img")
    image_urls = []
    for img in images:
        img_url = img.get("src") or img.get("data-src")
        if img_url:
            img_url = urljoin(base_url, img_url)  # Convert relative URLs to absolute
            image_urls.append(img_url)
    return image_urls
