FROM alpine:edge

# Add project source
WORKDIR /usr/src/discord.study
COPY . ./

# Install dependencies
RUN apk update \
&& apk add --no-cache \
  ca-certificates \
  python3 \
  py-pip \
  python3-dev \
  bash \
\
# Install build dependencies
&& apk add --no-cache --virtual .build-deps \
  gcc \
  git \
  libffi-dev \
  make \
  musl-dev \
\
# Install pip dependencies
&& pip install --no-cache-dir -r requirements.txt \
\
# Clean up build dependencies
&& apk del .build-deps

ENTRYPOINT ["/bin/bash"]
CMD ["/usr/src/discord.study/entry_exit/observer.sh"]