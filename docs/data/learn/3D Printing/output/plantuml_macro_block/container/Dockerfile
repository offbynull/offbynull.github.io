FROM alpine:3.10

# jre-headless won't work -- it fails when running plantuml
# fontconfig/ttf-dejavu required for fonts
# graphviz required for dot graphs
RUN apk add --no-cache \
      openjdk11-jre \
      fontconfig \
      ttf-dejavu \
      graphviz \
      wget \
  && mkdir -p /opt \
  && wget -O /opt/plantuml.jar \
      https://repo1.maven.org/maven2/net/sourceforge/plantuml/plantuml/1.2019.8/plantuml-1.2019.8.jar \
  && apk del --no-cache wget

WORKDIR /_macro
COPY run.sh .