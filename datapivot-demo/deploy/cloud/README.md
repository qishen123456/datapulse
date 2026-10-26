# DataPulse 腾讯云 Docker 部署指南

适用服务器：119.29.216.36，Ubuntu 24.04，4核8G、60G盘。依据项目根目录「云服务器配置」编写，文档中的资源余量是历史记录；本次没有远程登录或实测。

本目录提供 `deploy.sh` 和独立 `compose.yml`。初次配置后运行一条启动命令即可构建和启动。默认入口 **http://119.29.216.36:8888**，避开宝塔及现有 Nginx Proxy Manager 的 80/443 端口。

架构：浏览器 → 前端 Nginx:8888 → 后端:5002 → PostgreSQL:5432。后端和数据库没有宿主机端口映射。模型服务仍调用你配置的外部 API，本机不运行大模型。4核8G适合作为小规模试用起点，实际并发容量需用真实问数压测确认。

## 1. 上传当前代码（Mac 执行）

使用当前工作目录打包，包含尚未推送 Git 的最新界面。不要上传整个项目根目录，其中有模型服务凭据、其他项目资料及开发缓存。

```bash
cd /Users/ltq/Desktop/ambitious/4.Lin_project/1.智能问数
COPYFILE_DISABLE=1 tar \
  --exclude='.env' --exclude='.env.*' \
  --exclude='node_modules' --exclude='.git' --exclude='.venv' --exclude='venv' \
  --exclude='dist' --exclude='__pycache__' --exclude='*.log' \
  --exclude='config' --exclude='logs' --exclude='chroma_db' \
  --exclude='backups' --exclude='imports' --exclude='state' \
  -czf /private/tmp/datapulse-cloud.tar.gz datapivot-demo
scp /private/tmp/datapulse-cloud.tar.gz root@119.29.216.36:/tmp/
```

配置和数据后续单独迁移。这个代码包不会自动带上本地运行数据。

## 2. 服务器检查（SSH 后执行）

```bash
ssh root@119.29.216.36
docker version
docker compose version
df -h /
free -h
ss -lntp | grep ':8888 ' || true
```

