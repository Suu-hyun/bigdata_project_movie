import pandas as pd
import os

critic_data = []
root_dir = "movie_data"

for genre in os.listdir(root_dir):
    genre_path = os.path.join(root_dir, genre)
    critic_path = os.path.join(genre_path, 'critic')
    if not os.path.isdir(critic_path):
        continue

    for filename in os.listdir(critic_path):
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(critic_path, filename)
        movie_title = filename.replace('.txt', '')

        with open(file_path, encoding='utf-8') as f:
            lines = f.read().strip().split('\n')

        for line in lines:
            parts = line.rsplit(',', 1)
            if len(parts) != 2:
                continue
            review = parts[0].strip()
            score_raw = parts[1].strip()
            if score_raw.startswith('"') and score_raw.endswith('"'):
                try:
                    score = float(score_raw[1:-1])
                    critic_data.append({
                        '장르': genre,
                        '구분': '평론가',
                        '영화제목': movie_title,
                        '리뷰': review,
                        '점수': score
                    })
                except ValueError:
                    continue

df_critic = pd.DataFrame(critic_data)
df_critic.to_excel("평론가_리뷰.xlsx", index=False)