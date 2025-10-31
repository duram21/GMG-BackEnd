# 1. 파이썬 3.11 경량 버전을 기반으로 시작
FROM python:3.11-slim

# 2. 컨테이너 내부의 작업 폴더를 /app 으로 설정
WORKDIR /app

# 3. requirements.txt 파일을 먼저 복사
COPY ./requirements.txt .

# 4. requirements.txt 에 적힌 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 코드를 /app 폴더로 복사
#    (docker-compose에서 volumes를 사용하므로 이 줄은 생략 가능하나,
#     배포용 Dockerfile에는 이 줄이 포함되는 것이 좋습니다.)
COPY . .