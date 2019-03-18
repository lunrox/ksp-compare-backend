FROM python:3.7.2-alpine3.9

ENV FLASK_APP=chemy

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY chemy chemy/
COPY csv_to_mongo.py solubility_product.csv ./

CMD ["flask", "run", "--host=0.0.0.0"]
