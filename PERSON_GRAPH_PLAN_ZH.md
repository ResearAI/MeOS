# MeOS Person Graph Skill 方案草案

## 1. 背景与目标

MeOS 目前已经在做一件很重要的事：把用户的长期稳定 operating layer 沉淀成可复用资产，而不是把历史聊天原样塞进 memory dump。

下一步应该补的是一层更明确的 `Person Graph`：

- 让 Agent 更系统地理解用户是谁
- 让 Agent 更稳定地遵循用户的个性、偏好、兴趣、行为方式和工作风格
- 让这些理解有证据链、有层次、有范围边界，而不是只靠一段 persona prompt

这个图的目标不是“画出历史消息流”，而是“把一个人作为个体的稳定特征结构化”。

一句话定义：

> MeOS Person Graph 的核心目的是让 Agent 更懂你的个性和偏好，并在真实任务中以更像你的方式协作。

## 2. 核心产品定义

### 2.1 我们要解决什么问题

今天的大多数 agent 定制方式，通常只做到以下几种之一：

- 把用户写成一段 prompt
- 存一些偏好笔记
- 从聊天历史里做零散总结
- 记录少量 rules 和 corrections

这些方式的问题是：

- 不成体系
- 没有证据链
- 容易过拟合一次性表达
- 很难区分全局特征与特定场景特征
- 难以在 `apply` 阶段稳定地“像这个用户一样工作”

MeOS Person Graph 要解决的是：

- 如何把用户的个性、偏好、兴趣、行为、原则、边界和工作方式抽出来
- 如何把这些抽取结果变成可追踪、可更新、可冲突管理的结构
- 如何在使用 skill 时，把这些结构转换成真正影响 agent 行为的风格与决策约束

### 2.2 核心命题

MeOS 不应该只是“记住你说过什么”，而应该做到：

- 理解你是什么样的人
- 理解你喜欢怎样被协作
- 理解你通常怎样判断、怎样推进事情、怎样做取舍
- 在新任务里按这些特征来组织 reasoning、workflow、output 和 correction handling

### 2.3 非目标

以下内容不应作为 Person Graph 的目标：

- 纯粹的聊天回放
- 心理学式的人格诊断
- 夸张的角色扮演
- 对用户情绪和人生经历的主观脑补
- 与未来 agent 协作无关的私密信息堆积

## 3. 设计原则

### 3.1 Owner-Centric，而不是 Transcript-Centric

图的中心节点不是 session，不是 turn，不是 prompt，而是 `owner`。

会话、文档、项目、任务、产出，都只是证据来源和上下文，不是图的最终核心。

### 3.2 Claim-First，而不是 Summary-First

底层真相单元不是“摘要段落”，而是 `claim`。

也就是：

- 用户偏好什么
- 用户回避什么
- 用户长期关注什么
- 用户通常如何做决策
- 用户在哪些上下文下呈现出何种风格

每个 claim 都必须有：

- 类型
- 作用范围
- 置信度
- 稳定度
- 证据链
- 冲突管理

### 3.3 Scope-Aware，而不是把人压扁

同一个人会在不同上下文里表现不同：

- coding 任务里偏好短、直接、可执行
- research review 里偏好细、严、可审计
- 产品讨论里偏好更关注体验与表达

这不是冲突，而是 `scope` 不同。

Person Graph 必须支持：

- `global`
- `domain`
- `project`
- `task_family`

### 3.4 Evidence-Backed，而不是拍脑袋的人设

任何进入稳定图的内容，都必须有证据基础。

优先级从高到低：

- 明确用户自述
- 明确用户纠正
- 重复出现的选择或拒绝
- 跨上下文重复行为
- 助手侧单向推断

### 3.5 Style Alignment，而不是戏剧化 Roleplay

MeOS 要做的是“风格对齐”，不是“人格表演”。

Agent 在应用阶段应该：

- 遵循用户稳定的表达偏好
- 遵循用户稳定的判断偏好
- 遵循用户稳定的 workflow 偏好
- 遵循用户稳定的审美和输出习惯

但不应该：

- 虚构用户没有说过的人生观
- 模仿夸张口头禅
- 编造情绪和身份设定
- 为了“像”而损害准确性

### 3.6 Human-Editable

图谱不是黑箱模型。

