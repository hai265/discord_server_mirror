FROM python:3.10-slim-buster 
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip install --user --upgrade git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3","src/main.py"]
