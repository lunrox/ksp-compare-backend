FROM python:3.7.2-alpine3.9

WORKDIR /src
ENV FLASK_APP=chemy

COPY requirements.txt ./
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	; \
	pip install -r requirements.txt; \
	apk del .build-deps;

COPY chemy chemy/
COPY csv_to_mongo.py solubility_product.csv run.sh ./

CMD ["/src/run.sh"]
