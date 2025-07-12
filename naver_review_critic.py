from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 필요시 해제
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%9D%B8%ED%84%B0%EC%8A%A4%ED%85%94%EB%9D%BC+%EA%B4%80%EB%9E%8C%ED%8F%89&oquery=%EB%93%842+%EA%B4%80%EB%9E%8C%ED%8F%89&tqi=jbBRrlqpts0ssOlwi6sssssssSh-048406&ackey=2o6dfau2'
driver.get(url)

wait = WebDriverWait(driver, 15)

try:
    # 평론가 탭 클릭
    critic_tab = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cm_tap_area._tab_wrap ul li:nth-child(3) > a"))
    )
    critic_tab.click()

    # 탭 클릭 후 3초 이상 충분히 기다리기 (렌더링 지연 방지)
    time.sleep(4)

    # 자바스크립트로 평론가 리뷰 li 배열 가져오기
    reviews_data = driver.execute_script('''
        const items = document.querySelectorAll('div.lego_critic_outer._scroller ul.area_ulist > li');
        let result = [];
        items.forEach(item => {
            let content = item.querySelector('span.desc._text')?.innerText.trim() || "";
            let score = item.querySelector('div.area_text_box')?.innerText.trim() || "없음";
            result.push([content, score]);
        });
        return result;
    ''')

    # 리뷰 개수 확인
    print(f"스크립트로 추출한 평론가 리뷰 개수: {len(reviews_data)}")

    # CSV 저장
    with open('critic_reviews.csv', mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['리뷰내용', '평점'])
        for content, score in reviews_data:
            if content:
                writer.writerow([content, score])

    print("평론가 리뷰 CSV 저장 완료!")

except Exception as e:
    print("에러 발생:", e)

driver.quit()

## 한번씩 이상한 리뷰쓰는 곳으로 튕기곤 함 평론가 클릭해주면 끝