任何关键产物都应该让人能看懂、能改、能删：

- claims
- evidence
- conflicts
- graph views
- apply contract

## 4. Person Graph 的目标结构

## 4.1 三层结构

### Person Layer

描述“这个人是什么样的人”：

- `owner`
- `role`
- `interest`
- `preference`
- `principle`
- `behavior`
- `workflow`
- `constraint`
- `knowledge`
- `taste`

### Context Layer

描述“这些特征在哪些上下文里成立”：

- `domain`
- `project`
- `task_family`
- `tool`
- `artifact_type`
- `time_period`

### Evidence Layer

描述“为什么我们认为这是真的”：

- `session`
- `turn_excerpt`
- `document`
- `decision_note`
- `artifact_snapshot`
- `correction_record`

## 4.2 底层 claim 模型

建议 Person Graph 底层以 claim 为核心，图只是 claim 的投影。

建议结构：

```json
{
  "id": "claim_xxx",
  "subject": "owner",
  "dimension": "preference|interest|behavior|principle|constraint|role|knowledge|taste",
  "predicate": "prefers|interested_in|tends_to|values|avoids|identifies_as|knows|likes",
  "object": "concise_actionable_output",
  "scope": "global|domain:research|project:MeOS|task:code_review",
  "explicitness": "explicit|inferred",
  "stability": "weak|candidate|stable",
  "confidence": 0.82,
  "first_seen": "2026-04-01",
  "last_seen": "2026-04-08",
  "evidence_ids": ["ev_12", "ev_34"],
  "conflicts_with": []
}
```

图上的投影示例：

- `owner --prefers--> concise_actionable_output`
- `owner --avoids--> long_prefatory_explanations`
- `owner --interested_in--> agent_systems`
- `owner --values--> evidence_first_reasoning`
- `owner --uses_workflow--> inspect_then_patch_then_verify`

## 4.3 关键节点类型

### Identity 类

- `owner`
- `role`
- `domain`
- `project`

### Preference 类

- `input_preference`
- `output_preference`
- `format_preference`
- `interaction_preference`
- `ui_taste`

### Behavior 类

- `decision_style`
- `workflow_pattern`
- `correction_pattern`
- `planning_pattern`
- `verification_pattern`

### Value / Principle 类

- `principle`
- `constraint`
- `anti_pattern`

### Interest / Knowledge 类

- `interest`
- `topic`
- `knowledge_domain`
- `artifact_affinity`

## 4.4 关键边类型

- `prefers`
- `avoids`
- `values`
- `tends_to`
- `uses_workflow`
- `interested_in`
- `works_on`
- `belongs_to_scope`
- `supported_by`
- `conflicts_with`
- `promoted_from`
- `overrides`

## 5. 抽取对象定义

Person Graph 不是抽“所有内容”，而是只抽“会影响未来 agent 协作方式的稳定特征”。

### 5.1 应该抽取的内容

- 明确表达过的偏好
- 明确表达过的讨厌和禁忌
- 重复纠正过的 framing 错误
- 重复采用的任务推进方法
- 长期投入的兴趣主题
- 长期使用的判断标准
- 稳定的输出风格
- 稳定的审美倾向
- 明确的身份定位和工作语境

### 5.2 不应该抽取的内容

- 一次性情绪化表达
- 纯寒暄
- 无复用价值的私人细节
- 没有证据支撑的心理标签
- 与协作行为无关的人格归因

## 6. 抽取维度与判定标准

### 6.1 Preference

定义：用户希望 Agent 以什么方式服务自己。

高信号：

- 明确说“我希望你……”
- 在多个任务中反复选择同一输出方式
- 对格式、长度、结构做重复纠正

示例：

- 偏好简洁直接
- 偏好结论先行
- 偏好可执行建议而非泛泛分析

### 6.2 Interest

定义：用户愿意持续投入注意力和时间的主题。

高信号：

- 跨时间反复回到同一领域
- 自发拓展、追问、深入
- 围绕同一主题建立项目或资料积累

示例：

- 对 agent systems 感兴趣
- 对 research workflow 感兴趣
- 对个体建模与偏好建模感兴趣

### 6.3 Behavior

定义：用户在真实工作中反复表现出的动作模式。

高信号：

