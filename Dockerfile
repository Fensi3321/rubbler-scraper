FROM python:3.9.2

WORKDIR /opt/scraper

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir Scrapy

COPY . .

WORKDIR ./scraper/

CMD ["scrapy", "crawl", "OfferScraper"]