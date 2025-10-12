# 1. 베이스 이미지 선택 (파이썬 3.10 버전 사용)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정 (컨테이너 내부에 /app 폴더를 만들고 거기로 이동)
WORKDIR /app

# 3. 필요한 라이브러리 설치
#    --no-cache-dir 옵션은 불필요한 캐시를 남기지 않아 이미지 용량을 줄여줍니다.
RUN pip install --no-cache-dir osmnx matplotlib scikit-learn


# 4. 로컬의 파이썬 코드를 컨테이너의 /app 폴더로 복사
#    map_drawer.py 라는 이름으로 코드를 작성할 예정입니다.
COPY map_drawer.py .

# 5. 컨테이너가 실행될 때 자동으로 실행할 명령어 설정
CMD [ "python", "./map_drawer.py" ]