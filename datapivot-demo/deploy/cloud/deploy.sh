#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
umask 077
command -v docker >/dev/null || { echo '请先安装 Docker Engine'; exit 1; }
docker compose version >/dev/null
command -v openssl >/dev/null || { echo '请安装 openssl'; exit 1; }
compose() { docker compose --env-file .env -f compose.yml "$@"; }
case "${1:-start}" in
  init)
    if [[ -e .env ]]; then echo '.env 已存在，未覆盖'; exit 0; fi
    mkdir -p state/{config,backups,imports,logs,backend-logs}
    cat > .env <<ENV
DB_PASSWORD=$(openssl rand -hex 24)
DATAPULSE_ADMIN_USERNAME=admin
DATAPULSE_ADMIN_PASSWORD=$(openssl rand -hex 16)
DATAPULSE_ADMIN_DISPLAY_NAME=超级管理员
DATAPULSE_SECRET_KEY=$(openssl rand -hex 32)
WEB_PORT=8888
BIND_IP=0.0.0.0
DATAPULSE_AI_PROVIDER=custom
DATAPULSE_AI_LABEL=云端模型
DATAPULSE_AI_BASE_URL=
DATAPULSE_AI_MODEL=
DATAPULSE_AI_API_KEY=
ENV
    chmod 600 .env
    echo '已生成独立 .env。请在服务器 nano .env 查看管理员密码、填写模型配置。'
    ;;
  start|update)
    [[ -f .env ]] || { echo '先执行 bash deploy.sh init'; exit 1; }
    compose config --quiet
    # 依次构建降低 4核8G 主机的构建峰值；不修改现有宝塔/NPM。
    compose build migrate
    compose build backend
    compose build frontend
    compose up -d postgres
    compose run --rm migrate
    compose up -d --wait --wait-timeout 360 backend frontend
    compose ps
    echo '启动完成，请按 .env 的 WEB_PORT 访问。空库还需导入业务数据。'
    ;;
  status) compose ps ;;
  logs) compose logs --tail=150 -f ;;
  stop) compose stop ;;
  restart) compose restart backend frontend ;;
  backup)
    mkdir -p state/backups
    stamp=$(date +%Y%m%d_%H%M%S)
    compose exec -T postgres pg_dump -U postgres -d postgres -Fc > "state/backups/db_${stamp}.dump"
    tar -czf "state/backups/config_${stamp}.tgz" .env state/config
    echo "备份已写入 state/backups（包含敏感配置，请保密）"
    ;;
  *) echo '用法: bash deploy.sh {init|start|update|status|logs|stop|restart|backup}'; exit 2 ;;
esac
