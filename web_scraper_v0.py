# 원본 코드

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import os


FILE_NAME = 'result_data.csv'
TIME_SLEEP = 0.3


def get_urls():
    with open('data.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        urls = []
        for rd in rdr:
            urls.append(rd[-1])
    return urls


def get_process():
    with open(FILE_NAME, 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        complete_urls = [rd[-1] for rd in rdr]
    return complete_urls


def get_data(driver: webdriver.Chrome, url: str):
    driver.get(url)
    time.sleep(TIME_SLEEP)

    title = driver.find_element(By.CLASS_NAME, "title_subject").text

    info_div = driver.find_element(By.CLASS_NAME, "gall_writer.ub-writer")
    post_date = info_div.find_element(By.CLASS_NAME, "gall_date").text
    
    span_view = info_div.find_element(By.CLASS_NAME, "gall_count").text
    view_count = int(span_view.split()[-1])

    span_comment = info_div.find_element(By.CLASS_NAME, "gall_comment").text
    comment_count = int(span_comment.split()[-1])
    
    span_likes = info_div.find_element(By.CLASS_NAME, "gall_reply_num").text
    like_count = int(span_likes.split()[-1])

    div_dislikes = driver.find_element(By.CLASS_NAME, "down_num_box").text
    dislike_count = int(div_dislikes)

    info = [title, post_date, view_count, comment_count, like_count, dislike_count, url]
    return info


if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    urls = get_urls()

    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, FILE_NAME)

    if os.path.exists(file_path):
        completed = get_process()
        incompleted = [item for item in urls if item not in completed]

    else:
        with open(FILE_NAME, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['제목', '작성일', '조회수', '댓글수', '추천수', '반대수', '링크'])
            
            completed = []
            incompleted = urls[:]
    
    with open(FILE_NAME, 'a') as f:
        wr = csv.writer(f)
        for i, url in enumerate(incompleted):
            info = get_data(driver, url)
            wr.writerow(info)

    driver.quit()