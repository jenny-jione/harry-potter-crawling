# Estimated time of completion (ETC): 작업 완료 예상 시각
# ETC를 계산하는 코드

import time
from datetime import datetime, timedelta


def do_something():
    time.sleep(0.3)

li = [i for i in range(100)]

prev_time = datetime.now()
total = len(li)

for i, _ in enumerate(li):
    do_something()

    remaining_tasks = total - (i+1)
    current_time: datetime = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    elasped_time: timedelta = current_time - prev_time
    elasped_seconds = round(elasped_time.total_seconds(), 2)
    # Estimated Remaining Time (ERT, 남은 시간 추정)
    ert: datetime = elasped_time * remaining_tasks
    etc_raw: datetime = current_time + ert
    # Estimated Time of Completion (ETC, 작업 완료 예상 시각)
    etc = etc_raw.strftime("%Y-%m-%d %H:%M:%S")
    print(f'processing data ... {i+1}/{len(li)}\t{formatted_time}\t{elasped_seconds}\t{ert}\t{etc}')
    prev_time = current_time



"""
input: 작업해야 할 리스트
output: 현재시각, 작업완료예상시각(ETC)

예시
processing data ... 현재인덱스/전체길이  현재시각                  ETC
processing data ... 110/2156        2024-02-22 15:22:15     2024-02-22 17:20:29

ETC 계산하는 기준
남은 시간 = (현재 작업 시각 - 이전 작업 시각) * 남은 작업 개수 
ETC = 현재 시각 + 남은 시간
"""

"""
100개   4분
2000개  4*20 = 80분

1개     1~3초
2000개  2000~6000초
        = 33분~100분

1219개 시작 시각: 15:51:58
ERT: 1219초~3657초 = 20분~60분
ETC: 16:11:58~16:51:58
"""