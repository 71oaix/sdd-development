---
title: Gate 3 Verification 与 Fixed-Point Review
source: sdd-development
type: reference
status: active
created: 2026-09-16
updated: 2026-09-16
---

# Gate 3 Verification 与 Fixed-Point Review

## 目标

Gate 3 证明“实现已证明、实现有测试证据，并能追溯回规格”。它不是把测试通过、代码 review 和规格符合度混成一个分数，而是保留三类互补证据：可重复的工具结果、Specification Compliance review、Engineering Standards review。

## Fixed point preflight

实现 review 开始前，固定用户指定的 base commit、branch、tag 或 merge-base。没有 fixed point 时先询问，不凭当前 HEAD 猜测。先做以下确定性检查：

1. `git rev-parse <fixed-point>` 成功；
2. 记录 `git diff <fixed-point>...HEAD`，使用三点比较以基于 merge-base；
3. 记录 `git log <fixed-point>..HEAD --oneline`；
4. ref 无效或 diff 为空时立即 fail fast，不把问题交给 reviewer 子 Agent。

空 diff 不是“review 通过”；如果用户要做的是空变更审计，应明确使用另一种审计目标。

## Clean context 与来源

reviewer 必须从干净上下文开始，只读取 fixed point、diff、commit 列表、Specification / issue / plan、相关 standards source 和验证输出，不读取实现 Agent 的推理过程或“我已经检查过”的结论。若没有子 Agent，主 Agent 也要在完成实现上下文后重新按这个最小输入审查。

Specification source 按以下顺序找：

1. commit message 中的 issue / PR / change reference；
2. 用户明确给出的 issue、Specification Package 或 plan 路径；
3. `docs/`、`specs/` 或 `.scratch/` 中与分支 / feature 匹配的文档；
4. 找不到时，请用户提供来源；用户确认没有规格时，Spec 轴记录“no spec available”，不能伪装成通过。

Standards source 包括项目已有的 `AGENTS.md`、`CONTRIBUTING.md`、编码规范、ADR、lint / typecheck / test 配置和本项目要求的文档。工具已经确定的规则交给工具，不重复消耗 reviewer 判断力。

## 两个独立 review 轴

### Spec Compliance

只问实现是否忠实完成来源规格：

- Specification / Acceptance 要求哪些内容缺失或只完成一部分；
- diff 增加了哪些规格没有要求的行为（scope creep）；
- 看似实现了的行为是否在边界、失败路径或输入输出语义上不正确。

每条 finding 都引用 Specification / Acceptance / plan 的具体 ID 或章节，并指出 diff 中的文件 / hunk 证据。规格缺失、冲突或现实不可行时，不由 reviewer 自行放宽规格，提交 Specification Change Request。

### Engineering Standards

只问实现是否满足项目标准和实现质量：

- 先引用仓库明确规则；
- 再把潜在 smell 标成判断性建议，而不是硬违规；
- 可以检查重复逻辑、feature envy、data clumps、primitive obsession、repeated switches、shotgun surgery、divergent change、speculative generality、message chains、middle man、refused bequest 等，但跳过 lint / typecheck / test 已经确定的问题；
- 在实现形状是 load-bearing 时，使用 Implementation Architecture reference 的 module / interface / depth / seam / locality 语言，但不要借 standards 轴偷偷重写规格。

每条 finding 都引用对应的规则文件或 diff hunk，并明确是 hard violation 还是 judgement call。

## 汇总规则

报告固定使用两个独立章节：`## Spec Compliance` 和 `## Engineering Standards`。保留两个轴的发现、证据和处理状态，不合并、不重新排序为单一总分；一个轴通过不能掩盖另一个轴失败。修复后重新审查受影响轴，保留原 finding 与 disposition 供复盘。

## Gate 3 Evidence Pack

最终 plan / verification evidence 至少包含：

| 证据 | 必须记录 |
|---|---|
| Scope | issue、Specification Package、Acceptance IDs、Out of Scope |
| Graph（如适用） | ticket 状态、ready frontier 变化、blocker edge 理由 |
| Tests | ticket 对应的目标测试、typecheck、相关集成 / 端到端 / 全量测试命令和结果 |
| Implementation | ticket 对应 commit、关键改动和文档更新 |
| Spec Compliance | fixed point、source、findings、修复 / 豁免 / SCR |
| Engineering Standards | standards sources、findings、修复 / 豁免、是否为判断性建议 |
| Human acceptance | 需要人工观察的 UI / 运行结果、预览地址或明确“不适用”理由 |

当所有 ticket 都为 `verified`、相关测试证据通过、两个 review 轴没有未处理的阻塞 finding、文档和 `INDEX.md` 同步且不存在未提交的 Specification Change Request 时，才可标记 Gate 3 通过并进入人确认合并。
