import argparse
import os
import pendulum
from notion_helper import NotionHelper
import utils
from config import RELATION, TITLE, DATE

# 你指定的动态图标 URL
DIARY_ICON = "https://api.wolai.com/v1/icon?type=1&locale=cn&pro=0&color=red&method=f1"

def create_daily_log():
    # 1. 初始化时间 (Asia/Shanghai)
    now = pendulum.now("Asia/Shanghai")
    today_str = now.to_date_string() # 格式: 2026-01-05
    print(f"开始处理日期: {today_str}")

    # 2. 获取关联数据库的 ID (年、月、周、全部)
    # Helper 会自动处理：如果年/月/周的页面不存在，它会自动创建
    relation_ids = {}
    
    # 获取 '年' Page ID (例如: 2026)
    relation_ids["年"] = helper.get_year_relation_id(now)
    
    # 获取 '月' Page ID (例如: 2026年1月)
    relation_ids["月"] = helper.get_month_relation_id(now)
    
    # 获取 '周' Page ID (例如: 2026年第一周)
    relation_ids["周"] = helper.get_week_relation_id(now)
    
    # 获取 '全部' Page ID (Page名为: 全部)
    # 注意：这里我们直接调用 helper 的通用获取关联方法
    relation_ids["全部"] = helper.get_relation_id("全部", helper.all_database_id, "https://www.notion.so/icons/site-selection_gray.svg")

    # 3. 检查当日页面是否已存在
    # 我们通过标题 (2026-01-05) 在日数据库中查找
    day_filter = {"property": "Name", "title": {"equals": today_str}} 
    # 注意：你的截图中"日"数据库的标题属性名是 "Name"，如果不是请在Notion改为"Name"或者修改这里
    
    response = helper.query(database_id=helper.day_database_id, filter=day_filter)
    
    if len(response.get("results")) > 0:
        print(f"页面 {today_str} 已存在，跳过创建。")
        return

    # 4. 组装属性 (Properties)
    properties = {}
    
    # 设置标题 (Name)
    properties["Name"] = utils.get_title(today_str)
    
    # 设置日期 (Date)
    properties["Date"] = utils.get_date(now.to_date_string())
    
    # 设置关联 (Relations)
    properties["年"] = utils.get_relation([relation_ids["年"]])
    properties["月"] = utils.get_relation([relation_ids["月"]])
    properties["周"] = utils.get_relation([relation_ids["周"]])
    properties["全部"] = utils.get_relation([relation_ids["全部"]])

    # 5. 创建页面
    parent = {
        "database_id": helper.day_database_id,
        "type": "database_id",
    }
    
    helper.create_page(
        parent=parent, 
        properties=properties, 
        icon=utils.get_icon(DIARY_ICON) # 使用你指定的 Wolai 动态图标
    )
    
    print(f"成功创建日记页面: {today_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    helper = NotionHelper()
    create_daily_log()
