### 에러 일지 - 24.2.21

page 35 크롤링 도중 아래처럼 에러가 발생했다.

```
page=35 crawling ...
Traceback (most recent call last):
  File "/Users/jangjione/workspace/jenny/harrypotter/main.py", line 115, in <module>
    data = get_data(driver, page)
  File "/Users/jangjione/workspace/jenny/harrypotter/main.py", line 43, in get_data
    reply_count = int(a_tags[1].text[1:-1])
ValueError: invalid literal for int() with base 10: '14/1'
```
#### 원인
1. 대부분의 게시물의 경우 제목 뒤에 아래처럼 댓글 수가 표시된다.
    ```
    해리포터 주문 정리 [7]
    ```
2. 그러나 보이스리플이 있는 경우 아래처럼 표시 형식이 달라진다. [일반 리플/보이스 리플]
    ```
    해리포터 주문 정리 [14/1]
    ```
- 1번의 경우만 고려했을 때 사용했던 코드:
    ```python
    int(a_tags[1].text[1:-1])
    ```
    위 코드로 2번 경우를 크롤링 할 경우에 나오는 에러였다.
<br><br>
- 그래서 아래와 같이 코드를 수정.
    ```python
    repl_raw = a_tags[1].text
    if '/' in repl_raw:
        reply_count = int(repl_raw[1:].split('/')[0])
    else:
        reply_count = int(a_tags[1].text[1:-1])
    ```