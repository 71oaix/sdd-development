---
title: 开发循环九步详解
source: sdd-development
type: reference
---

# 开发循环（九步）

```
① 提出/确认 issue → ② 编写 plan → ③ plan 独立 review → ④ 人确认 plan
→ ⑤ 实现 → ⑥ 实现独立 review → ⑦ 测试验证 → ⑧ 人确认合并 → ⑨ 归档
```

## 各步骤要点

| 步骤 | 做什么 | 产物/要求 |
|------|--------|----------|
| ① issue | 要做什么：背景、目标、范围（含明确**不做**）、验收标准 | `docs/issues/open/YYYY-MM-DD-简述.md`，frontmatter 填 kind/priority/triage/areas；顶部必须有决策摘要 |
| ② plan | 怎么做：任务解释、关键决策、实现步骤、测试方案、需更新文档 | `docs/plans/open/YYYY-MM-DD-简述.md`（与 issue 同名），须满足 [artifacts.md](artifacts.md) 要求；顶部必须有决策摘要 |
| ③ plan review | 开独立 review（fresh context 的 subagent），查遗漏/矛盾/不可验证点 | review 意见合入 plan 后才算完成 |
| ④ 人确认 | 只展示 plan 摘要（方法 + 取舍 + 保守效果 + 决策点），等待用户批准 | **未批准不得进入实现**；默认不要求用户阅读实施步骤或完整 review |
| ⑤ 实现 | 按 plan 步骤写代码，完成一项更新一项 | 每步可追踪 |
| ⑥ 实现 review | 独立 review 检查与 plan 一致性、代码质量 | 问题修复后才算完成 |
| ⑦ 测试 | 单元测试 / 最小验证，按 areas 圈定范围 | 记录验证结果 |
| ⑧ 人确认合并 | 展示关键改动说明 + 预览地址 | 用户批准后提交/PR |
| ⑨ 归档 | issue+plan 移入 close/，status 改 archived | 同步 INDEX.md |

## 子流程约定

- **issue 与 plan 同名**：`YYYY-MM-DD-简述.md`，便于互相引用
- **issue 前置自检（可选）**：对「要解决什么」不确定时，先按 [issue-precheck.md](issue-precheck.md) 跑一次双向钢人，再写 issue；产物（重述后的真实问题、关键变量）写入 issue 的背景 / 目标。纯执行小任务直接跳过
- **GitHub 并行**：本地 SDD 文档全部进 git 仓库推送 GitHub；GitHub issue/PR 管协作与合并，SDD 文档管任务规格（见项目 AGENTS.md）
- **跳过规则**：用户明确豁免、或纯文档/一行改动等小任务时，可跳过 plan/review 步骤，但事后必须补文档记录

## 面向决策者的摘要交付

### Issue 摘要

issue 汇报先回答：问题是什么、影响谁、优先级建议是什么、是否值得进入 plan、需要用户决定什么。摘要用于排序，不等于批准开发。

### Plan 摘要

plan 汇报先回答：准备采用什么方法、关键取舍是什么、确定/可能/未知的效果分别是什么、需要用户确认什么。实施步骤、测试细节和 review 仍保留在源文件，默认不复制到汇报消息。

### 效果纪律

没有基线或验证条件时必须写“未知”；“显著提升”“完全解决”“零回归”等结论只有在有对应证据时才能写入最终摘要。
