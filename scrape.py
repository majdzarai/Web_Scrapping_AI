import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(website):
    print("Lunching chrome browser ...")
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver  = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page Loaded ...")
        html= driver.page_source
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




def split_don_content (dom_content, max_lenght=6000):
    return[
        dom_content[i: i + max_lenght] for i in range(0, len(dom_content), max_lenght)
    ]


from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_images(html_content, base_url):
    
    soup = BeautifulSoup(html_content, "html.parser")
    images = soup.find_all("img")

    image_urls = []
    for img in images:
        # Get image URL from 'src' or 'data-src' attributes
        img_url = img.get("src") or img.get("data-src")
        if img_url:
            # Convert relative URLs to absolute URLs
            img_url = urljoin(base_url, img_url)
            image_urls.append(img_url)
    return image_urls

