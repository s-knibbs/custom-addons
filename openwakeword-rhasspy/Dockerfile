ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      python3-dev \
      python3-pip \
      gcc \
      portaudio19-dev \
      libasound2-plugins \
    && pip3 install --no-cache-dir -U setuptools wheel \
    && pip3 install --no-cache-dir pyaudio requests openwakeword

WORKDIR /
COPY run.sh wakeword.py /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]