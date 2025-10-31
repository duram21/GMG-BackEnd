import pandas as pd

# 1. CSV 파일 읽기
# 한글 파일은 인코딩 문제가 있을 수 있어, utf-8로 먼저 시도하고 안되면 cp949로 읽습니다.
try:
    df = pd.read_csv('bus_station.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('bus_station.csv', encoding='cp949')

# 2. (정리 1) 컬럼명 맨 앞의 불필요한 문자 제거하기
# 가끔 파일 맨 앞에 눈에 보이지 않는 특수 문자(BOM)가 숨어있는 경우가 있습니다.
df.columns = df.columns.str.replace('^\ufeff', '', regex=True)

print("--- 원본 데이터 정보 ---")
print(f"전체 정류장 개수: {len(df)}")
print("원본 컬럼명:", df.columns.tolist())


# 3. (정리 2) 서울 지역 데이터만 필터링하기
region_col = '정류장지역유형(0:서울/1:경기/2:인천)'
seoul_df = df[df[region_col] == 0].copy()

print("\n--- 서울시 데이터 필터링 후 ---")
print(f"서울시 정류장 개수: {len(seoul_df)}")


# 4. (정리 3) 그래프 생성에 필요한 핵심 컬럼만 선택하기
essential_cols = {
    '정류장ID': 'stop_id',
    '정류장명': 'stop_name',
    '좌표X': 'lon',  # 경도
    '좌표Y': 'lat'   # 위도
}
cleaned_df = seoul_df[essential_cols.keys()].copy()


# 5. (정리 4) 다루기 쉽게 컬럼명을 간단한 영어로 바꾸기
cleaned_df.rename(columns=essential_cols, inplace=True)


# 6. 최종 결과 확인: 정리된 데이터의 첫 5줄 출력
print("\n--- 최종 정리된 데이터 (그래프 재료) ---")
print(cleaned_df.head())

# (선택) 정리된 결과를 별도의 파일로 저장하고 싶을 때
# cleaned_df.to_csv('seoul_stops_cleaned.csv', index=False)
# print("\n'seoul_stops_cleaned.csv' 파일로 저장 완료!")