---
name: sdd-development
description: >
  当项目采用文档驱动开发（SDD，docs/issues + docs/plans 结构）时，接收已批准的系统规格并开始 issue、plan、实现、测试或交付时触发。关键词：写 issue、做 plan、SDD、开发流程、按流程走、开始开发、实现功能、需求确认、计划评审、计划确认、Specification Package、handoff、实现交付。当目标、边界或架构仍然模糊时不应触发；先交给 three-space-development。纯问答、纯调研或单文件小改动可不触发。
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

① 提出/确认 issue → ② 编写 plan → ③ plan 独立 review → ④ 人确认 plan
→ ⑤ 实现 → ⑥ 实现独立 review → ⑦ 测试验证 → ⑧ 人确认合并 → ⑨ 归档

- 未确认 plan 不得进入实现（用户明确豁免的小改动除外）
- 每完成一个阶段，向用户汇报当前状态与下一步
- 实现 Architecture 可以细化上游 Solution Architecture，但不得无记录地改变其系统边界和核心行为
- 发现规格问题时提交 Specification Change Request，不在代码中静默修正规格

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

每次调用后，如发现新的高频踩坑点，询问用户是否记录到 gotchas.md。操作日志追加到 .run-log.jsonl。累计约 10 条后，主动询问是否总结日志为 gotcha。
