---
title: Task Graph 与渐进式实现协议
source: sdd-development
type: reference
status: active
created: 2026-09-16
updated: 2026-09-16
---

# Task Graph 与渐进式实现协议

## 定位与启用门

Task Graph 是 approved Specification 到 implementation 的执行地图，不是新的 Specification，也不拥有修改上游验收目标的权力。默认路径仍是一个 issue、一个 plan、一个 Agent 顺序完成一个 ticket。

只有命中以下任一条件才启用 Graph：

- approved Specification 包含两个或以上可以分别演示或验证的能力；
- ticket 之间存在需要显式表达的真实前置依赖；
- wide refactor 需要 expand → migrate → contract；
- 用户明确要求评估并行，但必须先证明任务边界已经稳定。

纯文案、明确 bug、小字段或一个上下文可以完成的单一能力，不为了形式建立 Graph。

## 小步定义

一个小步是一个边界明确、可独立验证、可追溯到 approved Specification / Acceptance，并在完成后让系统保持可接受状态的能力切片。通常它是 vertical tracer bullet：穿过本次能力实际涉及的所有层和 seam，形成一条可以运行、演示或验证的窄路径；不是把 database、backend、frontend、test 拆成互相不能验证的横向工作包。

小步的五个检查问题：

1. 它交付的是用户或 caller 可观察的完整行为，而不是“新增一张表”或“写完后端”这种层级动作吗？
2. 它能指向至少一个已有的 Specification / Acceptance ID 吗？
3. 它有预先约定的验证方式，并能在本步完成后独立判定通过或失败吗？
4. 它的工作量适合一个 fresh context window；如果不适合，是否可以沿能力边界而非技术层边界继续拆分？
5. 完成本步后，系统是否仍处于可接受状态，且下一步不会依赖未记录的对话记忆？

“fresh context window”是拆分信号和容量护栏，不是要求用固定 token 数估算。若不能满足，应在 plan 中说明为什么不能沿能力边界拆分。

### Wide refactor 例外

只有一个机械变化、blast radius 横跨全仓库、直接拆成 vertical slice 会让所有调用点同时变绿不可能时，才把它标成 wide refactor：

1. **Expand**：新旧形式并存，系统保持可工作；
2. **Migrate**：按 package / directory / 风险批次迁移，每批是一个 ticket，旧形式仍保留；
3. **Contract**：所有调用点迁移并验证后删除旧形式，`blocked_by` 指向所有 migrate ticket。

如果迁移批次无法各自保持绿色，仍保留这个顺序，但把它们放在明确的 integration branch 上，最后增加一个 `integrate-and-verify` ticket；不得把“最终一起才会绿”描述成普通独立 ticket。

## Ticket 记录与状态

启用 Graph 时，使用 [templates/task-graph.json](../templates/task-graph.json) 作为机器可检查的唯一状态真源。每个 ticket 至少有：

| 字段 | 规则 |
|---|---|
| `id` | Graph 内唯一、稳定的 ticket ID。 |
| `delivers` | 用户或 caller 可观察的端到端能力；不要写层级步骤。 |
| `traces_to` | 现有 Intention / Specification / Behavior / Rule / Acceptance ID；不得创造未经批准的验收目标。 |
| `blocked_by` | 只列真正阻塞它的直接前置 ticket；空数组表示可立即开始。 |
| `verification` | 预先约定的测试、检查、演示或人工观察；完成后补充实际证据。 |
| `status` | `draft`、`ready`、`in_progress`、`implemented`、`verified`、`blocked` 或 `cancelled`。 |

可按需增加 `context_pointers`，指向 Specification Package、issue、plan、research note、ADR 或前一个 commit。子 Agent 通过 pointer 读取上下文，不在消息中复制大段规范。

`ready` 的含义是：ticket 自身信息完整，且 `blocked_by` 中的 ticket 全部为 `verified`；因此 ready frontier 是所有 `status=ready` 且直接 blocker 全部 verified 的 ticket。实现完成但未验证只能是 `implemented`，不能解锁后继。

## Blocking edge 的判定

A `blocked_by` B，仅当 A 在 B 未经验证的输出、契约、迁移结果或不变量之前，无法安全地开始，或无法独立完成其预定验证。典型真 blocker 包括：

- B 先建立并验证了 A 必须消费的公开输入输出契约；
- B 先扩展兼容形式，A 才能迁移调用点；
- A 的验收前置条件由 B 产生，且没有可接受的替代 adapter / fixture；
- contract ticket 必须等所有 migrate ticket 验证完才能删除旧形式。

以下不是 blocker，除非存在上面的具体证据：

