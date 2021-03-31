FROM python:3.7
WORKDIR /rockx-market
COPY .  /rockx-market
RUN pip install -r requirements.txt
EXPOSE  5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.wsgi:app"]
