# chi-review

CHI/HCI类论文审稿全流程 Agent Skill（适配 Codex / WorkBuddy / Claude ）。

一个严格 CHI 审稿人的完整工作流：诚实批判不奉承、每条批评挂证据、可操作可执行。

## 三种主模式

| 模式 | 触发场景 | 流程 |
|---|---|---|
| **撰写模式**（§A） | 从零起草 review | PDF 提取 → 精读 → 证据核验 → 评分 → 中文工作稿 → 英文定稿 |
| **自查模式**（§B） | 审计已写好的 review 是否与论文相符 | 三轮法：全量审计 → 补漏自纠 → 修订版验证 |
| **外部审查模式**（§C） | 转交第三方核查报告后修订意见 | 版本鉴别 → 逐条核验 → 修订落地 → Form 分数复核 |

## 核心纪律

- **全文覆盖强制**：引用前必须实读完全文，未读区段的"引述"是幻觉高发区
- **引文逐字核对**：每条批评挂原文锚点（§ 号 + 逐字引用）
- **核心设计**：承认已自述 / 引原句证 disclaimer / 精确限定缺口
- **评分纪律**：评-文-荐三方自洽，不为匹配推荐而降分
- **保密红线**：全文不含真实投稿编号、论文名等可识别信息，判例一律匿名化

## 覆盖内容

PDF 提取（pymupdf + 行号锚点）、结构精读清单、11 项 grep 证据核验（伦理/报酬/招募/数字链/引用真实性/模型命名等）、PCS 表单字段填写规则（Research Integrity Flag / Best Paper Nominations / Confidential Comments）、叙事型中文工作稿与英文定稿规范、可复用批评库。

## 相关skills

配套技能：`ref-check`（引用真实性核验，Crossref + arXiv API）。https://github.com/Imad7777/ref-check

配套技能：`paper-citation-tracer`（引文溯源工具 / 论文中引文表述的合理性检验）。https://github.com/Imad7777/paper-citation-tracer

## 免责声明

本技能用于辅助论文评审的起草与自查，评审结论由审稿人本人负责。请遵守目标会议的保密义务与 AI 使用政策。
