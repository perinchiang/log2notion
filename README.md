# 🚀 Notion Life OS: Fully Automated Diary (Auto-Sync)

**A Fully Automated Notion Life OS Diary System**

[中文](https://github.com/perinchiang/notion-automated-diary/main/README_CHINESE) | [English](https://github.com/perinchiang/notion-automated-diary/main/README.md)

> Built on top of **duolingo2notion**, this project is a fully automated Life OS diary system for managing your daily logs in Notion.

---

## 🌟 Features

Most existing Notion automation scripts focus on only one specific function.
This project aims to deliver **“a fully automated day”**:

### 📅 Fully Automated Daily Diary Creation

* Automatically creates a new diary page every day at midnight.
* **Smart Relations**: Automatically calculates and links the diary to:

  * **Year**
  * **Month**
  * **Week**
  * **All**

  No manual maintenance required.
* Supports **dynamic icons** (calendar icons that change based on the date).
* Supports importing old diary entries
  (after importing, manually run **Backfill Old Data** once).

### ✍️ Intelligent Word Count

* Automatically processes the daily diary late at night.
* Counts the total number of words in the content and writes it back to a property.
* Works seamlessly with **Rollups** to generate monthly and yearly word count summaries.

### 🎨 Advanced Gallery View Support

* Powered by **Notion Formula 2.0**.
* Includes:

  * 🌈 **Rainbow progress bars**
  * 🎭 **Mood spectrum formulas**
* Automatically displays in **Month / Week / Year** gallery views:

  * Entry progress
  * Word count summaries
  * Mood distribution energy bars

---

## 🛠️ Preview

* **Monthly Gallery View**: Automatically shows monthly progress and mood distribution.
* **Daily Page**: Fully linked across all hierarchy levels.

![](https://images-1314261959.cos.ap-guangzhou.myqcloud.com/img/20260106181711895.png)

![](https://images-1314261959.cos.ap-guangzhou.myqcloud.com/img/20260106215456970.png)

![](https://images-1314261959.cos.ap-guangzhou.myqcloud.com/img/20260106214523177.png)

---

## ⚙️ How to Use

### 1. Prepare Your Notion Databases

You need a Life OS system with the following hierarchy:

* **Day**
* **Week**
* **Month**
* **Year**
* **All**

**The Day database must contain the following properties (case-sensitive):**

| Property Name | Type     | Description                    |
| ------------- | -------- | ------------------------------ |
| `Name`        | Title    | Page title                     |
| `Date`        | Date     | Diary date                     |
| `Word Count`  | Number   | Daily word count               |
| `Mood`        | Relation | Relation to your Mood database |
| `Year`        | Relation | Relation to Year database      |
| `Month`       | Relation | Relation to Month database     |
| `Week`        | Relation | Relation to Week database      |
| `All`         | Relation | Relation to All database       |

---

### 2. Fork This Repository

Click **Fork** in the top-right corner to copy the repository to your GitHub account.

---

### 3. Configure GitHub Secrets

Go to `Settings` → `Secrets and variables` → `Actions`, and add the following secrets:

| Secret Name    | Description                          |
| -------------- | ------------------------------------ |
| `NOTION_TOKEN` | Your Notion Integration Token        |
| `NOTION_PAGE`  | Notion Page ID (32-character string) |

---

### 4. Automation Schedule

This project uses **GitHub Actions** to run automatically:

* **00:05 daily** — Create the diary page for the day.
* **23:45 daily** — Calculate word count and write it back to Notion.

---

## 🤝 Credits

This project is based on and modified from
[malinkang/duolingo2notion](https://github.com/malinkang/duolingo2notion).
