# 1. 베이스 이미지 선택 (파이썬 3.10 버전 사용)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# (선택) 시스템 라이브러리 설치 - gpkg 저장을 위해 필요
RUN apt-get update && apt-get install -y --no-install-recommends libgdal-dev

# 3. requirements.txt 파일만 먼저 복사
COPY requirements.txt ./

# 4. 복사된 파일로 라이브러리 설치 (이 단계가 캐시됩니다!)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 모든 소스 코드(.py)를 마지막에 복사
COPY *.py ./

# 6. 컨테이너가 실행될 때 자동으로 실행할 명령어 설정
CMD [ "python", "./map_drawer.py" ]