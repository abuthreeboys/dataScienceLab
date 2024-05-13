import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def create_directory(site_url):
    """
    Create a directory for storing downloaded files.
    
    Args:
        site_url (str): The URL of the website.

    Returns:
        str: The path to the created directory.
    """
    parsed_url = urlparse(site_url)
    domain = parsed_url.netloc
    directory = os.path.join(os.getcwd(), domain)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return directory

def download_page(url, directory):
    """
    Download a web page and its assets (images, stylesheets, scripts).

    Args:
        url (str): The URL of the web page to download.
        directory (str): The directory where the downloaded files will be stored.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Download assets (images, stylesheets, scripts, etc.)
        for tag in soup.find_all(['img', 'link', 'script']):
            asset_url = urljoin(url, tag.get('src') or tag.get('href'))
            if asset_url.startswith(url):
                asset_path = os.path.join(directory, os.path.basename(asset_url))
                if not os.path.exists(asset_path):
                    with open(asset_path, 'wb') as asset_file:
                        asset_response = requests.get(asset_url)
                        if asset_response.status_code == 200:
                            asset_file.write(asset_response.content)
        
        # Save the HTML content
        page_name = urlparse(url).path.lstrip('/').replace('/', '_') or 'index.html'
        with open(os.path.join(directory, page_name), 'w', encoding='utf-8') as page_file:
            page_file.write(response.text)

def scrape_site(site_url, depth=3):
    """
    Recursively scrape a website and its pages with a specified depth.

    Args:
        site_url (str): The URL of the website to scrape.
        depth (int, optional): The maximum depth to scrape. Defaults to 3.
    """
    if depth == 0:
        return
    
    directory = create_directory(site_url)
    download_page(site_url, directory)
    
    response = requests.get(site_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            next_url = urljoin(site_url, link.get('href'))
            if next_url.startswith(site_url):
                scrape_site(next_url, depth-1)

if __name__ == "__main":
    site_url = "https://www.example.com"  # Replace with the domain name you want to scrape
    scrape_site(site_url)

```
---------------------------------------------------------------

This script will download web pages and their associated assets (e.g., images, stylesheets) from the provided domain and store them in a directory named after the domain. You can adjust the `depth` parameter to control how many levels deep the script should scrape. Be cautious when setting the `depth` to a high value, as it may download a large amount of data.

Make sure to replace `"https://www.example.com"` with the actual domain you want to scrape.

Invoke-WebRequest -Uri "https://www.preventionclinics.com/" -OutFile "index.html" -TimeoutSec 60
