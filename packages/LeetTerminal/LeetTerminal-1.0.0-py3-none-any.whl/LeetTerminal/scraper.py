import json
from bs4 import BeautifulSoup
from .tools import *
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_links(url):
    """
    Returns a list of problems with name and links.
    """
    response = scrape_page(url)

    soup = BeautifulSoup(response, "html.parser")

    problem_links = soup.find_all("a", href=True)
    problem_hrefs = [
        a["href"] for a in problem_links if a["href"].startswith("/problems/")
    ]

    return problem_hrefs


def get_problems(url):
    """
    Returns all questions on a given page.
    """
    response = scrape_page(url)

    soup = BeautifulSoup(response, "html.parser")
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    json_data = json.loads(script_tag.string)

    def _extract_problems(json_data):
        # Extract problem names and other relevant details
        problems = []
        study_plans = json_data["props"]["pageProps"]["dehydratedState"]["queries"][0][
            "state"
        ]["data"]["studyPlanV2Detail"]["planSubGroups"]
        for plan in study_plans:
            for question in plan["questions"]:
                problems.append(
                    {
                        "title": question["title"],
                        "slug": question["titleSlug"],
                        "difficulty": question["difficulty"],
                    }
                )
        return problems

    return _extract_problems(json_data)


def scrape_description(url):
    """
    Retruns given problem description.
    """
    try:
        chrome_options = Options()
        devnull = open(os.devnull, "w")
        original_stderr = os.dup(2)
        os.dup2(devnull.fileno(), 2)
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

        driver.get(url)
        problem_description_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-track-load='description_content']")
            )
        )  # Extract the text from the element
        problem_description = problem_description_element.text
        os.dup2(original_stderr, 2)
        devnull.close()

        return problem_description
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
    return None
