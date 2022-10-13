FROM python:3.7.14-alpine3.16

WORKDIR /app

RUN pip3 install flask flask-cors

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]