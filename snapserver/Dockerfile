ARG BUILD_FROM
FROM $BUILD_FROM

# Add env
ENV LANG C.UTF-8

RUN apk add --no-cache librespot --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing/
RUN apk add --no-cache snapcast-server --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community/

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
