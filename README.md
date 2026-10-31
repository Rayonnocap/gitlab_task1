# Калькулятор

Простой калькулятор с веб-интерфейсом на Flask. У каждой операции свой эндпоинт.

    POST /add       {"a": 2, "b": 3}
    POST /subtract  {"a": 5, "b": 3}
    POST /multiply  {"a": 4, "b": 6}
    POST /divide    {"a": 10, "b": 4}
    GET  /version
    POST /api/resolve  {"host": "localhost"}

Плюс отдельный сервис `frontend/` — "Pro"-режим на Next.js (App Router,
порт 4000).

## Локально

    pip install -r requirements.txt
    python app.py

Открыть http://localhost:5000

## Docker

    docker compose up -d --build

Поднимет оба сервиса: калькулятор на 5000, Pro-режим на 4000. Нужен плагин
`docker compose` (v2); если на машине только `docker.io`, доставьте
`docker-compose-plugin`.

## CI/CD (GitLab)

Пайплайн описан в `.gitlab-ci.yml`, четыре стадии, идут на каждый пуш в
любую ветку:

1. **test** - pytest в чистом контейнере python
2. **build** / **build_frontend** - сборка образов `calculator:<версия>` и
   `calculator-pro:<версия>`
3. **security** - semgrep (SAST, полный аудит по всем правилам реестра,
   `--config=auto`, без своих правил), trivy (SCA по зависимостям обоих
   сервисов, проверка конфигурации Dockerfile/`docker-compose.yml`,
   сканирование собранных образов), nuclei (DAST против обоих поднятых
   контейнеров, все community-шаблоны без фильтра по severity, без своих
   файлов). Кастомные правила/политики - только у trivy (и то не
   используются, хватает дефолтных). Все джобы с `allow_failure: true`,
   отчёты смотрим в Job -> artifacts.
4. **deploy** - `deploy.sh` через `docker compose` поднимает новую версию,
   проверяет `/version`, если не поднялась - откатывается на прошлую

Версия = `MAJOR_MINOR.номер_пайплайна`, например `1.0.12`. `MAJOR_MINOR`
лежит в начале `.gitlab-ci.yml`, номер ставится сам. Версия видна в углу
калькулятора и на `/version`.

### Настройка Debian-машины

    sudo apt update
    sudo apt install -y git curl docker.io docker-compose-plugin
    sudo systemctl enable --now docker

    curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
    sudo apt install -y gitlab-runner
    sudo usermod -aG docker gitlab-runner
    sudo rm -f /home/gitlab-runner/.bash_logout   # на debian иначе джобы падают

Создать раннер: проект в GitLab -> Settings -> CI/CD -> Runners ->
New project runner, тег `debian`, скопировать токен (`glrt-...`).

    sudo gitlab-runner register --non-interactive \
      --url https://gitlab.com \
      --token glrt-XXXXXXXX \
      --executor shell
    sudo gitlab-runner verify

Если GitLab свой, в `--url` его адрес.

### Git

    git init -b main
    git add .
    git commit -m "calculator"
    git remote add origin git@gitlab.com:<user>/calculator.git
    git push -u origin main

После пуша в main пайплайн сам все прогонит и обновит контейнер на машине.
Проверить: `curl http://<ip-машины>:5000/version`

### Как обновлять

- новый метод: добавить роут в `app.py` и тест в `tests/`, запушить
- новая версия flask: поправить `requirements.txt`, запушить
- новый базовый образ: поправить `FROM` в `Dockerfile`. Кроме того, сборка идет
  с `--pull`, так что свежий образ подтягивается при каждой сборке
- чтобы обновляться без коммитов: CI/CD -> Schedules, например раз в неделю
