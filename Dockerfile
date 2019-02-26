FROM python:3.7.2-alpine3.9

ENV FLASK_APP=chemy

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY chemy chemy/

CMD ["flask", "run", "--host=0.0.0.0"]
