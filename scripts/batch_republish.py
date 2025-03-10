import os
import glob
import argparse
import time
from datetime import datetime, timedelta
from republish_to_wordpress import republish_to_wordpress

def batch_republish(start_date, end_date, pause=5):
    """批量重新发布指定日期范围内的 Markdown 文件"""
    # 解析日期
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # 收集文件路径
    files = []
    current = start
    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        file_path = f"data/producthunt-daily-{date_str}.md"
        
        if os.path.exists(file_path):
            files.append(file_path)
        else:
            print(f"警告: 文件不存在: {file_path}")
        
        current += timedelta(days=1)
    
    # 批量发布
    total = len(files)
    print(f"找到 {total} 个文件需要发布")
    
    for i, file_path in enumerate(files, 1):
        print(f"\n处理文件 {i}/{total}: {file_path}")
        republish_to_wordpress(file_path)
        
        # 如果不是最后一个文件，暂停一段时间
        if i < total:
            print(f"暂停 {pause} 秒后继续...")
            time.sleep(pause)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='批量重新发布 Markdown 文件到 WordPress')
    parser.add_argument('--start-date', required=True, help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--pause', type=int, default=5, help='每次发布之间暂停的秒数 (默认: 5)')
    args = parser.parse_args()
    
    # 批量重新发布
    batch_republish(args.start_date, args.end_date, args.pause)

if __name__ == "__main__":
    main() 