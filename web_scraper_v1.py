# v0을 개선한 코드

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import os
from concurrent.futures import ThreadPoolExecutor

class WebCrawler:
    def __init__(self, file_name='result_data.csv', time_sleep=0.3):
        self.file_name = file_name
        self.time_sleep = time_sleep
        self.driver = None

    def initialize_driver(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def get_urls(self, file_path='data.csv'):
        with open(file_path, 'r') as f:
            rdr = csv.reader(f)
            next(rdr)
            urls = [rd[-1] for rd in rdr]
        return urls

    def get_process(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                rdr = csv.reader(f)
                next(rdr)
                complete_urls = [rd[-1] for rd in rdr]
            return complete_urls
        return []

    def get_data(self, url):
        try:
            self.driver.get(url)
            time.sleep(self.time_sleep)

            title = self.driver.find_element(By.CLASS_NAME, "title_subject").text

            info_div = self.driver.find_element(By.CLASS_NAME, "gall_writer.ub-writer")
            post_date = info_div.find_element(By.CLASS_NAME, "gall_date").text
            
            span_view = info_div.find_element(By.CLASS_NAME, "gall_count").text
            view_count = int(span_view.split()[-1])

            span_comment = info_div.find_element(By.CLASS_NAME, "gall_comment").text
            comment_count = int(span_comment.split()[-1])
            
            span_likes = info_div.find_element(By.CLASS_NAME, "gall_reply_num").text
            like_count = int(span_likes.split()[-1])

            div_dislikes = self.driver.find_element(By.CLASS_NAME, "down_num_box").text
            dislike_count = int(div_dislikes)

            info = [title, post_date, view_count, comment_count, like_count, dislike_count, url]


            return info

        except Exception as e:
            print(f"Error while processing {url}: {str(e)}")
            return None

    def crawl_urls(self, urls):
        completed = self.get_process()
        incompleted = [item for item in urls if item not in completed]

        with open(self.file_name, 'a') as f:
            wr = csv.writer(f)
            with ThreadPoolExecutor(max_workers=5) as executor:
                for i, info in enumerate(executor.map(self.get_data, incompleted)):
                    if info:
                        wr.writerow(info)

if __name__ == "__main__":
    web_crawler = WebCrawler()

    try:
        web_crawler.initialize_driver()
        urls_to_crawl = web_crawler.get_urls()

        if urls_to_crawl:
            web_crawler.crawl_urls(urls_to_crawl)

    finally:
        web_crawler.close_driver()
