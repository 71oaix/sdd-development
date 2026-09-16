---
title: 开发循环九步详解
source: sdd-development
type: reference
---

# 开发循环

## Handoff Preflight

如果任务来自 three-space-development，先完成 handoff preflight：

1. 检查 handoff version 和 status；
2. 检查范围、输入、输出、失败行为和验收标准；
3. 检查 Solution Architecture 的决策和限制；
4. 发现规格缺口时返回 Specification Change Request；
5. 只有 preflight 通过后，才进入 issue。

## 九步循环

① 提出/确认 issue（必要时建立 Task Graph）→ ② 编写 plan → ③ plan 独立 review → ④ 人确认 plan
→ ⑤ 按 ticket 实现并逐步验证 → ⑥ fixed-point clean-context 实现 review → ⑦ 测试与 Gate 3 验证 → ⑧ 人确认合并 → ⑨ 归档

## 各步骤要点

| 步骤 | 做什么 | 产物/要求 |
|------|------|----------|
| ① issue | 要做什么：背景、目标、范围、验收标准；复杂任务另有 ticket graph | docs/issues/open/YYYY-MM-DD-简述.md |
| ② plan | 怎么做：任务解释、关键决策、实现步骤、测试方案和文档更新 | docs/plans/open/YYYY-MM-DD-简述.md |
| ③ plan review | 独立检查遗漏、矛盾和不可验证点 | review 意见合入 plan |
| ④ 人确认 | 用户批准方法、取舍和待确认决策 | 未批准不得实现 |
| ⑤ 实现 | 按 ready ticket 做 vertical slice；默认单 Agent 顺序，稳定 frontier 才可进入并行 trial | 每个 ticket 独立可验证并可追踪 |
| ⑥ 实现 review | 以 fixed point 为基准，在 clean context 中分开检查 Spec Compliance 与 Engineering Standards | invalid ref / 空 diff 先 fail fast；发现按轴保留 |
| ⑦ 测试 | ticket 级 red→green 反馈、相关测试、最终全量或受影响范围测试 | Verification Evidence，满足 Gate 3 |
| ⑧ 人确认合并 | 展示关键改动和验证证据 | 用户批准后合并 |
| ⑨ 归档 | issue 和 plan 移入 close/ | 同步 INDEX.md |

## 默认路径与升级条件

### 默认：单 ticket、单 Agent

一个边界清楚、能够由一个上下文完成的能力，保留现有一个 issue + 一个 plan。实现时按一个 seam、一个失败测试、一个最小实现的反馈循环推进；不为了形式创建 Task Graph 或 worktree。

### 升级：Task Graph

只有当 approved Specification 包含两个或以上可独立交付的能力、存在真实前置依赖，或 wide refactor 需要 expand → migrate → contract 时，才读取 references/task-graph.md。先让用户确认 ticket 粒度和直接 blocker，再实现 ready frontier。

### 并行 trial

并行不是默认优化。只有 Graph 已批准、至少有两个 ready ticket、各 ticket 有独立验证 seam、没有共享未完成契约、context pointers 已齐备，并且已经定义 integration branch 与合并后验证时，才允许 worktree + 多 Agent。任一条件失效就退回单 Agent 顺序路径。

GitHub Issue/PR 管协作和合并，SDD 文档管任务规格。实现发现规格问题时，回到上游变更流程。

任务完成后按 references/run-log-schema.md 追加运行记录；不要把完整对话、敏感数据或大段命令输出复制进日志。
