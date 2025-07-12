from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv

# 셀레니움 드라이버 설정
options = webdriver.ChromeOptions()
# 헤드리스 모드 꺼짐
# options.add_argument('--headless')  # 브라우저 없이 실행을 원하면 이 줄을 주석처리하거나 삭제

options.add_argument('--disable-gpu')  # GPU 비활성화 (Optional)
options.add_argument('--no-sandbox')  # Sandbox 모드 비활성화 (Optional)

# 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 제공된 URL 그대로 사용 (기생충 영화 리뷰 페이지)
url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=1821761&qvt=0&query=%EB%B8%94%EB%A0%88%EC%9D%B4%EB%93%9C%20%EB%9F%AC%EB%84%88%202049%20%EA%B4%80%EB%9E%8C%ED%8F%89'

# 페이지로 이동
driver.get(url)

# 페이지가 로드될 때까지 기다리기
wait = WebDriverWait(driver, 10)

# 리뷰 영역이 로드될 때까지 기다리기
try:
    # 정확한 셀렉터를 사용하여 리뷰 영역 찾기
    review_section = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.lego_review_list._scroller > ul.area_card_outer._item_wrapper'))
    )

    # 리뷰 창을 찾기 (스크롤할 영역)
    review_scroll_div = review_section

    # 페이지 내에서 스크롤 가능한 요소를 더 정확하게 찾기 위해 페이지 스크롤의 범위를 늘림
    last_height = driver.execute_script("return arguments[0].scrollHeight", review_scroll_div)

    # 최대 200개의 리뷰를 가져올 때까지 스크롤
    reviews = set()  # 중복을 제거하기 위해 set 사용
    while len(reviews) < 200:
        # 스크롤 내리기
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_scroll_div)
        time.sleep(random.uniform(5, 8))  # 딜레이 주기

        # 스크롤 후 새로운 높이 측정
        new_height = driver.execute_script("return arguments[0].scrollHeight", review_scroll_div)

        # 스크롤이 끝까지 내려갔을 때 페이지 높이가 바뀌지 않으면 멈춤
        if new_height == last_height:
            break
        last_height = new_height

        # 리뷰 요소 가져오기 (스크롤 후 리뷰 추출)
        review_elements = driver.find_elements(By.CSS_SELECTOR, 'li.area_card._item')
        for review in review_elements:
            # 리뷰 제목 가져오기
            title = review.get_attribute('data-report-title').strip()
            # 리뷰 점수 가져오기 (실제 점수 부분)
            try:
                score_element = review.find_element(By.CSS_SELECTOR, 'div.area_text_box > span.blind')
                score = review.find_element(By.CSS_SELECTOR, 'div.area_text_box').text.strip().split(' ')[-1]  # 숫자만 추출
            except:
                score = '없음'  # 점수가 없는 경우 기본값

            # 중복이 아닌 경우에만 추가
            if title:
                reviews.add((title, score))  # 리뷰 제목과 점수를 튜플로 저장

            if len(reviews) >= 200:
                break

    # CSV 파일로 저장
    with open('movie_reviews_with_scores.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Review', 'Score'])  # CSV 파일 헤더
        for review, score in reviews:
            writer.writerow([review, score])  # 리뷰 제목과 점수 데이터 저장

    print(f"총 {len(reviews)}개의 리뷰와 점수를 CSV 파일에 저장했습니다.")
    # 리뷰 출력
    for idx, (review, score) in enumerate(reviews, 1):
        print(f'{idx}. {review} (점수: {score})')

except Exception as e:
    print(f"Error: {e}")

# 브라우저 종료
driver.quit()

## URL만 바꾸기만하면됨 다만 수동으로 스크롤 해줘야함