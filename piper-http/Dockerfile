ARG BUILD_FROM
FROM ${BUILD_FROM}

WORKDIR /usr/src
ARG BUILD_ARCH=amd64
ARG PIPER_RELEASE=v0.0.2

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
    && pip3 install --no-cache-dir -U setuptools wheel \
    && pip3 install --no-cache-dir aiohttp \
    && ARCH="${BUILD_ARCH}" \
    && if [[ "${BUILD_ARCH}" = "aarch64" ]]; then ARCH="arm64"; fi \
    && curl -L -s \
      "https://github.com/rhasspy/piper/releases/download/${PIPER_RELEASE}/piper_${ARCH}.tar.gz" \
        | tar -zxvf - -C /usr/share \
    \
    && curl -L -s \
      "https://github.com/rhasspy/piper/releases/download/${PIPER_RELEASE}/voice-en-us-ryan-medium.tar.gz" \
        | tar -zxvf - -C /usr/share/piper \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY run.* /
RUN chmod +x run.sh
CMD [ "/run.sh" ]