Docker 已安装时不重装。若缺少 Compose 插件，在已配置 Docker 官方 apt 源的前提下执行 `apt-get update && apt-get install -y docker-compose-plugin`；若没有相应源，按 [Docker Ubuntu 官方安装文档](https://docs.docker.com/engine/install/ubuntu/) 补齐。构建需要拉取 Node/Python/Postgres/Nginx 基础镜像，以及 npm/pip 依赖；失败时检查网络与镜像源，不反复清空数据。

若8888被占用，下一步在 `.env` 改用未占用端口，例如8890，同时修改云防火墙规则。

## 3. 初次部署

```bash
mkdir -p /www/wwwroot/datapulse
cd /www/wwwroot/datapulse
tar -xzf /tmp/datapulse-cloud.tar.gz
cd datapivot-demo/deploy/cloud
bash deploy.sh init
nano .env
```

`.env` 自动生成数据库密码、管理员密码及会话密钥。请在服务器保存管理员密码，不要把 `.env` 发到聊天或提交Git。模型参数可现在填写，也可启动后在“模型服务”配置：

```dotenv
DATAPULSE_AI_PROVIDER=custom
DATAPULSE_AI_LABEL=硅基流动
DATAPULSE_AI_BASE_URL=https://api.siliconflow.cn/v1
DATAPULSE_AI_MODEL=填写账号实际可用的模型ID
DATAPULSE_AI_API_KEY=填写你自己的密钥
WEB_PORT=8888
```

`init` 不会覆盖已有 `.env`。首次部署应保留自动生成的 `DB_PASSWORD`；已有PG卷建立后，修改这个变量不会自动修改数据库内密码。

**一键启动：**

```bash
bash deploy.sh start
```

脚本按顺序构建以降低内存峰值，先检查数据库，再运行迁移，最后等待后端和前端启动。健康依赖方式参照 [Compose 官方启动顺序说明](https://docs.docker.com/compose/how-tos/startup-order/)。首次构建时间取决于服务器下载速度，不承诺两分钟完成。

腾讯云轻量服务器控制台 → 防火墙 → 添加 **TCP 8888**；初次试用可限制来源为你的公网IP。不要开放5432或5002。Docker发布的端口与UFW规则存在特殊交互，边界以云防火墙配置为准。

访问 **http://119.29.216.36:8888**，登录名 `admin`，密码见服务器 `.env` 中 `DATAPULSE_ADMIN_PASSWORD`。

## 4. 带上当前三个燃气数据集（首次迁移）

**程序启动成功不等于数据已迁移。** 当前燃气数据在本机 PostgreSQL 的 `raw_gas`，数据集元数据、组织树和授权在业务库中；CSV本身不含完整问数配置。建议首次用完整业务库备份迁移，并单独复制JSON配置。

本节只用于全新云端实例；已有云端业务数据时应先做备份和迁移评估，不能直接覆盖。

在Mac执行，备份当前业务库：

```bash
mkdir -p /private/tmp/datapulse-transfer
chmod 700 /private/tmp/datapulse-transfer
docker exec askdesk-postgres pg_dump -U postgres -d postgres -Fc \
  > /private/tmp/datapulse-transfer/runtime.dump
chmod 600 /private/tmp/datapulse-transfer/runtime.dump
scp /private/tmp/datapulse-transfer/runtime.dump root@119.29.216.36:/tmp/datapulse-runtime.dump
```

云端执行（当前目录是 `datapivot-demo/deploy/cloud`）：

```bash
bash deploy.sh backup
docker compose stop backend frontend
docker compose exec -T postgres pg_restore -U postgres -d postgres \
  --clean --if-exists --no-owner --no-privileges --exit-on-error < /tmp/datapulse-runtime.dump
docker compose run --rm migrate
docker compose up -d --wait --wait-timeout 360 backend frontend
```

数据库迁移会带上账号、组织和三个燃气数据集，也可能带上本地模型服务配置。数据库内数据源应检查为 `postgres:5432`、库 `postgres`、用户 `postgres`，并在“数据源管理”重新填写云端 `DB_PASSWORD` 后测试，不能沿用本地数据库密码。

JSON配置需要保持本地专家指令、技能、控制台设置时，在Mac额外执行：

```bash
docker cp askdesk-backend:/app/config /private/tmp/datapulse-transfer/config
scp -r /private/tmp/datapulse-transfer/config root@119.29.216.36:/tmp/datapulse-config
```

云端备份后，将 `/tmp/datapulse-config/` 内文件复制到 `state/config/`，再运行 `bash deploy.sh restart`。若其中存在 `enc:v1` 加密值，需要同时按原系统方式提供对应的主密钥（`ASKDESK_SECRET_MASTER_KEY` / 密钥文件）；没有密钥时，在管理页面重新填写连接凭据。不要新生成密钥冒充旧密钥，不要把本地 `.env` 整份覆盖云端 `.env`。

核对三个数据集：经营与供销差、应收回款与稽核、安全与管网治理；确认数据源、组织范围、模型连通后再问：“2026年9月各分公司销气量环比8月变化多少”。

验收后清理服务器 `/tmp/datapulse-runtime.dump`、`/tmp/datapulse-config` 及Mac临时传输目录中的敏感备份；正式备份留在受控目录保存。

## 5. 域名和 HTTPS（正式使用）

已有 Nginx Proxy Manager，可新增 Proxy Host：

- 域名A记录指向119.29.216.36。
- 上游填写宿主机在 Docker 中可达的地址及8888端口；**不要填写NPM容器自己的127.0.0.1**。
- 申请证书，启用HTTPS；为问数流保持 `proxy_buffering off; proxy_cache off; proxy_read_timeout 300s;`。
- 浏览器验证完整流式问数后，关闭8888公网入口，仅保留80/443。保留NPM访问宿主机上游所需的内网连通。

首次试用可用IP+端口，正式使用建议完成HTTPS再开放给用户。

## 6. 运维、更新与回退

均在 `/www/wwwroot/datapulse/datapivot-demo/deploy/cloud` 执行：

```bash
bash deploy.sh status
bash deploy.sh logs
bash deploy.sh backup
bash deploy.sh restart
bash deploy.sh stop
```

备份目录为 `state/backups/`，包含数据库和JSON配置及 `.env`，需要保密并定期复制到服务器外。Chroma数据在独立卷中；上述备份不包含向量索引，恢复后需要按应用能力重建或另做卷备份。

更新前备份并保留上一版代码包，再上传新代码包解压覆盖源代码，运行 `bash deploy.sh update`。代码包不包含 `.env`、state和卷，正常更新不覆盖运行数据。若版本迁移改变库结构，不能只回退镜像；应结合发布前库备份和对应配置恢复。

禁止使用 `docker compose down -v` 清理本项目，它会删除数据库/向量卷。也不要运行全局 `docker system prune --volumes`，这台机器还承载其他应用。

排障：

```bash
docker compose logs --tail=100 migrate backend frontend
curl -f http://127.0.0.1:8888/api/health
docker compose exec -T postgres psql -U postgres -d postgres -c 'SELECT 1'
```

迁移容器正常为退出码0；后端和前端应持续运行。网页打不开先查云防火墙/端口；502先查后端健康；问数报错先查模型连通性与数据源，不把“页面打开了”视为完整验收。

本次已验证脚本语法与Compose配置；没有连接云服务器、启动云端容器或执行数据迁移。
