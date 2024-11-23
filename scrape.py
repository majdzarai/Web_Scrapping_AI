import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import subprocess
from selenium.webdriver.chrome.options import Options


def install_chrome():
    """Install Chrome on Linux environments without sudo."""
    try:
        print("Installing Chrome...")
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "google-chrome-stable"], check=True)
        print("Chrome installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Chrome: {e}")
        raise e



def scrape_website(website):
    print("Launching Chrome browser...")

    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Use chromedriver_autoinstaller
    try:
        chromedriver_path = chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        driver.get(website)
        print("Page Loaded...")
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error accessing {website}: {e}")
        raise e
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
