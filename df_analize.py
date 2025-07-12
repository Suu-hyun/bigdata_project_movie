# import pandas as pd
# from konlpy.tag import Okt
# import re
# from collections import Counter
#
# df = pd.read_excel('movie_review_df.xlsx', sheet_name='all_review')
#
# stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
#
# okt = Okt()
#
# def preprocess_text(text):
#     if not isinstance(text, str):
#         return ''
#     text = re.sub(r'[^가-힣\s]', '', text)
#     tokens = okt.morphs(text, stem=True)
#     tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
#     return ' '.join(tokens)
#
# df['cleaned_review'] = df['리뷰'].apply(preprocess_text)
#
# df.to_excel('movie_review_cleaned.xlsx', index=False)

# -------------------------------------- 평균 --------------------------------------------------------
# import pandas as pd
#
# # 1. 데이터 불러오기 (이미 정제된 df)
# df = pd.read_excel('movie_review_cleaned.xlsx')
#
# # 2. 영화별 평론가, 관람객 평점 평균 계산
# movie_avg = df.groupby(['영화제목', '구분'])['점수'].mean().unstack()
#
# # 3. 컬럼명 변경
# movie_avg = movie_avg.rename(columns={'관람객': '관람객 평균', '평론가': '평론가 평균'})
#
# # 4. 인덱스를 컬럼으로 변환
# movie_avg = movie_avg.reset_index()
#
# # 5. 결측치 처리 (원하면 제거 가능)
# movie_avg = movie_avg.fillna('평점 없음')
#
# print("영화별 평점 평균 (평론가 / 관람객):")
# print(movie_avg)
#
# # 6. 장르별 평론가, 관람객 평점 평균 계산 (동일하게 처리)
# genre_avg = df.groupby(['장르', '구분'])['점수'].mean().unstack()
# genre_avg = genre_avg.rename(columns={'관람객': '관람객 평균', '평론가': '평론가 평균'})
# genre_avg = genre_avg.reset_index()
# genre_avg = genre_avg.fillna('평점 없음')
#
# print("\n장르별 평점 평균 (평론가 / 관람객):")
# print(genre_avg)
#
# # 7. 엑셀로 저장 (index 제외, 깔끔하게)
# movie_avg.to_excel('movie_avg_score_by_critic_audience.xlsx', index=False)
# genre_avg.to_excel('genre_avg_score_by_critic_audience.xlsx', index=False)

# --------------------------------------- 워드 클라우드 ------------------------------------------------
# import pandas as pd
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS
# from konlpy.tag import Okt
# import re
#
# # 1. 데이터 불러오기
# df = pd.read_excel('movie_review_cleaned.xlsx')
#
# # 2. 불용어 설정 (필요한 단어는 여기에 추가)
# additional_stopwords = {
#     '영화', '감독', '배우', '장면', '스토리', '결말', '배경', '음악', '연기', '이제', '쿠키', '진짜', '그냥', '서준이', '감동'
#     '캐릭터', '씬', '사람', '내용', '장르', '평점', '관객', '평론가', '장소', '봉준호', '차라리', '액션', '이순신', '최민식', '시리즈',
#     '기대', '생각', '부분', '이야기', '때문', '것', '정도', '중간', '또한', '마블', '픽사', '정말', '윤계상', '마동석', '캐스팅',
#     '같은', '아주', '조금', '전체', '이런', '이것', '저것', '수준', '이다', '하다', '박서준', '형님', '스타', '액션 영화', '원빈'
# }
# stopwords = STOPWORDS.union(additional_stopwords)
#
# okt = Okt()
#
# # 3. 전처리 함수 (명사만 뽑고 불용어 제거)
# def preprocess_text(text):
#     if not isinstance(text, str):
#         return ''
#     text = re.sub(r'[^가-힣\s]', '', text)
#     morphs = okt.pos(text, stem=True)
#     tokens = [word for word, pos in morphs if pos == 'Noun']
#     tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
#     return ' '.join(tokens)
#
# # 4. cleaned_review 컬럼 새로 만들기 (전처리 적용)
# df['cleaned_review'] = df['리뷰'].apply(preprocess_text)
#
# import matplotlib.font_manager as fm
# import matplotlib.pyplot as plt
#
# # 한글 폰트 경로 지정
# font_path = 'C:/Windows/Fonts/malgun.ttf'
# font_prop = fm.FontProperties(fname=font_path).get_name()
#
# plt.rc('font', family=font_prop)
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
#
#
# # 5. 영화별, 구분별 워드클라우드 생성 함수
# def generate_wordcloud(data, title):
#     text = ' '.join(data.dropna())
#     if not text.strip():
#         print(f"{title} 리뷰 텍스트가 부족합니다.")
#         return
#     wc = WordCloud(
#         font_path='C:/Windows/Fonts/malgun.ttf',
#         width=800,
#         height=600,
#         background_color='white',
#         max_words=100,
#         stopwords=stopwords
#     ).generate(text)
#
#     plt.figure(figsize=(10, 8))
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis('off')
#     plt.title(title)
#     plt.show()
#
# # 6. 영화별, 평론가/관람객 분리해서 워드클라우드 출력
# movies = df['영화제목'].unique()
# for movie in movies:
#     for group in ['평론가', '관람객']:
#         subset = df[(df['영화제목'] == movie) & (df['구분'] == group)]
#         generate_wordcloud(subset['cleaned_review'], f"{movie} - {group} 워드클라우드")

