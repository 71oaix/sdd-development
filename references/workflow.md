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

① 提出/确认 issue → ② 编写 plan → ③ plan 独立 review → ④ 人确认 plan
→ ⑤ 实现 → ⑥ 实现独立 review → ⑦ 测试验证 → ⑧ 人确认合并 → ⑨ 归档

## 各步骤要点

| 步骤 | 做什么 | 产物/要求 |
|------|------|----------|
| ① issue | 要做什么：背景、目标、范围和验收标准 | docs/issues/open/YYYY-MM-DD-简述.md |
| ② plan | 怎么做：任务解释、关键决策、实现步骤、测试方案和文档更新 | docs/plans/open/YYYY-MM-DD-简述.md |
| ③ plan review | 独立检查遗漏、矛盾和不可验证点 | review 意见合入 plan |
| ④ 人确认 | 用户批准方法、取舍和待确认决策 | 未批准不得实现 |
| ⑤ 实现 | 按 plan 写代码并保持追踪 | 每步可追踪 |
| ⑥ 实现 review | 检查实现和 plan 一致性 | 问题修复后继续 |
| ⑦ 测试 | 单元测试、集成测试和最小验证 | 记录验证结果 |
| ⑧ 人确认合并 | 展示关键改动和验证证据 | 用户批准后合并 |
| ⑨ 归档 | issue 和 plan 移入 close/ | 同步 INDEX.md |

GitHub Issue/PR 管协作和合并，SDD 文档管任务规格。实现发现规格问题时，回到上游变更流程。
