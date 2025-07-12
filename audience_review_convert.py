import pandas as pd
import re
import os

audience_data = []

# 루트 경로 설정
root_dir = "movie_data"

# 장르별 폴더 순회
for genre in os.listdir(root_dir):
    genre_path = os.path.join(root_dir, genre)
    audience_path = os.path.join(genre_path, "audience")

    if not os.path.isdir(audience_path):
        continue

    for filename in os.listdir(audience_path):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(audience_path, filename)
        movie_title = filename.replace(".txt", "")

        with open(file_path, encoding='utf-8') as f:
            text = f.read()

        # 정규식으로 리뷰와 점수 추출
        pattern = r'(.*?)["\']?,["\']?중\)\s*\n(\d+(?:\.0)?)["\']?'
        matches = re.findall(pattern, text, re.DOTALL)

        for review, score in matches:
            review_clean = review.strip().strip('"').strip("'")
            try:
                score = float(score)
                audience_data.append({
                    '장르': genre,
                    '구분': '관람객',
                    '영화제목': movie_title,
                    '리뷰': review_clean,
                    '점수': score
                })
            except ValueError:
                continue

# 데이터프레임 생성
df = pd.DataFrame(audience_data)
df.to_excel("관람객_리뷰.xlsx", index=False)