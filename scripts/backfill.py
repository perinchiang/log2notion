import argparse
import pendulum
from notion_helper import NotionHelper
import utils
from config import TARGET_ICON_URL 

def backfill_relations():
    helper = NotionHelper()
    print("🚀 开始执行：全量同步旧日记关联与【对应日期】图标...")
    
    # 获取所有日记
    all_pages = helper.query_all(helper.day_database_id)
    print(f"📦 共找到 {len(all_pages)} 篇日记。")

    count = 0
    # 基础图标 API 地址
    ICON_BASE_URL = "https://api.wolai.com/v1/icon?type=1&locale=cn&pro=0&color=red&method=f1"

    for index, page in enumerate(all_pages):
        try:
            page_id = page.get("id")
            properties = page.get("properties")
            
            # 1. 核心：提取这篇日记【自己的日期】
            # 兼容 Date 或 日期 属性
            date_prop = properties.get("Date") or properties.get("日期")
            if not date_prop or not date_prop.get("date"):
                continue
                
            # 拿到日记页面里的日期字符串 (例如 "2025-12-25")
            this_page_date_str = date_prop.get("date").get("start")
            # 转化为时间对象
            this_page_date = pendulum.parse(this_page_date_str).in_timezone("Asia/Shanghai")
            
            # 💡 关键：这里必须取这篇日记的 day，不能用 pendulum.now()
            day_num = this_page_date.day 

            # 2. 重新计算关联（确保英文属性 Year, Month, Week, All 都有值）
            relation_ids = {
                "Year": helper.get_year_relation_id(this_page_date),
                "Month": helper.get_month_relation_id(this_page_date),
                "Week": helper.get_week_relation_id(this_page_date),
                "All": helper.get_relation_id("All", helper.all_database_id, "https://www.notion.so/icons/site-selection_gray.svg")
            }

            # 3. 准备更新的属性数据
            new_props = {
                "Year": utils.get_relation([relation_ids["Year"]]),
                "Month": utils.get_relation([relation_ids["Month"]]),
                "Week": utils.get_relation([relation_ids["Week"]]),
                "All": utils.get_relation([relation_ids["All"]])
            }

            # 4. 🔴 动态生成图标：确保 &day= 后面跟的是这篇日记的 day_num
            target_icon_url = f"{ICON_BASE_URL}&day={day_num}"
            new_icon = {
                "type": "external",
                "external": {"url": target_icon_url}
            }

            # 5. 执行强制更新
            helper.client.pages.update(
                page_id=page_id, 
                properties=new_props, 
                icon=new_icon
            )
            
            count += 1
            if count % 10 == 0:
                print(f"🔄 已成功同步 {count} 篇页面的图标与关联...")
            
        except Exception as e:
            print(f"❌ 处理第 {index+1} 页时出错: {e}")

    print(f"\n🎉 任务完成！共处理了 {count} 篇日记。")

if __name__ == "__main__":
    backfill_relations()
