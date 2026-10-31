FROM node:20-slim AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-slim

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY next.config.js ./
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public

ENV NEXT_TELEMETRY_DISABLED=1
EXPOSE 4000

RUN useradd -m appuser
USER appuser

CMD ["npm", "run", "start"]
