---
title: Implementation Architecture 决策规则
source: sdd-development
type: reference
status: active
created: 2026-09-16
updated: 2026-09-16
---

# Implementation Architecture 决策规则

## 边界

Solution Architecture 属于 three-space-development，描述系统边界、高层组件关系和关键不变量。Implementation Architecture 属于 SDD，描述为了实现 approved Specification 而选择的模块、接口、seam、测试面和代码组织。它可以细化，不可以悄悄改变系统边界、输入输出语义、失败行为、领域规则或 Acceptance。

## 默认词汇与目标

- **Module**：有 interface 和 implementation 的任何规模单元；不要把层级名自动当成模块。
- **Interface**：caller / test 必须知道的全部使用事实，包括不变量、顺序、错误模式、配置和性能特征。
- **Depth**：小 interface 背后隐藏多少行为；目标是高 leverage 和高 locality，而不是堆实现行数。
- **Seam**：可以替换行为而不修改调用处的 interface 所在位置；seam 是位置决策，不等于系统边界。
- **Adapter**：在 seam 上满足 interface 的具体实现。
- **AI navigability**：一个 agent 是否能沿稳定的领域名、pointer、单一 interface 找到行为、测试和证据，而不在浅包装之间来回跳转。

## 选择 heuristics

在 plan 的关键决策中，依次问：

1. 一个小而稳定的 interface 能否隐藏更多复杂度，让 caller 和 test 少学一些事实？
2. 变化、bug、知识和验证能否集中在一个 deep module，形成 locality？
3. deletion test：删除这个模块后，复杂度会消失，还是会散回 N 个 caller？如果只是 pass-through，避免新增一层。
4. interface 是否自然成为 test surface；测试是否可以通过 public interface 观察行为，而不用探入 implementation？
5. seam 是否由真实变化证明？一个 adapter 往往只是 hypothetical seam；生产 adapter + test adapter 才是有理由的 seam。
6. 是否可以“先让 change 容易，再做容易的 change”？任何 prefactor 必须是范围明确、可验证、不会引入未来 speculative generality 的小步。

常见的可测试形状是：注入系统边界依赖、让 module 返回结果而不是让 caller 观察隐藏副作用、减少 interface 方法和参数；mock 优先放在真正外部边界，不 mock 自己控制的内部 module。

## Design-it-twice：条件试验

当 interface / seam 的形状会锁定多个后续 ticket、成本高或一旦选错会造成大范围返工时，才做 design-it-twice。先在 plan 中写清约束、依赖类别和可观察目标，再提出至少两个明显不同的 interface 方案，比较 depth、locality、seam placement、testability 和 AI navigability，记录选择理由。可以请求独立探索，但不为了形式启动并行 Agent；普通单 ticket 直接选择并记录一个足够清楚的方案。

这个试验只决定 Implementation Architecture，不把函数名、类名、数据库表名或代码步骤反向写入 Three-Space Specification。若探索结果说明 approved Specification 不可实现，停止并提交 Specification Change Request。
