# 추천/비추천 수 수집하는 코드 (가장 원본)
# 제목 | 작성일 | 조회수 | 댓글수 | 추천수 | 반대수 | 링크

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
from datetime import datetime, timedelta
import os


FILE_NAME = 'dislikes.csv'
TIME_SLEEP = 0.3


# 기존 csv 파일에서 url만 가져오는 함수
def get_urls():
    with open('data.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        urls = []
        for rd in rdr:
            # data.csv에서 가장 마지막 열이 url이라서 index=-1로 접근함.
            # csv 파일 데이터가 변경되면 여기도 수정 필요함.
            urls.append(rd[-1])
    return urls


# 중간부터 크롤링 시작할 경우 - 이미 수집한 url은 제외하는 함수
def get_process():
    with open(FILE_NAME, 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        complete_urls = [rd[-1] for rd in rdr]
    return complete_urls



# 크롤링 함수 (메인 함수)
# 제목 | 작성일 | 조회수 | 댓글수 | 추천수 | 반대수 | 링크
def get_data(driver: webdriver.Chrome, url: str):
    driver.get(url)
    time.sleep(TIME_SLEEP)

    # 제목
    title = driver.find_element(By.CLASS_NAME, "title_subject").text

    # 작성일, 조회수, 댓글수, 추천수
    # gall_writer ub-writer
    info_div = driver.find_element(By.CLASS_NAME, "gall_writer.ub-writer")
    post_date = info_div.find_element(By.CLASS_NAME, "gall_date").text
    
    span_view = info_div.find_element(By.CLASS_NAME, "gall_count").text
    view_count = int(span_view.split()[-1])

    # 댓글수
    span_comment = info_div.find_element(By.CLASS_NAME, "gall_comment").text
    comment_count = int(span_comment.split()[-1])
    
    # 추천수
    span_likes = info_div.find_element(By.CLASS_NAME, "gall_reply_num").text
    like_count = int(span_likes.split()[-1])

    # 반대수
    div_dislikes = driver.find_element(By.CLASS_NAME, "down_num_box").text
    dislike_count = int(div_dislikes)

    info = [title, post_date, view_count, comment_count, like_count, dislike_count, url]
    return info


if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    urls = get_urls()

    test_mode = False
  
    # 이미 해당 파일이 존재한다면 (크롤링 데이터가 있는 경우) => mode: a
    # 해당 파일이 존재하지 않는다면 (처음 크롤링 시작하는 경우) => mode: w

    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, FILE_NAME)

    # if로 나눈 이유: 크롤링할 url 리스트가 다르기 때문.
    # 그래서 일단 대상 url 리스트를 구하면 그 후로는 같은 파이프라인을 타게 하면 된다.

    # 파일 존재한다면 (이미 크롤링해둔 데이터가 존재하는 경우)
    if os.path.exists(file_path):
        # 크롤링 해야할 url들만 모아서 crawling & csv write 시작.
        completed = get_process()
        print('전체:', len(urls))
        print('완료:', len(completed))
        # 크롤링 미완료된 url 구하기
        # incompleted = list(set(urls)-set(completed))
        incompleted = [item for item in urls if item not in completed]

        print('미완:', len(incompleted))

    # 파일이 존재하지 않는다면 (처음 크롤링 시작하는 경우)
    else:
        with open(FILE_NAME, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['제목', '작성일', '조회수', '댓글수', '추천수', '반대수', '링크'])
            
            completed = []
            incompleted = urls[:]
    
    ##
    prev_time = datetime.now()
    total = len(incompleted)
    ##

    with open(FILE_NAME, 'a') as f:
        wr = csv.writer(f)
        for i, url in enumerate(incompleted):
            # # 현재 시각을 가져옵니다.
            # current_time = datetime.now()
            # # 원하는 형식으로 포맷팅합니다.
            # formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            # print(f'crawling data ... {i+1}/{len(incompleted)} {formatted_time}')
            info = get_data(driver, url)
            wr.writerow(info)

            ## 
            remaining_tasks = total - (i+1)
            current_time: datetime = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            elasped_time: timedelta = current_time - prev_time
            elasped_seconds = round(elasped_time.total_seconds(), 2)
            remaining_time: datetime = elasped_time * remaining_tasks
            etc_raw: datetime = current_time + remaining_time
            etc = etc_raw.strftime("%Y-%m-%d %H:%M:%S")
            print(f'processing data ... {i+1}/{len(incompleted)}\t{formatted_time}\t{elasped_seconds}\t{etc}')
            prev_time = current_time
            ##

    driver.quit()


"""
url 2156개 크롤링 시작
시작 - 14:17:40

"""


##
##로 감싸진 코드는 터미널 출력을 위한 부가 코드임. 크롤링에는 관련 없음
##
