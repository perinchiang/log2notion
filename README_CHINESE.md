# 🚀 Notion Life OS: Fully Automated Diary (Auto-Sync)

**全自动化 Notion Life OS 日记系统**

> 基于 [duolingo2notion](https://github.com/malinkang/duolingo2notion) 二次开发，一个自动化的 Life OS 每日日记管理系统。

## 🌟 项目亮点 (Features)

市面上的 Notion 自动化脚本大多功能单一，本项目的目标是**“全自动化的一天”**：

1. **📅 全自动日记创建**：
* 每天凌晨自动生成当天的日记 Page。
* **智能关联**：自动计算并关联到对应的 **Year（年）**、**Month（月）**、**Week（周）** 和 **All（全部）** 数据库，无需手动维护。
* 支持动态图标（根据日期变化的日历图标）。

3. **✍️ 智能字数统计 (Word Count)**：
* 每天深夜自动回扫当天的日记。
* 自动统计正文字数并填入属性，配合 Rollup 实现月度/年度字数汇总。

4. **🎨 极致的画廊视图支持 (Gallery View)**：
* 配合 Notion Formula 2.0，提供了一套**彩虹进度条**和**心情光谱**公式。
* 自动在月/周/年视图展示：`篇数进度`、`字数汇总`、`心情分布能量条`。



---

## 🛠️ 效果预览 (Preview)

*(这里建议你放 1-2 张截图，比如你的月度画廊视图、每天自动生成的日记页面)*

* **月度画廊 (Monthly Gallery)**：自动统计本月进度与心情分布。
* **每日页面 (Daily Page)**：自动关联所有层级，包含多邻国打卡卡片。

---

## ⚙️ 部署教程 (How to Use)

### 1. 准备 Notion 数据库

你需要一个包含以下层级的 Life OS 系统（建议直接复制模板）：

* **Day (日)**
* **Week (周)**
* **Month (月)**
* **Year (年)**
* **All (全部)**

**Day 数据库必须包含以下属性（区分大小写）：**
| 属性名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `Name` | Title | 标题 |
| `Date` | Date | 日期 |
| `Word Count` | Number | 字数统计 |
| `Mood` | Relation | 关联到你的心情数据库 |
| `Year` | Relation | 关联到 Year 库 |
| `Month` | Relation | 关联到 Month 库 |
| `Week` | Relation | 关联到 Week 库 |
| `All` | Relation | 关联到 All 库 |

### 2. Fork 本仓库

点击右上角 Fork 到你的 Github 账号。

### 3. 配置 Github Secrets

进入仓库的 `Settings` -> `Secrets and variables` -> `Actions`，添加以下变量：

| Secret Name | 说明 |
| --- | --- |
| `NOTION_TOKEN` | 你的 Notion Integration Token |
| `NOTION_PAGE` | 你的 Notion 主页链接（包含所有数据库的页面） |
| `JWT` | 多邻国的 JWT Token (登录 web 版 F12 获取) |
| `USER_NAME` | 多邻国用户名 |

### 4. 自动化运行

项目配置了 Github Actions：

* **每天 00:05**：自动创建当天日记。
* **每天 23:45**：自动统计当天日记字数并回填。

---

## 🧠 高级玩法：Notion 公式分享

本项目配套了一套强大的 Notion Formula 2.0 公式，用于在画廊视图中展示进度条和心情。

**月度/年度画廊公式 (Gallery Formula):**
/* === 第一部分：基础数据 === */
("📝 篇数： " + prop("Rollup_Entries") + " 篇").style("b", "blue") 
+ "\n" + 
("✍️ 字数： " + prop("Rollup_Wordcount") + " 字").style("b", "green") 
+ "\n" + 

/* === 第二部分：周进度条 (分母改为 7) === */
let(
    /* 周满勤按 7 天算 */
    target, 7,
    rawProgress, round(prop("Rollup_Entries") / target * 10),
    
    let(
        fillCount, if(rawProgress > 10, 10, rawProgress),
        emptyCount, if(rawProgress > 10, 0, 10 - rawProgress),
        
        ("📅 进度： " + 
        substring("■■■■■■■■■■", 0, fillCount) + 
        substring("□□□□□□□□□□", 0, emptyCount) + 
        " " + format(round(prop("Rollup_Entries") / target * 100)) + "%").style("b", "pink")
    )
) 
+ "\n" + 

/* === 第三部分：心情能量条 (完全复用月度的逻辑) === */
let(
    moodList, 
    prop("Day").map(current.prop("Mood").first().prop("Mood Type").format()),

    let(
        hCount, moodList.filter(current.contains("Positive")).length(),
        nCount, moodList.filter(current.contains("Neutral")).length(),
        sCount, moodList.filter(current.contains("Negative")).length(),
        total, hCount + nCount + sCount,

        if(total == 0, "😶 本周暂无心情记录".style("i", "gray"),
            let(
                hBlock, floor(hCount / total * 10),
                nBlock, floor(nCount / total * 10),
                sBlock, 10 - hBlock - nBlock, 
                
                ("🌈 心情： " + 
                substring("■■■■■■■■■■", 0, hBlock).style("green") + 
                substring("■■■■■■■■■■", 0, nBlock).style("gray") + 
                substring("■■■■■■■■■■", 0, sBlock).style("red")) 
                + "\n" +
                ("😆 " + format(round(hCount / total * 100)) + "%").style("b", "green") + "   " + 
                ("😐 " + format(round(nCount / total * 100)) + "%").style("b", "gray") + "   " + 
                ("😫 " + format(round(sCount / total * 100)) + "%").style("b", "red")
            )
        )
    )
)

---

## 🤝 致谢 (Credits)

本项目修改自 [malinkang/duolingo2notion](https://github.com/malinkang/duolingo2notion)。感谢原作者提供的多邻国爬虫逻辑。

---

### 💡 还有什么要补充的吗？

如果你有 Notion 的模板链接（Duplicate Link），也可以贴上去，这样别人“一键复制模板 + Fork 代码”就能跑起来，Star 数绝对蹭蹭涨！祝你的项目大火！🔥
