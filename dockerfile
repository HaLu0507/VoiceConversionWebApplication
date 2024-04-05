FROM  nvidia/cuda:12.3.1-devel-ubuntu22.04

RUN apt update \
    && apt install -y \
    git\
    python3.10\
    python3-pip \
    curl

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get autoremove -y && apt-get clean && \
    rm -rf /usr/local/src/*

RUN apt-get update && apt-get -y install sudo

# 音声の処理に関するライブラリ
RUN apt-get install -y libsndfile1

# pyenv の導入
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# pyenv ~/.bashrc の設定
RUN echo '# pyenv settings' >> ~/.bashrc
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# pyenv ~/.profile の設定
RUN echo '# pyenv settings' >> ~/.profile
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
RUN echo 'eval "$(pyenv init -)"' >> ~/.profile

# poetry の導入
RUN curl -sSL https://install.python-poetry.org | python3 -
# poetry ~/.bashrcの設定
RUN echo '# poetry settings' >> ~/.bashrc
RUN echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc

# # ROOTにパスワードをセット
# # 「su - root」 でrootユーザにログイン
# RUN echo 'root:user01' |chpasswd

# # ユーザーの設定
# ENV UNAME=user01
# ENV GID=1000
# ENV UID=1000
# RUN groupadd -g $GID -o $UNAME
# RUN useradd -m -u $UID -g $GID -G sudo -o -s /bin/bash $UNAME
# RUN echo "$UNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# USER user01