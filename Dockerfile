FROM python:3.8.5-slim-buster

# Add project source
WORKDIR /usr/src/discord.study

# Install dependencies
RUN apt update \
  && apt-get -y install procps python3-magic \
  && apt-get -y install vim \
  && apt-get -y clean \
  && rm -rf /var/lib/apt/lists/* 

# Add project source
COPY . ./

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install -U "discord.py[voice]"

ENTRYPOINT ["/bin/bash"]
CMD ["/usr/src/discord.study/entry_exit/observer.sh"]