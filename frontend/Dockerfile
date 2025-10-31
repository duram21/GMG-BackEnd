# 1. Node.js 18 경량 버전을 기반으로 시작
FROM node:18-alpine

# 2. 컨테이너 내부의 작업 폴더를 /app 으로 설정
WORKDIR /app

# 3. package.json과 package-lock.json(있다면)을 먼저 복사
COPY package*.json ./

# 4. package.json 에 적힌 라이브러리 설치 (npm install)
RUN npm install

# 5. docker-compose.yml의 volumes가 나머지 src, public 폴더를
#    /app 폴더로 마운트(연결)해 줄 것입니다.
#    (배포용 Dockerfile에는 'COPY . .'가 포함됩니다)

# 6. React 개발 서버의 기본 포트 3000번을 노출
EXPOSE 3000

# 7. 컨테이너 실행 시 기본 명령어
CMD ["npm", "start"]