FROM dustynv/local_llm:r35.3.1
WORKDIR /opt/combo/
COPY . /opt/combo/
ENV DEBIAN_FRONTEND=noninteractive
CMD python3 /opt/combo/main.py
