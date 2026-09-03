---
title: Three-Space Handoff 兼容规则
source: sdd-development
type: reference
status: active
created: 2026-09-03
updated: 2026-09-03
contract-version: 0.1.0
---

# Three-Space Handoff 兼容规则

## 读取时机

收到 three-space-development 的 Specification Package，或判断某个输入是否达到实现条件时读取。

## 当前支持版本

| Handoff Version | 状态 | 说明 |
|---|---|---|
| 0.1.0 | supported | 初版 Problem、Intention、Specification、Solution Architecture 和 Acceptance Contract |

## 必须存在的内容

- handoff_version；
- handoff_status；
- problem_statement；
- intention_summary；
- approved_specification；
- solution_architecture；
- acceptance_criteria；
- known_risks；
- open_decisions；
- traceability。

## 接收门

只有 handoff_status 为 ready，且用户已经批准规格时，才能进入 SDD issue 和 plan。

以下情况必须返回上游：

- 仍有阻塞性 open decision；
- 输入输出不清楚；
- 失败行为未定义；
- 验收标准不可测试；
- Solution Architecture 与 Specification 冲突；
- 需要重新判断用户目标或系统边界。

## 版本兼容

- Patch：只改文字、示例或非语义说明；
- Minor：新增可选字段或兼容行为；
- Major：删除字段、改变字段含义或改变交接流程。

破坏性变更时，SDD 先支持新旧版本，再由 three-space-development 切换生产版本。

## SDD 侧输出

SDD 将 Handoff 转换为：

- implementation issue；
- implementation plan；
- test cases；
- verification evidence；
- 必要时的 specification change request。

SDD 不得通过 issue、plan 或代码静默改变上游 Specification 的语义。