# -------------------------- 가설 1 확인(t-검정) ---------------------------------
# import pandas as pd
# from scipy import stats
#
# # 데이터 불러오기
# df = pd.read_excel('movie_avg_score_by_critic_audience.xlsx')
#
# # 결측치 제거 (평론가 또는 관람객 평균이 없는 경우 제외)
# df_clean = df.dropna(subset=['관람객 평균', '평론가 평균'])
#
# # 대응표본 t-검정
# t_stat, p_value = stats.ttest_rel(df_clean['관람객 평균'], df_clean['평론가 평균'])
#
# print(f"대응표본 t-검정 결과: t-statistic = {t_stat:.3f}, p-value = {p_value:.3f}")
#
# if p_value < 0.05:
#     print("유의미한 차이가 있습니다.")
# else:
#     print("유의미한 차이가 없습니다.")

# ------------------------------------ 가설 2(괴리 시각화) ----------------------------------------------------
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import matplotlib.font_manager as fm
#
# # --- 한글 폰트 설정 (윈도우용 예: Malgun Gothic) ---
# font_path = "C:/Windows/Fonts/malgun.ttf"
# font_name = fm.FontProperties(fname=font_path).get_name()
# plt.rc('font', family=font_name)
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
#
# # 1. 장르별 관람객 평균, 평론가 평균 데이터 불러오기
# df = pd.read_excel('genre_avg_score_by_critic_audience.xlsx')
#
# print(df.head())  # 데이터 확인
#
# # 2. 점수 괴리 계산 (평론가 평균 - 관람객 평균)
# df['점수 괴리'] = df['평론가 평균'] - df['관람객 평균']
#
# # 3. 시각화
# plt.figure(figsize=(12, 7))
#
# # 관람객 평균, 평론가 평균 함께 비교하기 위한 barplot
# df_melt = df.melt(id_vars='장르', value_vars=['관람객 평균', '평론가 평균'],
#                   var_name='구분', value_name='평균 점수')
#
# sns.barplot(data=df_melt, x='장르', y='평균 점수', hue='구분')
#
# plt.title('장르별 관람객 평균 vs 평론가 평균 점수 비교')
# plt.xlabel('장르')
# plt.ylabel('평균 점수')
# plt.xticks(rotation=45)
# plt.grid(axis='y', linestyle='--', alpha=0.6)
# plt.tight_layout()
# plt.show()
#
# # 4. 점수 괴리 박스플롯 (사실 장르별 1개 값이라 박스플롯은 의미 없고, barplot으로 대체)
# plt.figure(figsize=(12, 7))
# sns.barplot(data=df, x='장르', y='점수 괴리', color='lightcoral')
# plt.title('장르별 평론가 - 관람객 점수 괴리')
# plt.xlabel('장르')
# plt.ylabel('점수 괴리')
# plt.xticks(rotation=45)
# plt.grid(axis='y', linestyle='--', alpha=0.6)
# plt.tight_layout()
# plt.show()
# -------------------------------- 가설 2(괴리 분석) ---------------------------------
# import pandas as pd
# import re
# from scipy.stats import kruskal
# import matplotlib.pyplot as plt
# import seaborn as sns
# import matplotlib.font_manager as fm
#
# # --- 한글 폰트 설정 (윈도우용 예: Malgun Gothic) ---
# font_path = "C:/Windows/Fonts/malgun.ttf"
# font_name = fm.FontProperties(fname=font_path).get_name()
# plt.rc('font', family=font_name)
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
#
# # 1. 데이터 불러오기
# df = pd.read_excel('movie_review_df.xlsx', sheet_name='all_review')
#
# # 2. 영화 제목 정규화: "_평론가" 제거 + 띄어쓰기 모두 제거해서 같은 영화로 묶기
# def normalize_title(title):
#     if isinstance(title, str):
#         title = re.sub(r'[_ ]*평론가.*$', '', title).strip()
#         title = title.replace(" ", "")  # 띄어쓰기 제거
#         return title.lower()            # 소문자 통일 (선택사항)
#     return title
#
# df['영화제목_정규화'] = df['영화제목'].apply(normalize_title)
#
# # 3. 영화별 평론가/관람객 점수를 한 행에 모으기 (pivot)
# pivot_df = df.pivot_table(
#     index=['영화제목_정규화', '장르'],
#     columns='구분',
#     values='점수',
#     aggfunc='mean'  # 평균 점수 사용
# ).reset_index()
#
# # 4. 점수 괴리 계산
# pivot_df['점수 괴리'] = pivot_df['평론가'] - pivot_df['관람객']
#
# # 5. 장르별 영화 개수 확인 후 필터링 (3편 이상만)
# genre_counts = pivot_df['장르'].value_counts()
# valid_genres = genre_counts[genre_counts >= 3].index
# df_valid = pivot_df[pivot_df['장르'].isin(valid_genres)]
#
# print(f"\n🎯 분석 대상 장르 수: {len(valid_genres)}")
# print(f"✅ 점수 괴리 데이터 샘플:\n{df_valid.head()}")
#
# if len(valid_genres) == 0:
#     print("❗ 점수 괴리 분석을 위한 장르 데이터가 부족합니다.")
# else:
#     # 6. Kruskal-Wallis 검정
#     grouped = [group['점수 괴리'].dropna().values for name, group in df_valid.groupby('장르') if not group['점수 괴리'].dropna().empty]
#
#     if len(grouped) < 2:
#         print("\n❗ Kruskal-Wallis 검정을 위한 그룹이 2개 미만입니다. 분석 불가.")
#     else:
#         stat, p = kruskal(*grouped)
#         print(f"\n📊 Kruskal-Wallis H-statistic: {stat:.4f}, p-value: {p:.4f}")
#
#     # 7. 시각화: 장르별 점수 괴리 박스플롯
#     plt.figure(figsize=(12, 7))
#     order_genres = genre_counts[genre_counts >= 3].index.tolist()
#     sns.boxplot(data=df_valid, x='장르', y='점수 괴리', order=order_genres)
#     plt.title('장르별 평론가와 관람객 점수 괴리 분포')
#     plt.xlabel('장르')
#     plt.ylabel('점수 괴리 (평론가 - 관람객)')
#     plt.xticks(rotation=45)
#     plt.grid(True, axis='y', linestyle='--', alpha=0.6)
#     plt.tight_layout()
#     plt.show()

