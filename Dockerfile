FROM python:3.10

WORKDIR /tmp

COPY ./requirements.txt ./tmp/requirements.txt
COPY ./src ./tmp/src

RUN pip install --upgrade pip \
	pip install --upgrade 'build>=0.7' 'setuptools>=61.0,<64.0' 'wheel>=0.37' \
	pip install -r requirements.txt \
	pre-commit install

CMD ["python", "src/coinpan_crawler.py"]
