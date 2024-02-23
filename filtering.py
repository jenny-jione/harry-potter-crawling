# 추천수 < 반대수인 글은 거르는 코드
import csv

# data: 2차원 리스트
def save_file(data: list, threshold: int):
    with open(f'data_filtered_{threshold}.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(['제목', '작성일', '조회수', '댓글수', '추천수', '반대수', '링크'])
        for row in data:
            wr.writerow(row)

THRESHOLD = 5

with open('data_wd.csv', 'r') as f:
    rdr = csv.reader(f)
    header = next(rdr)
    print(header)
    # 제목 | 작성일 | 조회수 | 댓글수 | 추천수 | 반대수 | 링크
    result = []
    for rd in rdr:
        like, dislike = int(rd[4]), int(rd[5])
        if like < dislike:
            continue
        if dislike > THRESHOLD:
            continue
        result.append(rd)
    result.sort(key=lambda x:int(x[4]), reverse=True)
    
    print(len(result))
    save_file(result, THRESHOLD)