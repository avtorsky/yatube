#!/bin/bash

set -e
set -o pipefail

echo '-------------------------------// isort: mission accepted'
isort --profile black yatube
echo '-------------------------------// isort: mission accomplished ヽ(⚬_⚬)ノ'

echo '-------------------------------// black: mission accepted'
black --line-length 79 --skip-string-normalization yatube
echo '-------------------------------// black: mission accomplished ヽ(⚬_⚬)ノ'

echo '-------------------------------// unit tests: mission accepted'
source venv/bin/activate && cd ./yatube
coverage run --source='about,core,posts,users' manage.py test -v 1
coverage report
echo '-------------------------------// unit tests: mission accomplished ヽ(⚬_⚬)ノ'

echo '-------------------------------// pytest: mission accepted'
pytest
echo '-------------------------------// pytest: mission accomplished ヽ(⚬_⚬)ノ'