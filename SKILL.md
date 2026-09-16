---
name: sdd-development
description: >
  当项目采用文档驱动开发（SDD，docs/issues + docs/plans 结构），并且已经有用户批准且 handoff_status=ready 的 Specification Package，需要把规格转换为 issue、plan、ticket、实现、测试或交付时触发。关键词：写 issue、做 plan、SDD、开发流程、按流程走、开始实现、计划评审、计划确认、Specification Package、handoff、实现交付。当目标、边界、核心行为、失败行为或 Solution Architecture 仍然模糊，或任务仍处于 Problem / Intention / Specification 澄清阶段时不应触发；先交给 three-space-development。纯问答、纯调研或单文件小改动可不触发。
---

# SDD 开发流程

> 仿 Harness Engineering 实践。
> 核心信念：文档是 Agent 的上下文底座——一切需要被知道的知识都应文档化，人只做决策。

本 Skill 负责批准规格之后的 issue、plan、implementation、verification 和 delivery。它消费上游的 Specification Package，不替代上游定义问题或系统规格。

## 文件地图

> 路径均相对于本 skill 目录。按需读取，不一次性全量加载。

| 文件 | 何时读 |
|------|--------|
| references/workflow.md | 开始任何开发任务时（九步循环 + handoff preflight） |
| references/three-space-handoff-compatibility.md | 收到 three-space-development 的 Specification Package 时 |
| references/issue-precheck.md | 写 issue 前、对「要解决什么」不确定时（可选） |
| references/artifacts.md | 编写 plan / 汇报合并时（人决策所需信息，硬性要求） |
| references/docs-discipline.md | 涉及创建或更新文档时（五层映射、doc-contract、INDEX） |
| references/task-graph.md | approved Specification 需要拆成多个 ticket，或需要判断 blocker / ready frontier 时 |
| references/verification-review.md | 实现 review、Gate 3 验证或准备合并时 |
| references/implementation-architecture.md | 模块、接口、seam 或重构形状是实现决策时（可选） |
| references/run-log-schema.md | 任务完成后记录运行证据、或复盘 Skill 机制时 |
| templates/task-graph.json | 启用 Task Graph 时，作为机器可检查的 ticket 清单模板 |
| templates/run-log-record.json | 追加结构化 v0.2 运行记录时 |
| templates/retrospective.md | 累计约 5–10 次可比运行后做机制复盘时 |
| scripts/validate_task_graph.py | 启用 Task Graph 时，做确定性结构、引用、环和 frontier 检查 |
| scripts/validate_run_log.py | 校验旧版和 v0.2 `.run-log.jsonl` 记录结构时 |
| gotchas.md | 遇到问题、收尾检查、或准备跳过流程步骤时 |

## 上游输入边界

three-space-development 负责：

- Problem Discovery；
- Intention 澄清；
- Specification；
- Solution Architecture；
- 用户批准和验收目标。

SDD 负责：

- 接收和检查 approved Specification Package；
- 将规格转成 implementation issue 和 plan；
- 选择 Implementation Architecture；
- 编码、测试、review、合并和归档；
- 反馈规格缺失或不可行的问题。

当输入仍然缺少目标、边界、核心行为、失败行为或验收标准时，SDD 不得直接进入实现，应返回 Specification Change Request。

## Handoff Preflight

收到 Specification Package 后，先读取 references/three-space-handoff-compatibility.md，检查：

- handoff_version 是否支持；
- handoff_status 是否为 ready；
- Problem、Intention 和 Specification 是否完整；
- In Scope 和 Out of Scope 是否明确；
- Solution Architecture 是否有决策和理由；
- Acceptance Criteria 是否可执行；
- Open Decisions 是否为空或明确不阻塞。

Preflight 未通过时，不创建“可直接实现”的 plan；应将缺口返回 three-space-development。

## 工作流程

在 Handoff Preflight 通过后，执行：

① 提出/确认 issue（必要时建立 Task Graph）→ ② 编写 plan → ③ plan 独立 review → ④ 人确认 plan
→ ⑤ 按 ticket 实现并逐步验证 → ⑥ fixed-point clean-context 实现 review → ⑦ 测试与 Gate 3 验证 → ⑧ 人确认合并 → ⑨ 归档

- 未确认 plan 不得进入实现（用户明确豁免的小改动除外）
- 默认单 ticket、单 Agent 顺序实现；只有在 Task Graph 已稳定且 ready frontier 中存在真正独立的 ticket 时，才按 references/task-graph.md 的条件启用并行 trial。
- 每完成一个阶段，向用户汇报当前状态与下一步
- 实现 Architecture 可以细化上游 Solution Architecture，但不得无记录地改变其系统边界和核心行为
- 发现规格问题时提交 Specification Change Request，不在代码中静默修正规格

## 执行路由

- 简单任务走单 issue + 单 plan + 单 ticket 的轻量路径；按 references/workflow.md 运行 seam-first 验证，不为了形式创建 Graph 或 worktree。
- 多能力、真实依赖或 wide refactor 读取 references/task-graph.md；其中的 `delivers`、`traces_to`、`blocked_by`、`verification` 和 `status` 是执行层规则，不改变上游 Specification。
- 实现 review、Gate 3 和 fixed-point clean-context 双轴检查读取 references/verification-review.md；模块、接口或 seam 形状有负载时才读取 references/implementation-architecture.md。
- 任务完成后读取 references/run-log-schema.md，追加一条结构化运行记录；累计约 5–10 次可比运行后使用 templates/retrospective.md 做机制复盘，不把一次成功直接固化成 gotcha 或规则。

## 关键原则

1. 先文档后代码：没有 plan 就不写实现
2. 规格在 docs 里，不在对话里：不依赖对话记忆
3. 人确认两件事：确认 Plan、确认合并
4. 文档是交付物：改完代码同步更新文档和 INDEX.md
5. 实现偏差必须可追溯：偏差属于规格问题时回流上游

## GitHub 与源仓库

本 Skill 源仓库是可编辑、可审阅、可回滚的真源。用户 Skill 目录中的安装副本只用于运行，不直接编辑。

推荐协作方式：

- main 只接受 PR；
- 每个任务一个分支；
- 小步提交；
- PR 描述说明范围、测试和相关契约版本；
- 合并后再更新安装副本；
- 远程地址必须明确配置，不对未知远程推送。

跨 Skill 变更必须同时说明：

- producer contract version；
- consumer supported version；
- compatibility status；
- 是否需要 Specification Change Request。

## 与其他 Skill 的关系

- three-space-development：问题、意图、规格和 Solution Architecture。
- think：需要架构判断和方案取舍时使用。
- doc-contract：创建、更新或归档 issue、plan 等文档时使用。
- sdd-plan-report：编写 plan 时使用。
- project-doc-architecture / docs-scan：文档目录和 INDEX 维护时使用。
- hunt：已有错误、崩溃或回归需要找根因时使用。

## 自迭代规则

每次调用完成后，按 references/run-log-schema.md 向 .run-log.jsonl 追加一条 v0.2 运行记录；保留历史 legacy 记录，不回写迁移。只记录机制使用、结果、成本和 evidence pointer，不记录完整对话或敏感数据。

如发现新的高频踩坑点，仍需询问用户是否记录到 gotchas.md；累计约 5–10 次可比运行后，按 templates/retrospective.md 做一次机制复盘，再决定 adopt、trial、simplify 或 remove，不因单次成功直接膨胀 Skill。
