FROM python:3.10-bookworm
LABEL description="Deploy Mage on ECS"
ARG FEATURE_BRANCH
USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

## System Packages
COPY sources.list /etc/apt/sources.list
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update
## System Packages
RUN \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
  NODE_MAJOR=20 && \
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update -y

RUN  \
  apt-get install -y --no-install-recommends \
  nodejs \
  nfs-common \
  graphviz
RUN  apt-get clean &&  rm -rf /var/lib/apt/lists/*

# 设置 pip 使用阿里云的 HTTPS PyPI 镜像源
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

## Python Packages
RUN \
  pip3 install --no-cache-dir sparkmagic && \
  mkdir /root/.sparkmagic

COPY example_config.json /root/.sparkmagic/config.json
RUN \
  sed -i 's/localhost:8998/host.docker.internal:9999/g' /root/.sparkmagic/config.json && \
  jupyter-kernelspec install --user "$(pip3 show sparkmagic | grep Location | cut -d' ' -f2)/sparkmagic/kernels/pysparkkernel"

RUN \
  pip3 install --no-cache-dir "git+https://github.com/wbond/oscrypto.git@d5f3437ed24257895ae1edd9e503cfb352e635a8" && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/singer-python.git#egg=singer-python" && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/dbt-mysql.git#egg=dbt-mysql" && \
  pip3 install --no-cache-dir "git+https://github.com/mage-ai/sqlglot#egg=sqlglot" && \
  pip3 install --no-cache-dir faster-fifo


# Mage
COPY ./mage_ai/server/constants.py /tmp/constants.py
RUN  pip3 install --no-cache-dir "git+https://github.com/13129/mage-ai_xjc.git#egg=mage-integrations&subdirectory=mage_integrations";
RUN  pip3 install --no-cache-dir "git+https://github.com/13129/mage_ai_xjc.git#egg=mage-ai[all]";
# COPY . /tmp/mage_ai_xjc


# RUN \
#   pip3 install --no-cache-dir  /tmp/mage_ai_xjc/mage_integrations && \
  # pip3 install --no-cache-dir  /tmp/mage_ai_xjc[all] && \
  # rm -rf /tmp/mage_ai_xjc



## Startup Script
COPY --chmod=0755 ./scripts/install_other_dependencies.py ./scripts/run_app.sh /app/

ENV MAGE_DATA_DIR="/home/src/mage_data"
ENV PYTHONPATH=".:/home/src"
WORKDIR /home/src
EXPOSE 6789
EXPOSE 7789

CMD ["/bin/sh", "-c", "/app/run_app.sh"]
