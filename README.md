# MG-FleaMarket

**MG-Mod 实时跳蚤市场同步工具** — 基于 Python 的自动价格数据同步服务

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://python.org)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey)](LICENSE)

---

## 📖 简介

**MG-FleaMarket** 是 MG-Mod **实时跳蚤市场**功能的后端数据同步工具。它自动从 **tarkov.dev GraphQL API** 获取 Tarkov 社区物品价格数据，经过加权算法处理后，生成最优价格 JSON 文件，并通过 Git 推送到云端。

MG-Mod 的实时跳蚤功能在游戏启动时自动从本仓库下载最新的 `price.json`，实现游戏内跳蚤市场价格的实时同步。

---

## 🔄 数据流

```
tarkov.dev GraphQL API
         │
         ▼  HTTP GET (items: id, name, basePrice, avg24hPrice, low24hPrice, high24hPrice)
         │
  ┌──────────────┐
  │ main.py      │ ← 读取本地 items.json（物品白名单）
  │              │ ← 加权价格算法计算
  │              │ → 输出 price.json
  └──────┬───────┘
         │
         ▼  Git commit + push
         │
  ┌──────────────┐
  │ price.json   │ ← 云端同步（本仓库）
  └──────┬───────┘
         │
         ▼  MG-Mod 启动时自动拉取
         │
  ┌──────────────┐
  │ 游戏内跳蚤市场│ ← 价格同步完成
  └──────────────┘
```

---

## 🏗️ 项目结构

```
MG-FleaMarket/
├── src/
│   ├── main.py           ← 主入口（API 请求 → 加权计算 → Git 推送）
│   ├── method.py         ← 工具类（日期/文件/HTTP/Git 操作）
│   └── static_value.py   ← 路径常量配置
├── res/
│   ├── base/
│   │   ├── items.json          ← 物品白名单（本地维护）
│   │   └── itemsBaseInfo.json  ← API 全量物品信息缓存
│   └── price.json              ← 输出：最终价格数据
├── Build/                ← PyInstaller 构建输出
├── main.exe              ← 编译后的可执行文件
└── main.spec             ← PyInstaller 打包配置
```

### 核心算法

`main.py` 中的价格计算采用三阶段加权算法：

| 情况 | 条件 | 算法 |
|------|------|------|
| ① 仅有 basePrice | `avg24hPrice` 为空 | 直接返回 basePrice |
| ② 缺少 low/high | 有 base + avg，缺 low/high | `0.15 × base + 0.85 × avg` |
| ③ 四项齐全 | base + avg + low + high 均有 | 复杂加权模型（含基准权重 + 平均价格 + 价格区间） |

### 工具类（`method.py`）

| 类 | 职能 |
|------|------|
| `MGDate` | 日期获取与格式化 |
| `FileControl` | JSON 文件的读写操作 |
| `HttpControl` | HTTP POST 请求封装（调用 GraphQL API） |
| `PathControl` | 路径拼接与文件定位 |
| `GitControl` | Git 自动 pull/add/commit/push 封装 |

---

## 🚀 使用方式

### 手动运行
```bash
python src/main.py
```

### 自动运行（编译版本）
```bash
main.exe
```

### 运行流程
1. `git pull` 同步本地仓库
2. 调用 tarkov.dev GraphQL API 获取最新价格
3. 保存 `itemsBaseInfo.json`（API 数据缓存）
4. 读取 `items.json`（物品白名单过滤）
5. 加权计算每个物品价格
6. 输出 `price.json`
7. `git add/commit/push` 推送至云端

---

## 🛠️ 技术细节

- **API**: [tarkov.dev](https://tarkov.dev/) GraphQL
- **查询参数**: `items(lang:zh)` — 物品 ID、名称、简称、基础价格、24h 均价/最低/最高
- **打包工具**: PyInstaller（单文件无控制台模式）
- **依赖**: 仅 Python 标准库 + PyInstaller（构建用）

---

## 📄 许可证

本项目采用 **CC BY-NC-ND 4.0** 协议。

- ✅ 允许免费使用和分享（需署名）
- ❌ **禁止商业用途**
- ❌ **禁止修改后重新发布**

保留所有版权。详见 [LICENSE](LICENSE) 文件。

---

## 🔗 相关链接

- [MG-Mod（主仓库）](https://github.com/MarecGents/MG-Mod)
- [MG-Mod-CSharp（核心逻辑库）](https://github.com/MarecGents/MG-Mod-CSharp)
- 作者：[MarecGents](https://sns.oddba.cn/author/92586) | [爱发电](https://ifdian.net/a/MarecGents)
