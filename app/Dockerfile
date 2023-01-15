FROM python:alpine
WORKDIR /usr/src/app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]