# poetry 設定
poetry config virtualenvs.in-project true

# pyenv 任意のpythonのバージョンをインストールするために必要なモジュールをインストール
apt-get update
apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# CycleGAN-VC2の設定
cd ./flask/models/converters/CycleGAN_VC2
pyenv install 3z.7.14
poetry install 