- 期望的执行顺序、同一个人负责、同一个目录、可能复用代码；
- “先做基础设施比较安心”；
- 两个 ticket 可能触碰相邻文件；这通常是 merge-risk，应通过 seam、批次或 integration verify 管理。

每条 edge 在 plan 中写一句理由。边不确定时先不添加顺序性依赖，记录风险并用探索或集成验证澄清；不要把普通顺序伪装成 blocker。Graph 不得有环，直接边即可，不重复表达传递闭包。

## 用户确认门

在建立 ticket / Graph 后、进入实现前，向用户展示编号列表。每项至少展示：标题、`delivers`、`blocked_by`、验证方式。询问：粒度是否过粗或过细、每条 edge 是否是真 blocker、是否需要合并或拆分。用户批准的是执行分解，不是对 approved Specification 的重新批准；若分解过程中发现规格本身不成立，返回 Specification Change Request。

## Exploration 与 implementation 分离

探索的职责是回答“现状在哪里、哪些 seam 可用、哪些依赖和风险会影响 ticket”，产出短的 research note / context pointer；它不顺手修改实现，也不替实现 Agent 做未批准的设计。Implementation 只读取与当前 ticket 相关的 pointer，按 approved Specification 和已确认 plan 写代码并验证。这样既避免每个 Agent 重复扫描代码库，也避免把探索中的假设伪装成规格或实现事实。

探索笔记至少标出：已确认事实、待验证假设、相关模块 / interface / 测试入口、不会改变的约束。若探索发现输入规格缺失或现实冲突，笔记应指向 Specification Change Request，而不是在 ticket 中自行修正。

## Traceability

Graph 与现有 SDD 追踪关系连接为：

```text
Intention → Specification / Behavior / Rule → Acceptance → Ticket
         → Test / Check → Implementation / Commit → Verification Evidence
```

每个 ticket 的 `traces_to` 至少命中一个现有 Specification 或 Acceptance ID；每个 Acceptance 要么被一个或多个 ticket 覆盖，要么在 plan 中说明为什么不由本次实现覆盖。ticket 结束时把 test / check 的实际结果、commit 和人工观察写入 verification evidence，形成 Gate 3 的证据链。

## 单 Agent 默认循环

对 ready frontier 中的 ticket，默认由一个 Agent 按以下最小反馈回路完成：

1. 读取指向的 Specification、Acceptance、plan 和 context pointers；
2. 在 plan 中确认一个 public seam；
3. 写一个描述行为的失败测试（red），或记录没有合适自动 seam 的人工 / 端到端验证；
4. 写刚好让该验证通过的最小实现（green）；
5. 在 red → green 循环之外做必要的小范围 refactor / review，并保证验证仍通过；
6. 运行目标测试和必要的 typecheck，记录结果；
7. 将 ticket 从 `implemented` 推进为 `verified`，所有 ticket 完成后再运行一次全量或受影响范围测试，然后重新计算 frontier。

测试应通过 public interface / seam 观察行为，不测试私有方法、内部调用次数或可由实现重算的期望值。Mock 优先限于真正的系统边界；内部 collaborator 不能靠 mock 掩盖接口设计问题。

## 并行 frontier：conditional / trial protocol

并行是 Graph 稳定后的可选执行机制，不是默认优化。只有全部满足以下条件才启用：

1. Graph、ticket 粒度和 blocker edges 已由用户确认；
2. ready frontier 至少有两个 ticket；
3. 每个 ticket 都是可独立演示 / 验证的 vertical slice，拥有独立 public seam，不共享未完成的接口、不变量或同一不可分割的迁移批次；
4. 每个 ticket 的 context pointers / exploration notes 已存在，实施 Agent 不需要重复做大范围探索；
5. 每个 ticket 使用自己的 branch / worktree；主分支不直接接收未经验证的工作；
6. 有一个 integration branch 和 merger / integration verifier，规定每次合并后的目标测试、冲突处理和最终全量或受影响范围测试；
7. 任何实现冲突仍在 approved Specification 范围内解决；若冲突暴露规格缺失或不可行，暂停并提交 Specification Change Request。

并行完成后，merger 只合并已经本地验证的 ticket，重新运行集成验证并更新 Graph 状态。反复冲突、验证不能独立运行、上下文重复探索或合并成本高于收益时，立即退回单 Agent 顺序路径。worktree 是隔离执行工具，不是流程完成条件。

## 机器检查

在用户批准 Graph 后运行：

```powershell
python scripts/validate_task_graph.py path\to\task-graph.json
```

脚本检查必填字段、ID 引用、直接 blocker、环、状态一致性和 ready frontier。脚本通过只说明 Graph 结构可执行，不替代 Specification、plan review、测试或用户决策。
