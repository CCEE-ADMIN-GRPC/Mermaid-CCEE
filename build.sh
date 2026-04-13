#!/usr/bin/env bash

# Sai do script se algum comando falhar
set -e

# 1. Instala os pacotes do Python
pip install -r requirements.txt

# 2. Cria uma pasta local chamada 'bin' e instala o D2 dentro dela
mkdir -p bin
curl -fsSL https://d2lang.com/install.sh | sh -s -- --dir ./bin
