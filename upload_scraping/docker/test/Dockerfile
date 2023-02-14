FROM ubuntu:latest
RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        # debug utility
        vim \
        less \
        curl \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir scraping
COPY /upload_scraping/docker/run.sh .
RUN sed -i 's/\r//' run.sh
COPY /upload_scraping/docker/test/run_unittest.sh /scraping/upload_scraping/test/
RUN sed -i 's/\r//' /scraping/upload_scraping/test/run_unittest.sh
COPY /requirements.txt /scraping/
COPY /setup.py /scraping/
COPY /upload_video_downloader.py /scraping/
COPY /LICENSE /scraping/
COPY /README.md /scraping/
COPY /upload_scraping/src /scraping/upload_scraping/src
COPY /upload_scraping/test /scraping/test
COPY /upload_scraping/test/link.txt /scraping/test/
RUN echo '#!/bin/bash\n/run.sh' > /usr/bin/run_app && chmod +x /usr/bin/run_app
RUN echo '#!/bin/bash\n/scraping/run_unittest.sh' > /usr/bin/run_test && chmod +x /usr/bin/run_test
WORKDIR /scraping
RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR /