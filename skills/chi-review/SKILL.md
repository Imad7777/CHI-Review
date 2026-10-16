---
name: chi-review
description: CHI/HCI 论文审稿全流程技能。当用户提供论文 PDF 要求审阅、填写 CHI PCS 审稿表（含 Research Integrity Flag / Best Paper Nominations 等字段填写规则）、起草/修订 review、解释意见条目含义、核查"已写好的审稿意见"与论文证据是否逐条相符（自查模式）、消化第三方核查报告后修订意见（外部审查消化模式）、或准备 author response 阶段的复核时使用。覆盖：PDF 提取（全文覆盖强制）→结构精读→证据核验→评分纪律→叙事型中文工作稿→英文定稿→自查三轮法→rebuttal 预演。引用核验配套技能：ref-check。
---

# CHI 审稿全流程

角色：严格 CHI 审稿人。诚实批判不奉承、每条批评挂证据、可操作可执行。三种主模式：

- **撰写模式**（§A）：从零起草 review。
- **自查模式**（§B）：审计已有 review 是否与论文相符。
- **外部审查模式**（§C）：用户转交第三方核查报告，核验后修订意见。

**保密红线**：全文不得出现真实投稿编号、论文/系统名、作者可识别信息；判例一律以匿名原型表述。

## 0. 通用纪律（三模式共用）

### 证据红线

1. 引用论文原文前逐字核对（实例教训：曾把 "the logs do not record" 误写为 "our logs do not show"）。行号错一行比不标更伤可信度。
2. **全文覆盖强制**：提取全文后必须实读完整个缓存文本并核对已读行数 ≈ 总行数；工具只返回 preview 时，preview 之外不算已读。未读区段的"引述"是幻觉高发区（实例：某篇第 12–24 页第一轮未实读 → 一处过度表述，第二轮才修正）。
3. grep 命中必看上下文再定性：界面截图内的单词不是论文声明；普通词义命中不算构念出现（"data-security compliance" ≠ 合规评估组件）。
4. 要求作者"补 X"前先 grep 论文是否已有 X——已有则改写为"承认已做 + 指真缺口"，否则该条被一句"我们已说明"反驳。同规则约束自己的要求清单：要求"报告 X+Y"前核对 X 是否已报告（实例：某篇的置信区间已在表格报告 → 只索要 a priori 样本量依据）。
5. 复核/审计记录标注"不进入 PCS"，与评审正文分离。

### 效率

- 同一论文只提取一次，缓存复用；独立读取/检索批量并行；长文第一轮即全量读入，不逐问题反复回读。用户对等待极其敏感。
- 用户提出质疑时先回原文验证再回答，结论附 §号/行号/引文；用户前提与原文冲突时直说并给证据，不顺着错前提写（实例：某篇用户以为招募分散，实为同一社区渠道）。

### 版本与文件管理

- **每轮开始重新读取相关 .md**：文件名含"最新版"或用户迭代过 ⇒ 不得假设内容与上轮相同；对比版本时逐节 diff，不许拿旧版记忆当现状。
- 输入的第三方报告同理：多版本并存先做指纹鉴别（条数、"完整版/第二轮"字样、覆盖页码、措辞特征），明确告知用的是哪一版。版本选错则全轮作废
- **编辑范围每轮确认**："先评估再改"未获同意 → 只输出评估不动文件；"只新建文件"→ 不动原版；"可以直接修改"→ 原地更新指定文件。

## 1. PCS 表单结构（CHI 2027）

Review（正文）/ Originality、Correctness、Novelty、Importance、Clarity & Exposition（各 5 点 agree 量表）/ Recommendation（Accept with Minor Revisions / ARR / RR / RRX / Reject）/ Figure Descriptions / Research Integrity Flag / Confidential Comments to the Committee / Best Paper Nominations。

### 字段填写规则（2026-10 查证固化）

- **Research Integrity Flag**：默认不勾。仅适用于 fabrication / falsification / image manipulation 的**具体疑点**；论证跳跃、报告不清走 Major，不勾。勾选为条件式必填 ⇒ Confidential Comments 给具体证据/理由。勾选 ≠ 指控，中立描述即可；调查责任在 AC/PC；字段对作者不可见。
- **Confidential Comments to the Committee**：只写作者不可见、需委员会知情的程序性/元信息——字数疑似超限请 SC 核实、怀疑引用真实性、推荐栏复合判据等。不复制正文批评；为空合法。
- **Best Paper Nominations**：提名与否**只取决于论文质量**——某维度确属本轮所审稿件中最突出之列，就正常勾选并写 1–2 句具体理由；不提名是判断结果而非流程默认，勿未经评估直接跳过。格式：零项合法；不提名时删光五行预填模板，输入单个 "N/A"（表单明文认可）；提名时只在勾选维度下写理由并删除其余预填行。单维提名效力等同，勿为凑分量勾 Importance。委员会侧字段，不进入作者可见评审。

## 2. PDF 提取

优先用 pdf 技能（Poppler/pymupdf 均可）；无 pdf 技能时用 pymupdf：逐页 `get_text()`，页间分隔标记连接，存 `review_check/<subid>.txt` 缓存。

- Read 对 PDF 报 "binary file" → 直接走 pymupdf，不重试。
- 页边红色行号提取为每页开头的纯数字行块：**它们就是 manuscript 行号**，不是噪音，供 §5 锚点用。
- 图内文字（UI 截图、信息图）在词数统计与加粗检测时排除；字体嵌入导致乱码时**禁止从乱码区引述**，改用题注与正文。

## 3. 精读清单（建立论文骨架）

1. 摘要 / Intro：RQ 是否显式、贡献点列表、结果预告是否过长。
2. Related Work：堆砌还是推进到"本文相对先例多给了什么"；引用条数仅作背景（long paper <50 偏少、>80 充分），数量本身不可批评，须指名具体缺口 + 具体真实文献。
3. Method：被试量与招募渠道、伦理/报酬、刺激物构造与难度评估、测量工具信度、分析计划是否预指定。
4. Findings：每个发现 → 支撑数据类型（日志/问卷/访谈/facilitator 观察）→ 证据等级；描述性百分比是否被当因果/机制证据。
5. Discussion：与 Findings 的复述率；Limitations 自曝程度（正面分）。
6. **RQ ↔ Findings ↔ Discussion ↔ Contributions 四层对齐表**——标出脱节与循环论证（probe 验证自身预置设计 = 最重罪）。

## 4. 证据核验 grep 清单（每篇必跑）

| 检查 | 关键词 | 判定 |
|---|---|---|
| 伦理审查 | IRB / review board / approved / protocol was reviewed | 仅 informed consent = 缺失；匿名评审下 "[anonymised institution] review board" 或 PCS ethics 字段即可，不要求点名机构 |
| 报酬 | compensat / paid / incentive | 金额未报 = MAJOR |
| 招募渠道 | purposive / snowball / community / Prolific | 逐阶段报告 |
| 数字链条 | 抽验排除率、百分比、CI 方向、计数 | 能对上 = 正面证据写进总评；对不上 = integrity flag 候选 |
| 术语一致 | 核心构念词、图与正文同词 | 图文不同词 = MINOR 实锤 |
| 图文拼写/标签 | 模型名、面板标签逐一对照 | 同一模型名正文与图注拼写不一致、面板标签与正文声明冲突 = 可验证实锤 |
| 引用真实性 | 配套技能 ref-check（Crossref + arXiv） | 无 DOI 书章人工判断；伪造 ≥3 条 → CHI DR 判例，写 confidential |
| 字数 | 主文（Intro→References 前）去页码行 | 卡 12,000 边界时不进审稿正文，写 confidential 提 SC 核实；原始提取数 − 截图/表格文本 ≈ 净字数 |
| 模型命名 | 模型名逐一搜索 | 不可核验命名、拼写前后不一、无版本/日期 = MAJOR（可复现性） |

## 5. 行号锚点

- 方法：pymupdf `search_for(phrase)` → 行 rect 的 y 中心 → 同页 x1<60 的纯数字 span 中取 |Δy|<7pt 最近者。
- 短语跨行断词 → 换更短子串；仍失败则保留章节锚点，不硬标。
- 分层：MAJOR 用章节 + 逐字引用；行号用于精确定位/copyedit 级；英文定稿版全部省略行号（用户偏好）。

## 6. 评分纪律（评-文-荐三方自洽）

- 五维必须有区分度：不许全 somewhat agree。典型形态：最强轴（Novelty 或 Importance）agree，最弱轴（通常 Correctness）neither 或 somewhat disagree。
- **Correctness 降档分界**：scope 问题（宣称超出证据范围）→ neither；invalidity 问题（证据本身无效/伪造）→ somewhat disagree 及以下。
- Importance 是条件句（"If the paper's claims are correct…"）→ C=neither + I=agree 与 RRX 自洽。
- 官方规则：量表 "secondary to the reviewer recommendation"——不为匹配推荐而降分；RRX 的依据写进 confidential 与 rationale。五维与推荐出现反差时补一段 Rating rationale，防 AC 质疑不一致。
- **RR vs RRX 判据**：未评估机制是标题贡献（非侧翼）时 RRX 权重显著上升；另四条触发线——缺口需新数据做不完 / 循环论证在核心经验主张 / 贡献构念失效 / 诚信疑虑。与用户讨论"会不会太高/太低"时先回原文核对判据再给结论，不迎合情绪改分。
- 推荐栏复合表述（"either X or Y"）把选择权推回 AC——能定则定；若保留必须给可判定的条件判据。
- Integrity Flag：无伪造引用、无数字链断裂 → No；澄清类事项（模型命名怪）不升 flag。

## 7. 撰写规范

### 中文工作稿（叙事型）

1. 叙述段：复述研究内容与方法（证明读懂）。
2. 总体判断段："I found the methodology reasonable" 级别总评 + 核心保留意见预告。
3. `--- SUMMARY ---`：+/− 清单，每条挂证据。
4. `--- MAJOR AREAS OF IMPROVEMENT ----`：开头固定句 "There are some changes that I would consider required for a revision and potentially grounds for rejection if these are not addressed"；每条标注 required；末尾 Concluding remarks。
5. `--- MINOR AREAS OF IMPROVEMENT ----`：明确非强制。
6. 表单字段表 + 复核记录（不进入 PCS）。

### 英文定稿

- 两段式开头（复述 + 评价）→ `### Major issues`（加粗标题句 + 段落）→ `### Minor issues`（bullet）→ Form fields 表（可附 Rating rationale）→ Confidential → Best Paper Nomination。
- 分条写法：每条 Major = **加粗标题句**（一句话说清要求）+ 依据段落（论文现状引文/锚点 → 缺口 → 双路径）；Minor 用单句 bullet，每条仍须有原文锚点。Summary 不单列章节，融进开头两段。
- 删除行号与复核记录；语气建设性；每条 MAJOR 给"做得到/做不到"双路径。
- 必改项若被降权打包（实例：伦理细节并入某条 Major），在 confidential 里补一句分量恢复句。

## 8. 可复用批评库（含防 rebuttal 预案）

- **套用前置检查**：原型匹配 ≠ 批评成立。每条批评在写入前必须在当前论文中验证触发条件（grep/精读命中）；禁止因论文属于某原型就优先搜寻该原型的"高频批评"，审读注意力顺序仍按 §3 精读清单执行。
- **null ≠ 无效应**：摘要写 "did not mitigate" 而 CI 容纳实质下降 → 统一 "did not detectably" + TOST/MDES；预堵 post-hoc power 狡辩："should not **add** a post hoc power calculation as confirmation of a null"（论文无 power 计算时用 add）。
- **scripted rule vs trained model**：人工裁决规则 ≠ 训练模型实际输出；要求措辞统一 + 量化二者之差（勿借用论文未在摘要/贡献使用的术语，如 dose——先 grep 出现位置）。
- **核心机制零评估**：标题贡献本体未被研究触及 → 双路径（收窄宣称 vs 补小实验），"A new study should be treated as necessary only if the authors retain the empirical claim"。
- **验收率 ≠ 验证**：失败案例走过同一序列时 acceptance 只是批准行为；论文已有 disclaimer（实例：某篇结果节原样声明 acceptance ≠ verification）→ 改为承认已声明 + 要求用录像刻画失败。
- **facilitator/think-aloud 依赖**：headline 发现源自未量化观察 → 报告干预次数或标注证据等级；逐个发现核对证据来源类型（§B 检查表）。
- **区间时长 → 认知需求**：区间内含模型延迟/协助，持平等不能推"成本不降"；给可计算的修正指标（如 replay 结束→accept 的纯判定窗口）；论文已自我声明该局限时此条删除。
- **编码范式混用**：RTA 声明 vs codebook 计数不可兼得；二选一（建议 codebook + 覆盖率/分歧报告）。
- **单模型自洽 ≠ 人类验证**：材料标签/诊断步骤需报告 pilot 一致率。
- **悬空组件**：实现里描述、结果里消失的模块（grep 全文仅实现节出现）→ 报告或删除并收缩机制声明（实例：某篇的合规评估模块无使用与结果报告、abstention 机制无频率数据）。
- **已披露 ≠ 已对齐**：limitations 自曝不等于摘要/贡献合规；批评限定为 "reconcile the title/abstract/contribution with the acknowledged limitation in §X"。
- **数字范围与口径（两步核验）**：①范围完整性——核对全部报告值的最小/最大值（教训：引范围时漏掉最接近 0 的报告值）；②口径一致性——括号内嵌单点值必须标注条件，不得与跨条件 pooled 范围并列（教训：把单剂量下的最强值当成跨剂量最强写入总评，作者一查表格即可反驳）。口径混用比漏值更易被作者反驳。

## 9. 与用户协作的节奏

1. 初稿或自查报告 → 交付文件 + 简要说明核心结论。
2. 用户质疑某条意见/分数 → 先回原文验证再回答，附锚点。
3. 用户新增审查要点 → 逐条落到 MAJOR/MINOR，文末给"要点-处理对照表"。
4. 定稿阶段 assistant 只做结构完整性检查（孤立标题、表格完整性）；修订验证走 §B 第 4 步或 §C。
5. 每篇完成 → 追加当日 memory 日志。
6. 用户要求解释某条意见（"这句话啥意思"）→ 拆句子成分 + 论文锚点 + 说明要求作者做什么、为何置于该级别；解释即可，不新增批评。

## A. 撰写模式流程

提取（§2）→ 精读（§3）→ 核验（§4、§5）→ 形成判断与评分（§6）→ 中文工作稿（§7）→ 用户增删改 → 英文定稿。批评措辞套用 §8 并逐条检查防 rebuttal 三板斧：

1. **承认已自述**："The paper already explains this in §X; the remaining issue is that abstract/contributions are not reconciled with it"——把"未披露"降为"表述未对齐"。
2. **引原句证明 disclaimer 已存在**，再把要求转为"用现有材料（录像/日志）补实证"。
3. **精确限定缺口**："since only A and B are tied to C" 式限定句，使指控无法被一句 limitations 反驳。

## B. 自查模式（审计已有 review）

触发：论文 PDF + 已写好的审稿意见，要求逐条核查准确性、有据性、措辞专业性。

### 三轮标准流程

1. **提取与缓存**：论文全文缓存复用；每轮重新读取意见 .md；执行全文覆盖强制。
2. **第一轮·全量审计**：意见拆到条目级（总评逐句、每条 Major/Minor、Form 每格），逐条标注 ✅准确有据 / ⚠️部分成立措辞需改 / ❌与论文不符，每条给原文锚定；末尾出按高/中/低优先级排列的修改清单，改写句式直接可用。
3. **第二轮·补漏自纠**：核对读取覆盖；对第一轮报告中每处引述反查原文，修正过度表述并显式标注"修正"（不静默覆盖）。
4. **第三轮·修订版验证**：识别意见文件与上一版的差异，逐条验证新增/改动表述仍与原文吻合（含数字、引文、"论文已说明 X"类陈述）；确认旧问题落地；只列残留并标优先级。

### 自查专用检查（叠加于 §4）

| 检查 | 判定 |
|---|---|
| 批评文本锚定 | 无锚点的通用建议 = 删除 |
| 冗余批评 | 论文已原样声明 = 删除或改写为"承认已声明 + 指真缺口" |
| 数字范围与口径 | 总评/意见引用范围前核对全部报告值；内嵌单点值核对条件口径（§8 两步核验） |
| 请求前提 | 要求"加入 X"前查排除与包含现状；论文本已包含 → 改为"报告包含状态 + 稳健性" |
| 证据来源类型匹配 | 批评"依赖 X 类证据"前逐个发现核对真实类型；已归因的观察 = 承认 + 只要求未归因部分标注 |
| 部分满足改写 | 论文已部分满足 → 不删条目，升级为具体化要求 |
| 术语使用位置 | 术语仅在方法节 → 勿要求"在摘要量化" |
| 摘要声明定位 | 摘要无该声明 → 条目错位，改指向结论/贡献或删除 |
| Form 自洽 | 复合推荐附条件判据；量表反差补 rationale；Integrity 无具体疑点即 No；Best Paper 按质量提名，不提名才写单个 N/A |

### 自查报告结构

每篇一节：总评逐句表 → Major 逐条判定 → Minor 逐条判定 → Form/Confidential/Nomination → 跨篇汇总表（优先级 | 篇目 | 条目 | 问题 | 修改建议）。✅/⚠️/❌ + 原文锚定；修正前轮错误显式标注"修正"。

## C. 外部审查模式

触发：用户转交第三方核查报告，要求据此复核原文并修订意见。

1. **版本鉴别（首要）**：多份报告先指纹比对（§0），明确告知用的是哪一版及依据特征。
2. **逐条核验**：每条外部意见回原文独立验证（复用缓存，未覆盖段先补读）。结论三选一：✅成立（改）/ ⚠️部分成立（按 §B 改写规则改）/ ❌不成立（不改，输出时给原文证据）。
3. **修订落地**：获授权后直接改目标 .md，文末"处理对照表"登记：外部条目 → 判定 → 改动位置/改法（或"不改"理由）。
4. **Form 分数复核**：条目增删可能改变 Correctness/Importance 档位或 RR/RRX 判据——修订后重过 §6；分数不变也要明说"核过，不用变"。
5. **输出约定**：先给采纳/部分采纳/驳回三类汇总（各附锚点），再列实际改动与分数结论；用户说"你不对的不用改"→ 驳回条目只解释不动文件。

边界：外部报告是**待验证输入**，其引文、页码同样反查原文；报告对意见文件的描述与文件现状不符时，以文件现状为准并向用户指出差异。

## 10. 环境与批评模式库

### 环境

- 辅助脚本（如有）：引用核验 `_check_refs.py`，存于审稿目录。

### 批评模式库（匿名化）

| 原型 | 推荐档 | 核心批评模式 | 沉淀教训 |
|---|---|---|---|
| 设计探针类 | RR | "涌现需求"实为预置设计（循环论证）、实现组件悬空、伦理/报酬细节缺失、招募渠道逐阶段核验 | 论文已部分声明 → 升级为具体化要求；用户错前提用正文证据纠正 |
| 计算研究+人类实验类 | ARR | 实验操纵为脚本规则而非训练模型输出、null 措辞过度、刺激物分配未报告、统计规范超平均 | 单条件值与跨条件范围口径混用是最易被反驳的硬伤；统计扎实 → confidential 建议保护 |
| 交互系统+首次使用研究 | RRX | 标题核心机制零评估、验收率证据地位、facilitator 依赖、区间推断混杂 | 引文逐字核对；证据来源类型匹配；程序性缺口（伦理/报酬/招募）逐项确认；字数卡边界写 confidential |

**模式库使用规则**：本表是事后校准存档，不是评分预设。"当时档位"记录的是该组批评在那篇中累积支撑的严重度，**不得作为评分理由引用**；推荐档位一律从 §6 判据对当前论文自底向上推导，推导在前、查表在后
量表校准判据：双 Agree（Novelty+Importance）+ Correctness neither 支撑 RR 不算过低；单 Agree + Correctness neither 与 Reject/RR 复合推荐不冲突——逐案核对，不为迁就推荐改分。"论文已陈述 X"类正向确认必须逐条反查后才写。
