#!/bin/sh
# использование: sh deploy.sh <версия>
set -e

VERSION=$1
OLD=$(docker inspect -f '{{.Config.Image}}' calculator 2>/dev/null || true)

docker rm -f calculator 2>/dev/null || true
docker run -d --name calculator --restart unless-stopped -p 5000:5000 calculator:$VERSION

# ждем пока поднимется
for i in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fs http://localhost:5000/version | grep -qF "\"$VERSION\""; then
    echo "версия $VERSION работает"
    exit 0
  fi
  sleep 1
done

echo "версия $VERSION не поднялась"
docker logs calculator || true
docker rm -f calculator

if [ -n "$OLD" ]; then
  echo "откатываюсь на $OLD"
  docker run -d --name calculator --restart unless-stopped -p 5000:5000 $OLD
fi
exit 1
