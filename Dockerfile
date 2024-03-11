FROM dustynv/local_llm:r35.3.1

WORKDIR /opt/combo/
COPY . /opt/combo/

ENV DEBIAN_FRONTEND=noninteractive

RUN pip3 install --no-cache-dir --verbose paho-mqtt==1.6.1
RUN pip3 list

CMD python3 /opt/combo/main.py