# -------------------------------- 가설 3 -------------------------------------
# import pandas as pd
# from scipy.stats import pearsonr
# import matplotlib.pyplot as plt
#
# # 1. 데이터 불러오기
# movie_avg = pd.read_excel('movie_avg_score_by_critic_audience.xlsx')
#
# # (가정) 흥행 지표가 포함된 파일이라면
# # 예: '관객수'라는 컬럼이 있다고 가정
# # 만약 없다면 영화별 흥행 지표 데이터 합치기 필요
#
# # 2. 점수 괴리 계산
# movie_avg['점수 괴리'] = (movie_avg['평론가 평균'] - movie_avg['관람객 평균']).abs()
#
# # 3. 결측치 제거 (평점이나 흥행지표 없는 경우 제외)
# movie_avg = movie_avg.dropna(subset=['점수 괴리', '흥행지표'])
#
# # 4. 상관관계 계산 (피어슨)
# corr, p_value = pearsonr(movie_avg['점수 괴리'], movie_avg['흥행지표'])
#
# print(f"평론가-관람객 점수 괴리와 흥행지표 간 피어슨 상관계수: {corr:.4f}, p-value: {p_value:.4f}")
#
# # 5. 산점도 시각화
# plt.figure(figsize=(8,6))
# plt.scatter(movie_avg['점수 괴리'], movie_avg['흥행지표'])
# plt.xlabel('평론가-관람객 점수 괴리')
# plt.ylabel('흥행지표 (예: 관객수)')
# plt.title('점수 괴리와 흥행 간 상관관계')
# plt.grid(True)
# plt.show()