FROM python:3.13.3

ENV TZ=Asia/Tehran

RUN apt-get -y update && apt-get -y upgrade && apt-get install vim -y

WORKDIR /code
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . .

RUN chmod +x entrypoint.sh
CMD ["sh", "entrypoint.sh"]
