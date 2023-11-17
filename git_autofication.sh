#!/bin/bash

# GitHub 조직 이름과 토큰
ORG_NAME="0D0S"
TOKEN="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"

# 리포지토리 이름
REPO_NAME="odos"

# 로컬에서 작업한 변경사항을 커밋
git add .
git commit -m ":memo: update `date +%F+%H:%M`"

# 조직 이름과 토큰을 사용하여 GitHub에 push
git push https://$ORG_NAME:$TOKEN@github.com/$ORG_NAME/$REPO_NAME.git main

