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
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from konlpy.tag import Okt
import re

# 1. 데이터 불러오기
df = pd.read_excel('movie_review_cleaned.xlsx')

# 2. 불용어 설정 (필요한 단어는 여기에 추가)
additional_stopwords = {
    '영화', '감독', '배우', '장면', '스토리', '결말', '배경', '음악', '연기', '이제', '쿠키', '진짜', '그냥',
    '서준이', '감동', '캐릭터', '씬', '사람', '내용', '장르', '평점', '관객', '평론가', '장소', '봉준호', '차라리',
    '액션', '이순신', '최민식', '시리즈', '기대', '생각', '부분', '이야기', '때문', '것', '정도', '중간', '또한',
    '마블', '픽사', '정말', '윤계상', '마동석', '캐스팅', '같은', '아주', '조금', '전체', '이런', '이것', '저것',
    '수준', '이다', '하다', '박서준', '형님', '스타', '액션 영화', '원빈', '한국', '강동원', '김윤석', '시대',
    '트럼프', '디즈니', '뮤지컬', '노래', '기생충', '송강호', '히어로', '캡틴', '빌런', '파트', '티모시', '영화관',
    '아이맥스', '애니', '투슬 리스(투슬리스)', '디카프리오', '레버넌트', '해전', '완전', '이순신장군', '마블리',
    '조선족', '라이트', '베이비', '프랜차이즈', '자동차', '과학', '역시', '질문', '작품', '속편', '전작', '하나',
    '이번', '순간', '의미', '오늘', '판타지', '가장', '웹툰', '원작', '김용화', '아저씨', '다시', '보고', '몇번',
    '지니', '기술', '자스민', '알라딘', '윌스미스', '아이', '미국', '대한', '어스', '조던', '아웃', '겟아웃', '원소',
    '엘리', '우리', '서로', '이드', '컬래버', '세이건', '크게', '년대', '익스펜더블', '아놀드', '왕년', '출연', '대박',
    '브루스', '모든', '놀란', '인간', '호아킨 피닉스', '토드 필립스', '조커', '코미디', '배트맨', '호아킨', '히스 레저',
    '파라', '공포 영화', '알바', '카메론', '제임스', '반드시', '블록버스터', '후의', '타이타닉', '명작', '재개', '봉하',
    '광주', '연출', '토마스', '로봇', '변신', '분명', '소년', '합체', '상영', '시간', '옵티머스', '마이클 베이',
    '범블비', '마무리', '잠시', '반지 제왕', '호빗', '전투', '박소', '소담', '동안', '화보', '라푼젤', '동화', '다른', '화룡', '장담', '엘사', '애니메이션', '계획', '무엇', '월드', '확장', '지점', '설국열차', '김기영', '입안',
'내내', '미즈', '모니카', '노스', '브리', '라슨', '마블스', '자주', '구스', '캡틴마블', '느낌', '고양이', '사막', '샬라메', '드니 빌뇌브', '상미', '극장', '영상',
'처음', '실사', '화의', '투슬 리스', '투스리스', '루베', '오스카', '엠마누엘', '레오', '해상', '신의', '장군', '한번', '올해', '범죄', '베테', '꿀잼', '드라이버',
'거의', '에드가', '운전', '분노', '질주', '우주', '다음', '정체', '빌뇌브', '독자', '전편', '후속작', '이해', '닥터', '피트', '뮤직', '지금', '태식', '흐름', '옆집', '이영화',
'이정범', '번은', '우리나라', '액션영화', '개봉', '상미', '공주', '알라딘', '공포', '여러', '오직', '게다가', '얼마나', '공포영화', '다른', '엠버', '멘탈', '제발', '웨이드', '눈물',
'혼자', '전설', '자리', '이연걸', '실베스터', '스트레스', '피닉스', '토드 필립스', '공포영화', '컨저링', '개봉', '로즈', '극장', '언제', '외부', '피터', '택시운전사',
'트랜스포머', '메간폭스', '마이클', '반지의제왕', '만큼', '드라마', '더빙', '안나', '리산알 가입', '리산 가입', '투슬 리스', '슈퍼히어로', '오프닝', '하드캐리', '마지막',
'농담', '강추', '가족영화', '이건', '인터스텔라', '토드', '필립스', '토드 필립스', '토드필립스', '택시 운전사', '대한민국', '고민', '패자',
'장료', '러싼', '여기', '마지막', '폴른', '미군', '베이', '마지막', '레골라스', '추천', '면서', '돼지', '호러영화', '로서', '알리', '반지하', '드니', '동시', '엑소시스트'
}
stopwords = STOPWORDS.union(additional_stopwords)

okt = Okt()

# 3. 전처리 함수 (명사만 뽑고 불용어 제거)
def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'[^가-힣\s]', '', text)
    morphs = okt.pos(text, stem=True)
    tokens = [word for word, pos in morphs if pos == 'Noun']
    tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
    return ' '.join(tokens)

# 4. cleaned_review 컬럼 새로 만들기 (전처리 적용)
df['cleaned_review'] = df['리뷰'].apply(preprocess_text)

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# 한글 폰트 경로 지정
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_prop = fm.FontProperties(fname=font_path).get_name()

plt.rc('font', family=font_prop)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지


# 5. 영화별, 구분별 워드클라우드 생성 함수
def generate_wordcloud(data, title):
    text = ' '.join(data.dropna())
    if not text.strip():
        print(f"{title} 리뷰 텍스트가 부족합니다.")
        return
    wc = WordCloud(
        font_path='C:/Windows/Fonts/malgun.ttf',
        width=800,
        height=600,
        background_color='white',
        max_words=100,
        stopwords=stopwords
    ).generate(text)

    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()

# 6. 영화별, 평론가/관람객 분리해서 워드클라우드 출력
movies = df['영화제목'].unique()
for movie in movies:
    for group in ['평론가', '관람객']:
        subset = df[(df['영화제목'] == movie) & (df['구분'] == group)]
        generate_wordcloud(subset['cleaned_review'], f"{movie} - {group} 워드클라우드")

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
import pandas as pd
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

