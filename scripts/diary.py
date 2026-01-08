import argparse
import pendulum
from notion_helper import NotionHelper
import utils
import time
from config import RELATION, TITLE, DATE

# 动态图标
DIARY_ICON = "https://api.wolai.com/v1/icon?type=1&locale=cn&pro=0&color=red&method=f1"

def get_text_from_blocks(blocks):
    """递归提取 Block 中的纯文本"""
    text_content = ""
    for block in blocks:
        b_type = block.get("type")
        if b_type in block and "rich_text" in block[b_type]:
            rich_texts = block[b_type].get("rich_text", [])
            for rt in rich_texts:
                text_content += rt.get("plain_text", "")
        if block.get("has_children"):
            pass
    return text_content

def update_word_count(page_id, title="未知日期"):
    """统计页面Word Count并更新"""
    # 增加 title 参数方便日志查看
    print(f"   📝 正在统计: {title} ...", end="")
    try:
        blocks = helper.get_block_children(page_id)
        full_text = get_text_from_blocks(blocks)
        clean_text = full_text.replace(" ", "").replace("\n", "")
        count = len(clean_text)
        
        properties = {
            "Word Count": utils.get_number(count) 
        }
        helper.update_page(page_id, properties)
        print(f" ✅ {count} 字")
        
    except Exception as e:
        print(f" ❌ 失败: {e}")

# --- 新增函数：同步最近 N 天的字数 ---
def sync_recent_word_counts(days=7):
    # 1. 计算 N 天前的日期
    start_date = pendulum.now("Asia/Shanghai").subtract(days=days).to_date_string()
    print(f"\n🔍 开始检查最近 {days} 天 ({start_date} 以来) 的日记字数...")

    # 2. 构建过滤条件 (利用 Notion API 过滤，而不是拉取所有数据)
    filter_params = {
        "property": "Date", # 你的数据库日期字段叫 "Date"
        "date": {
            "on_or_after": start_date
        }
    }

    # 3. 查询符合条件的页面
    # 注意：这里直接调用 query，不需要 query_all，因为7天的数据量很少，不需要分页
    response = helper.query(database_id=helper.day_database_id, filter=filter_params)
    pages = response.get("results", [])
    
    print(f"📦 找到 {len(pages)} 篇近期日记，准备更新字数。")

    # 4. 循环更新
    for page in pages:
        page_id = page.get("id")
        # 获取标题用于显示
        props = page.get("properties")
        title_prop = props.get("Name") or props.get("标题")
        title = "未知日期"
        if title_prop and title_prop.get("title"):
            title = title_prop.get("title")[0].get("plain_text")
            
        update_word_count(page_id, title)
        time.sleep(0.5) # 防止触发 API 限制

def create_daily_log():
    now = pendulum.now("Asia/Shanghai")
    today_str = now.to_date_string()
    print(f"🚀 开始今日任务: {today_str}")

    # 1. 检查今日页面是否存在
    day_filter = {"property": "Name", "title": {"equals": today_str}}
    response = helper.query(database_id=helper.day_database_id, filter=day_filter)
    
    if len(response.get("results")) > 0:
        print(f"✅ 今日页面 {today_str} 已存在。")
    else:
        # 创建新页面逻辑 (保持不变)
        print(f"✨ 创建新页面: {today_str}")
        relation_ids = {}
        relation_ids["Year"] = helper.get_year_relation_id(now)
        relation_ids["Month"] = helper.get_month_relation_id(now)
        relation_ids["Week"] = helper.get_week_relation_id(now)
        relation_ids["All"] = helper.get_relation_id("All", helper.all_database_id, "https://www.notion.so/icons/site-selection_gray.svg")

        properties = {}
        properties["Name"] = utils.get_title(today_str)
        properties["Date"] = utils.get_date(today_str)
        properties["Year"] = utils.get_relation([relation_ids["Year"]])
        properties["Month"] = utils.get_relation([relation_ids["Month"]])
        properties["Week"] = utils.get_relation([relation_ids["Week"]])
        properties["All"] = utils.get_relation([relation_ids["All"]])
        properties["Word Count"] = utils.get_number(0)

        parent = {"database_id": helper.day_database_id, "type": "database_id"}
        helper.create_page(parent=parent, properties=properties, icon=utils.get_icon(DIARY_ICON))

    # --- 核心修改：无论今日页面是否新建，都执行一次最近7天的字数同步 ---
    sync_recent_word_counts(7)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    helper = NotionHelper()
    create_daily_log()
