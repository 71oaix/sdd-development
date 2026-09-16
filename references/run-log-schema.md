---
title: SDD 运行记录与机制复盘协议
source: sdd-development
type: reference
status: active
created: 2026-09-16
updated: 2026-09-16
---

# SDD 运行记录与机制复盘协议

## 读取时机

任务完成后追加 `.run-log.jsonl`，或累计约 5–10 次可比运行、需要判断某个 SDD 机制是否值得保留时读取。本文件不要求在普通实现开始时加载。

## 目标与边界

运行日志记录的是可复盘的证据，不是完整对话转储。它回答四个问题：用了哪些机制、为什么使用或跳过、发生了什么结果、下一次应该保留还是调整什么。

不要记录用户秘密、完整 prompt、完整测试输出或没有复盘价值的过程噪声；使用 issue、plan、Graph、test、commit、review 的路径或 ID 作为 `evidence_refs`。

## 兼容策略

历史记录使用无版本的轻量格式：`ts`、`task`、`success`、`findings`。它们保持原样，不回写、不迁移。新记录使用 `schema_version: "sdd-run/0.2"`；validator 同时接受 legacy 和 v0.2，避免升级日志系统时损失历史。

## v0.2 最小结构

每次任务追加一行 JSON，至少包含；模板为了可读性使用多行 JSON，实际写入 `.run-log.jsonl` 前需要压缩为单行。

```json
{
  "schema_version": "sdd-run/0.2",
  "run_id": "SDD-YYYYMMDD-XXX",
  "ts_start": "...",
  "ts_end": "...",
  "task": {
    "shape": "simple | complex | wide-refactor | skill-maintenance",
    "acceptance_count": 0,
    "user_visible_scope": "..."
  },
  "path": {
    "mode": "light | task-graph | parallel-trial | skill-maintenance",
    "why": "..."
  },
  "mechanisms": {},
  "execution": {},
  "verification": {},
  "retrospective": {}
}
```

### mechanisms

每个实际评估的机制记录：

- `used`：是否使用；
- `effect`：`helped`、`neutral`、`hurt`、`unknown`、`not-needed` 或 `not-used`；
- `reason`：为什么使用、跳过或得出这个判断；
- `evidence_refs`：支持判断的 issue、plan、test、commit 或 review 引用。

建议只记录本次真正相关的机制，例如 `vertical_slice`、`traceability`、`task_graph`、`tdd_loop`、`fixed_point_review`、`parallel`，不要为了填表把所有机制都列一遍。

### execution 与 verification

`execution` 记录少量可比较的计数，例如 planned / verified ticket、初始和最终 blocker 数、修正过的 edge、rework、Specification Change Request；`verification` 记录 targeted tests、typecheck、full / impacted tests、Spec Compliance findings、Engineering Standards findings、post-merge defects 和证据引用。

### retrospective

单次任务的判断是临时信号，不是永久规则。至少记录：

- `overall`：`positive`、`mixed`、`negative` 或 `unknown`；
- `keep`：已有证据值得继续使用的机制；
- `trial_next_time`：证据不足但值得继续观察的机制；
- `simplify`：方向有价值但成本过高、需要减轻的机制；
- `remove`：没有收益或不适用于本项目的机制；
- `confidence`：`low`、`medium` 或 `high`；
- `reason`：一句话说明证据和成本。

## 周期性复盘

累计约 5–10 次同类或相近规模的运行后，使用 [templates/retrospective.md](../templates/retrospective.md) 汇总：

1. 机制实际使用次数；
2. 明确帮助、无影响或造成成本的次数；
3. 返工、阻塞、漏测、review findings 和合并冲突的变化；
4. 机制维护成本；
5. 下一周期的 adopt / trial / simplify / remove 决定。

不要只根据一次成功或失败修改 `SKILL.md`；只有重复、可解释且有证据的信号，才进入 gotchas 或稳定规则。