- 多次重复相同推进序列
- 多次重复相同检查方式
- 多次重复相同纠偏机制

示例：

- 先看结构，再定方案，再要求落地
- 先要 framing，再要 SOP，再要 plan
- 不满足于抽象结论，要求可执行化

### 6.4 Principle

定义：用户认为什么是“应该”或“不应该”的协作方式。

高信号：

- 明确纠正价值判断
- 对质量标准、真实性标准有重复要求
- 对方法论有稳定规范

示例：

- 反对空泛 persona 化
- 重视 evidence-backed 结论
- 强调 scope 和边界

### 6.5 Constraint

定义：用户明确不接受什么。

高信号：

- 明确的负向纠正
- 多次重复的拒绝信号
- 对某种输出类型有明确排斥

示例：

- 不要只谈代码实现
- 不要做聊天流图
- 不要把用户压平成 prompt persona

### 6.6 Role / Knowledge / Taste

定义：

- `role` 是用户如何定位自己
- `knowledge` 是用户稳定拥有的领域能力
- `taste` 是用户在表达和结果上的长期审美倾向

高信号：

- 自我定位 + 跨任务一致行为
- 在某类问题上持续高水平判断
- 对结果呈现反复给出同方向偏好

## 7. Person Graph 抽取 SOP

## 7.1 Init SOP

适用于第一次建立 Person Graph。

### Step 1. Source inventory

从允许的本地来源中选高价值材料：

- 本地会话历史
- 项目文档
- correction notes
- task / quest history
- 用户提供的长期资料

### Step 2. Evidence slicing

把原材料切成最小证据单元。

要求：

- 一个 evidence unit 只承载一个高信号判断
- 不把整段长对话原样搬进图
- 必须保留原始出处引用点

### Step 3. Candidate claim extraction

对每个 evidence unit 提问：

1. 这条材料在说明这个人的什么？
2. 这是偏好、兴趣、行为、原则、边界、角色、知识还是审美？
3. 这是用户明确说的，还是行为推断的？
4. 这是全局特征，还是范围受限特征？
5. 这条信息是否会改变未来 agent 的协作方式？

### Step 4. Normalization

把自然语言证据标准化成统一 claim。

例如：

- 原始表达：别给我太多铺垫，直接告诉我怎么做
- 标准化后：
  - `owner --prefers--> concise_actionable_output`
  - `owner --avoids--> long_prefatory_explanations`

### Step 5. Scoring

为每个 claim 打分：

- explicitness
- repetition
- cross-context recurrence
- recency
- conflict
- scope clarity

### Step 6. Scope assignment

为每个 claim 标注作用范围：

- `global`
- `domain:*`
- `project:*`
- `task_family:*`

### Step 7. Conflict review

检查：

- 真冲突
- 假冲突
- 范围不同
- 时间更新导致的覆盖

### Step 8. Promotion

按稳定度分流：

- `weak` -> 仅进入 `evidence`
- `candidate` -> 进入候选 claim 集
- `stable` -> 进入稳定图，并可同步进入 `assets`

### Step 9. Apply contract generation

从稳定图中生成一个 `alignment packet`，供 `apply` 模式读取。

## 7.2 Refresh SOP

适用于已有 Person Graph 的增量刷新。

### Step 1. 读取现有稳定图和候选 claim

先看已有结构，再处理新增材料，避免重复创建。

### Step 2. 只处理新增高价值材料

重点关注：

- 新的用户纠正
- 新的长期重复模式
- 新出现的稳定兴趣或角色转向
- 对旧规则的明确覆盖

### Step 3. 合并而不是堆叠

如果新材料支持旧 claim：

- 更新 `last_seen`
- 提升 confidence
- 增加 evidence count

如果新材料限制旧 claim：

- 缩小 scope
- 标记 conflict
- 视情况生成 override

### Step 4. 更新 alignment packet

确保 apply 阶段读取的是最新稳定特征。

## 7.3 Apply SOP

这是 Person Graph 真正发挥作用的地方。

### Step 1. Task typing

先判断当前任务是什么类型：

- coding
- research
- review
- planning
- writing
- product / design

### Step 2. Retrieve relevant graph slice

不要读全图，只读取最相关的部分：

