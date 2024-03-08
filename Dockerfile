FROM dustynv/local_llm:r35.3.1
LABEL authors="Links"
WORKDIR /opt/combo/
COPY . /opt/combo/
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y ffmpeg vim \
    && pip3 install openai-whisper \
    && python3 /opt/combo/whisper_init.py
CMD python3 /opt/combo/main.py
