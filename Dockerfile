FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY . .

RUN apt-get update && apt-get install -y lame
ENTRYPOINT ["sh", "entrypoint.sh"]

CMD flask run -h 0.0.0.0 -p 8086