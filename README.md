# 14-taximeter（打车计价）

Taximeter — 起步价 + 里程价 + 低速时长费（夜间加价系数）

## 启动

```bash
docker compose up --build
```

| 入口 | 地址 |
| --- | --- |
| 前端 | http://localhost:4300 |
| API | http://localhost:9300 |

## 主链

录行程里程与低速时长 → 拆解车费 → 行程单

## 计价脉冲

规则页（`GET/POST /api/pulse`，落库于 `pulse_rules`，部分唯一索引保证同时仅一条启用）。启用后超出含公里按每 0.5 公里一跳、低速按每整分钟一跳计价，不足一跳的尾数不计；回包给出 `mileage_hops`、`slow_hops`、`per_mileage_hop`、`per_slow_hop`、`start`、`total`。夜间系数乘在跳后金额上，起步只收一次；停用回到连续计价且跳数为 0。负数输入拒绝且不写记录，`persist=false` 只读试算。

## 技术栈

Python 3.12 + FastAPI + SQLite；Vue 3 + Vite + Nginx。
