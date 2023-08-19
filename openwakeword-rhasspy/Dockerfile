ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV PIP_BREAK_SYSTEM_PACKAGES 1

RUN ARCH=`uname -m` && \
    apt-get update \
    && apt-get install -y --no-install-recommends \
      python3-dev \
      python3-pip \
      gcc \
      portaudio19-dev \
      libasound2-plugins \
      libspeexdsp-dev \
    && pip3 install --no-cache-dir -U setuptools wheel \
    && pip3 install --no-cache-dir pyaudio requests openwakeword==0.5.0 \
    && pip3 install --no-cache-dir https://github.com/dscripka/openWakeWord/releases/download/v0.1.1/speexdsp_ns-0.1.2-cp39-cp39-linux_${ARCH}.whl

WORKDIR /
COPY run.sh wakeword.py /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]