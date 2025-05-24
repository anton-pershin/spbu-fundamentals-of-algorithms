#!/bin/bash

# Скрипт для обновления форка
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
