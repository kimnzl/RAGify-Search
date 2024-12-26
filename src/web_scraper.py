import asyncio
import aiohttp
import os
import urllib.parse
from googlesearch import search
from bs4 import BeautifulSoup
from config import REQUESTS_HEADER

# Function to encode URL for filename
def encode_url_to_filename(url):
    return urllib.parse.quote(url, safe="") + ".html"

# Function to decode filename back to URL
def decode_filename_to_url(filename):
    return urllib.parse.unquote(filename[:-5])  # Remove ".html" and decode

# Function to fetch and save a single page
async def fetch_and_save(session, url, folder):
    try:
        filename = encode_url_to_filename(url)
        filepath = os.path.join(folder, filename)

        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            text = soup.find("body").get_text(strip=True)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
            print(f"Saved: {filepath}")
    except Exception:
        return f"Failed to fetch or save for url: {url}"


# Function to download all pages
async def fetch_web_pages(query, download_dir: str = "./downloaded"):
    urls = search(query, lang="en", region="us")
    # Ensure the folder exists
    os.makedirs(download_dir, exist_ok=True)

    async with aiohttp.ClientSession(headers=REQUESTS_HEADER) as session:
        tasks = [fetch_and_save(session, url, download_dir) for url in urls]
        await asyncio.gather(*tasks)

def remove_temp_files(download_dir: str = "./downloaded"):
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        os.remove(file_path)
