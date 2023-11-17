#!/bin/bash

# GitHub 조직 이름과 토큰
ORG_NAME="0D0S"
TOKEN=$env_github_token

# 리포지토리 이름
REPO_NAME="odos"

# 로컬에서 작업한 변경사항을 커밋
git pull
git add .
git commit -m ":memo: update `date +%F+%H:%M`"

# 조직 이름과 토큰을 사용하여 GitHub에 push
git push https://$ORG_NAME:$TOKEN@github.com/$ORG_NAME/$REPO_NAME.git main
