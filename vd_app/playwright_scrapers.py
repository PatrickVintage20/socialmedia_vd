import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import threading

class VideoScraper:
    def __init__(self, base_url, video_url, output_filename="", audio=False):
        self.__base_url = base_url
        self.__home_directory = os.path.expanduser("~")
        __option = webdriver.FirefoxOptions()
        __option.add_argument('--headless')
        self.__driver = webdriver.Firefox(options=__option)
        self.video_url = video_url
        self.output_path = output_filename
        self.audio = audio

    def __get_download_type_element(self) -> str:
        """Gets the web element for the download button based on platform."""
        return "/html/body/div[2]/div/div/div[1]/div/div[2]/div/div[3]/p[1]/a"

    def download_video(self):
        """Scrapes and downloads the video from the platform."""
        self.__driver.get(self.__base_url)
        url_entry_field = self.__driver.find_element(By.NAME, "url")
        url_entry_field.send_keys(self.video_url)
        url_entry_field.send_keys(Keys.ENTER)

        download_btn = WebDriverWait(self.__driver, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, self.__get_download_type_element()))
        )
        download_url = download_btn.get_attribute('href')

        self.__download_file(download_url, self.output_path)

        self.__driver.close()

    def __download_file(self, url, output_path):
        """Helper function for downloading the file."""
        response = requests.get(url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

# Define functions for each social media platform
def scrape_youtube_video(video_url, output_filename=""):
    scraper = VideoScraper("https://ytb.rip/", video_url, output_filename)
    scraper.download_video()

def scrape_facebook_video(video_url, output_filename=""):
    scraper = VideoScraper("https://getfvid.com", video_url, output_filename)
    scraper.download_video()

def scrape_twitter_video(video_url, output_filename=""):
    scraper = VideoScraper("https://twdown.net", video_url, output_filename)
    scraper.download_video()

def scrape_tiktok_video(video_url, output_filename=""):
    scraper = VideoScraper("https://snaptik.app", video_url, output_filename)
    scraper.download_video()

def scrape_instagram_video(video_url, output_filename=""):
    scraper = VideoScraper("https://snapinsta.app", video_url, output_filename)
    scraper.download_video()
