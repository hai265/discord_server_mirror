FROM python:3.9-slim-bullseye
RUN apk add git
RUN apk add --update py-pip
RUN pip install --user --upgrade git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY . .
CMD ["python3","src/main.py"]
