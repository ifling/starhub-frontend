## Windows 本机安装 Docker（WSL2 + Docker Desktop）

适用环境：Windows 10/11，PowerShell。

目标：让你在本机能运行本仓库根目录的：

```powershell
docker compose up -d --build
```

---

### 0. 必要条件（先看一眼）

- **CPU 虚拟化已开启**：任务管理器 → 性能 → CPU → “虚拟化：已启用”
- 你需要能以**管理员身份**运行 PowerShell

如果虚拟化未启用，需要进 BIOS/UEFI 开启（名称可能是 Intel VT-x / AMD SVM）。

---

### 1. 安装 WSL2（管理员 PowerShell）

1) 以管理员身份打开 PowerShell，执行：

```powershell
wsl.exe --install
```

2) 按提示 **重启电脑**。

3) 重启后（普通 PowerShell 即可）执行：

```powershell
wsl --set-default-version 2
wsl --status
```

如果你想明确安装 Ubuntu 22.04（可选）：

```powershell
wsl --install -d Ubuntu-22.04
```

---

### 2. 安装 Docker Desktop

1) 下载并安装 Docker Desktop（Windows 版）
2) 安装完成后启动 Docker Desktop，等待它初始化完成
3) 在 Docker Desktop：
   - Settings → Resources → **WSL Integration**
   - 勾选你的 WSL 发行版（例如 Ubuntu）

---

### 3. 验证 Docker 是否可用

打开一个新的 PowerShell 窗口执行：

```powershell
docker --version
docker compose version
docker run --rm hello-world
```

都成功后，Docker 就装好了。

---

### 4. 启动本仓库后端（Docker Compose）

在仓库根目录：

```powershell
cp .\.env.example .env
# 建议编辑 .env，把 POSTGRES_PASSWORD 改掉
docker compose up -d --build
```

验证：

```powershell
curl http://localhost:8000/health
```

浏览器查看接口文档：

- `http://localhost:8000/docs`

---

## 常见问题（把输出贴给我即可）

### A) `wsl` 提示需要更新 / 安装失败

把以下命令输出贴给我：

```powershell
wsl --status
wsl --version
```

### B) `docker` 命令找不到（`CommandNotFoundException`）

通常是 Docker Desktop 未安装/未启动，或需要重启终端。

把以下命令输出贴给我：

```powershell
where.exe docker
docker --version
```

### C) Docker Desktop 启动失败 / WSL2 engine 报错

把 Docker Desktop 的报错截图或错误文字贴给我，同时贴：

```powershell
wsl --status
wsl -l -v
```

### D) `docker compose up` 卡在拉镜像/网络问题

把以下输出贴给我：

```powershell
docker compose ps
docker compose logs -f api
docker compose logs -f db
```

