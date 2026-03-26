FROM python

WORKDIR /

COPY . .
RUN rm .env # you can't steal my secrets

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
