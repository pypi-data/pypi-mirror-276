import cloudscraper


def scrape_page(url):
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
            "mobile": False,
        }
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = scraper.get(url, headers=headers)
        response.raise_for_status()

    except Exception:
        return scrape_page(url)
    return response.text