- 当前 task family 相关 claims
- 当前 domain 相关 claims
- 全局高优先级 claims
- corrections / constraints

### Step 3. Compile alignment packet

建议生成一个简明的 apply 合同，例如：

```json
{
  "tone": ["direct", "concise", "non-fluffy"],
  "reasoning_style": ["evidence-first", "scope-aware", "structure-before-detail"],
  "workflow_style": ["inspect-first", "plan-then-commit", "concrete-deliverable"],
  "output_preferences": ["clear plan", "explicit tradeoffs", "actionable next steps"],
  "constraints": ["avoid shallow persona prompts", "avoid flow-only modeling"],
  "task_scoped_traits": ["for concept work, emphasize ontology and SOP"]
}
```

### Step 4. Execute with alignment

Agent 在执行任务时，应让以下层面被图谱影响：

- reasoning
- workflow
- output structure
- tone
- tradeoff framing
- correction handling

### Step 5. Self-check before responding

回答前自检：

- 是否符合当前用户偏好
- 是否踩到了已知禁忌
- 是否遵循了用户的稳定判断风格
- 是否在准确性和风格之间做了正确优先级排序

### Step 6. Write back only stable changes

如果当前任务暴露出新的稳定特征，再写回 graph；否则不增加噪声。

## 8. 风格模拟与人格对齐规则

## 8.1 基本原则

MeOS 在 `apply` 模式下，不只是“参考用户偏好”，而是应该明确按用户特征来组织协作方式。

这意味着 skill 应具备一个显式规则：

> 在不损害真实性、安全性和任务准确性的前提下，Agent 应尽量遵循用户稳定的个性风格、偏好和工作习惯来回答与执行。

## 8.2 模拟的对象是什么

要模拟的是用户的 `working personality`，不是用户完整人生人格。

应该模拟：

- 说话的直接程度
- 结构化偏好
- 细节密度偏好
- 判断和取舍方式
- 审美与输出倾向
- 对错误和风险的敏感点
- 推进任务的典型节奏

不应该模拟：

- 编造人生经历
- 戏剧化口头禅
- 情绪表演
- 与任务无关的人格标签

## 8.3 Apply 优先级顺序

在 apply 阶段，所有风格与行为约束按以下优先级生效：

1. 当前用户消息中的明确要求
2. 明确 corrections / overrides
3. 当前 task family 下的稳定 claims
4. 当前 domain 下的稳定 claims
5. 全局稳定 claims
6. 候选 claims
7. 模型默认风格

## 8.4 必须遵守的边界

- 风格对齐不能覆盖事实准确性
- 风格对齐不能覆盖安全规则
- 风格对齐不能覆盖当前用户最新指令
- 风格对齐不能把候选特征伪装成确定事实
- 风格对齐不能把 scope 受限规则误当全局规则

## 8.5 Skill 提示词层面的新增要求

建议在 MeOS skill 中加入一条明确指令：

> 当进入 apply 模式时，不仅要读取相关 assets，还要读取相关 person-graph slice，并显式让输出风格、推理方式、工作节奏和 correction handling 与用户的稳定特征保持一致。

建议再加入一条负向约束：

> 这种对齐不是角色扮演。不要夸张模仿，不要编造心理画像，不要让“像用户”压过“对用户有用”。

## 9. Claim 打分与晋升规则

建议采用以下维度：

- `explicitness`
- `repetition`
- `cross_context`
- `recency`
- `conflict_penalty`
- `scope_clarity`

建议晋升门槛：

- `0-2`: 只进 evidence
- `3-5`: 候选 claim
- `6+`: 稳定 claim

特殊规则：

- 明确用户纠正：高优先级，直接进入稳定层，但仍需记录 evidence
- 与旧规则冲突：不直接覆盖，先进入 conflict review
- 明显只在特定场景成立：必须带 scope 才能晋升

## 10. 图的可视化视图

建议 Person Graph 至少导出以下五种视图：

### 10.1 Identity Map

展示：

- owner
- roles
- domains
- long-term projects

### 10.2 Preference Map

展示：

- input preferences
- output preferences
- format preferences
- collaboration preferences
- taste preferences

### 10.3 Behavior Map

展示：

- workflow habits
- decision style
- planning style
- verification style
- correction patterns

### 10.4 Interest Map

展示：

