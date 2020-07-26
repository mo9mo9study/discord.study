FROM python:3.8.5-slim-buster
# FROM alpine:edge

# Add project source
WORKDIR /usr/src/discord.study
COPY . ./

# Install dependencies
RUN apt update \
  && apt-get -y install procps \
  && apt-get -y clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install -U "discord.py[voice]"

ENTRYPOINT ["/bin/bash"]
CMD ["/usr/src/discord.study/entry_exit/observer.sh"]