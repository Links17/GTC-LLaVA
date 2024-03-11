FROM dustynv/local_llm:r35.3.1
WORKDIR /opt/combo/
COPY . /opt/combo/
RUN pip3 install -i https://pypi.doubanio.com/simple paho-mqtt==1.6.1
ENV DEBIAN_FRONTEND=noninteractive
CMD python3 /opt/combo/main.py