- recurring topics
- sustained interests
- domain clusters
- artifact affinities

### 10.5 Constraint / Correction Map

展示：

- anti-patterns
- explicit rejections
- overrides
- high-priority behavior constraints

每个节点建议显示：

- confidence
- stability
- scope
- first_seen
- last_seen
- evidence_count

## 11. 与现有 MeOS 资产的关系

Person Graph 不是要替代现有 assets，而是给现有 assets 增加一个结构层。

关系应该是：

- `assets/`：人类可读的长期规范与画像资产
- `evidence/`：证据记录与 claim 账本
- `runtime/graph/`：图的结构产物与可视化产物
- `private/`：原始历史材料

即：

- `assets` 是 canonical prose
- `graph` 是结构化索引
- `evidence` 是追溯依据

## 12. 建议的文档与文件规划

建议新增：

- `SKILL/references/person-graph-sop.md`
- `SKILL/references/graph-ontology.md`
- `SKILL/references/claim-scoring-policy.md`
- `SKILL/references/style-alignment-policy.md`

建议新增 schema：

- `SKILL/schemas/claim-entry.schema.json`
- `SKILL/schemas/person-graph.schema.json`
- `SKILL/schemas/alignment-packet.schema.json`

建议新增本地数据文件：

- `SKILL/evidence/claims.jsonl`
- `SKILL/evidence/claim-conflicts.jsonl`
- `SKILL/evidence/claim-source-map.json`

建议新增运行时产物：

- `SKILL/runtime/graph/owner-graph.json`
- `SKILL/runtime/graph/owner-graph.svg`
- `SKILL/runtime/graph/owner-graph.html`
- `SKILL/runtime/graph/preference-map.svg`
- `SKILL/runtime/graph/behavior-map.svg`

## 13. 分阶段落地计划

### Phase 0. 定位与文案统一

目标：

- 在 README 顶部明确 MeOS 的核心目的是让 Agent 更懂你的个性和偏好
- 在 skill 描述中加入“风格对齐”而不只是“资产读取”

产物：

- README 改版
- README_ZH 改版
- 本方案草案

### Phase 1. 本体与 SOP 固化

目标：

- 定义 claim ontology
- 固化 init / refresh / apply 的 graph SOP
- 固化 style alignment policy

产物：

- ontology 文档
- SOP 文档
- scoring policy
- style alignment policy

### Phase 2. 证据层与 claim 层成形

目标：

- 把 transcript / docs / notes 中的高信号材料转成 claims
- 区分 evidence / candidate / stable

产物：

- claims.jsonl
- conflict records
- source mapping

### Phase 3. Apply 行为真正被图影响

目标：

- 让 Agent 在 apply 模式下显式按 person graph 工作
- 让 output / reasoning / workflow / tone 被用户特征校准

产物：

- alignment packet
- apply behavior contract

### Phase 4. 图视图与导出

目标：

- 提供 owner-centric 可视化
- 支持按维度看用户画像

产物：

- identity map
- preference map
- behavior map
- interest map
- constraint map

### Phase 5. 质量评估与迭代

目标：

- 评估 graph 是否真的让 agent 更懂用户
- 评估纠偏次数是否下降
- 评估用户是否觉得“更像我”

建议指标：

- apply 任务中的重复纠偏次数
- 用户对“像我程度”的主观评分
- graph 中 stable claims 的覆盖率
- claim 冲突率
- scope 标注完整率

## 14. 成功标准

如果 Person Graph 设计成功，应该出现以下结果：

- Agent 能更快进入用户的协作节奏
- 输出更符合用户个性和偏好
- 用户不必在新会话中重复解释自己
- 图能回答“这个人是什么样的人，如何与他协作”而不是只回答“他说过什么”
- 图谱更新后，`apply` 的行为能明显变得更贴近用户

最终标准不是图画得多漂亮，而是：

> Agent 是否真的更懂这个人，并且能按这个人的特征工作。

## 15. 建议写入 README 的一句话定位

推荐中文：

> MeOS 的核心目的，是让 Agent 更懂你的个性、偏好、习惯与工作方式，并在真实任务中以更像你的方式协作。

推荐英文：

> MeOS exists to help agents understand your personality, preferences, and way of working, then collaborate in a way that feels aligned with you.
