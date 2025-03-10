import os
import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import argparse
import glob
import time
import random

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("已加载 .env 文件中的环境变量")
except ImportError:
    print("dotenv 模块未安装，将直接使用环境变量")

def get_producthunt_token():
    """获取 Product Hunt 访问令牌"""
    # 优先使用 PRODUCTHUNT_DEVELOPER_TOKEN 环境变量
    developer_token = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
    if developer_token:
        print("使用 PRODUCTHUNT_DEVELOPER_TOKEN 环境变量")
        return developer_token
    
    # 如果没有 developer token，尝试使用 client credentials 获取访问令牌
    client_id = os.getenv('PRODUCTHUNT_CLIENT_ID')
    client_secret = os.getenv('PRODUCTHUNT_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise Exception("Product Hunt client ID or client secret not found in environment variables")
    
    # 使用 client credentials 获取访问令牌
    token_url = "https://api.producthunt.com/v2/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(token_url, json=payload)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        print(f"获取 Product Hunt 访问令牌时出错: {e}")
        raise Exception(f"Failed to get Product Hunt access token: {e}")

def fetch_product_image(product_url, token, retry_count=0, max_retries=3):
    """从 Product Hunt API 获取产品图片 URL"""
    # 从 URL 中提取产品 slug
    match = re.search(r'/posts/([^?]+)', product_url)
    if not match:
        print(f"无法从 URL 提取产品 slug: {product_url}")
        return None
    
    slug = match.group(1)
    
    # 构建 GraphQL 查询
    query = """
    {
      post(slug: "%s") {
        name
        media {
          url
          type
        }
      }
    }
    """ % slug
    
    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "ImageFixScript/1.0"
    }
    
    try:
        # 添加随机延迟，避免请求过于频繁
        delay = 2 + random.random() * 3  # 2-5秒的随机延迟
        print(f"等待 {delay:.2f} 秒后请求 API...")
        time.sleep(delay)
        
        response = requests.post(url, headers=headers, json={"query": query})
        
        # 处理 429 错误（请求过多）
        if response.status_code == 429:
            if retry_count < max_retries:
                retry_delay = (2 ** retry_count) * 10  # 指数退避: 10, 20, 40秒...
                print(f"API 请求过多 (429)，将在 {retry_delay} 秒后重试 ({retry_count + 1}/{max_retries})...")
                time.sleep(retry_delay)
                return fetch_product_image(product_url, token, retry_count + 1, max_retries)
            else:
                print(f"达到最大重试次数，无法从 API 获取图片: {product_url}")
                return None
        
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'post' in data['data'] and data['data']['post'] and 'media' in data['data']['post']:
            media = data['data']['post']['media']
            if media and len(media) > 0:
                return media[0]['url']
        
        print(f"API 返回数据中没有找到图片 URL: {json.dumps(data)}")
        return None
    except Exception as e:
        print(f"获取产品图片 URL 时出错: {e}")
        
        # 如果是网络错误或服务器错误，尝试重试
        if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) or \
           (isinstance(e, requests.exceptions.HTTPError) and e.response.status_code >= 500):
            if retry_count < max_retries:
                retry_delay = (2 ** retry_count) * 5  # 指数退避: 5, 10, 20秒...
                print(f"网络错误，将在 {retry_delay} 秒后重试 ({retry_count + 1}/{max_retries})...")
                time.sleep(retry_delay)
                return fetch_product_image(product_url, token, retry_count + 1, max_retries)
        
        return None

def fetch_og_image_url(url, retry_count=0, max_retries=3):
    """从网页获取 Open Graph 图片 URL（备用方法）"""
    try:
        # 添加随机延迟，避免请求过于频繁
        delay = 1 + random.random() * 2  # 1-3秒的随机延迟
        print(f"等待 {delay:.2f} 秒后请求网页...")
        time.sleep(delay)
        
        response = requests.get(url, timeout=15)
        
        # 处理 429 错误（请求过多）
        if response.status_code == 429:
            if retry_count < max_retries:
                retry_delay = (2 ** retry_count) * 5  # 指数退避: 5, 10, 20秒...
                print(f"网页请求过多 (429)，将在 {retry_delay} 秒后重试 ({retry_count + 1}/{max_retries})...")
                time.sleep(retry_delay)
                return fetch_og_image_url(url, retry_count + 1, max_retries)
            else:
                print(f"达到最大重试次数，无法从网页获取图片: {url}")
                return None
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找 og:image meta 标签
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                return og_image["content"]
            # 备用: 查找 twitter:image meta 标签
            twitter_image = soup.find("meta", name="twitter:image") 
            if twitter_image and twitter_image.get("content"):
                return twitter_image["content"]
        return None
    except Exception as e:
        print(f"获取 OG 图片 URL 时出错: {url}, 错误: {e}")
        
        # 如果是网络错误或服务器错误，尝试重试
        if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) and retry_count < max_retries:
            retry_delay = (2 ** retry_count) * 5  # 指数退避: 5, 10, 20秒...
            print(f"网络错误，将在 {retry_delay} 秒后重试 ({retry_count + 1}/{max_retries})...")
            time.sleep(retry_delay)
            return fetch_og_image_url(url, retry_count + 1, max_retries)
        
        return None

def fix_markdown_file(file_path, token):
    """修复 Markdown 文件中缺失的图片链接"""
    print(f"正在处理文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用正则表达式查找产品块
    product_blocks = re.findall(r'## \[\d+\. (.+?)\]\((.+?)\)[\s\S]+?!\[\1\]\(([^\)]*)\)', content)
    
    if not product_blocks:
        print(f"在文件中未找到产品块: {file_path}")
        return False
    
    modified = False
    
    for product_name, product_url, image_url in product_blocks:
        # 如果图片 URL 为空，尝试获取
        if not image_url:
            print(f"正在获取产品图片 URL: {product_name}")
            
            # 首先尝试从 API 获取
            new_image_url = fetch_product_image(product_url, token)
            
            # 如果 API 获取失败，尝试从网页获取
            if not new_image_url:
                print(f"从 API 获取图片 URL 失败，尝试从网页获取: {product_name}")
                new_image_url = fetch_og_image_url(product_url)
            
            if new_image_url:
                print(f"成功获取图片 URL: {product_name} -> {new_image_url}")
                # 替换图片链接
                old_pattern = f"![{product_name}]()"
                new_pattern = f"![{product_name}]({new_image_url})"
                content = content.replace(old_pattern, new_pattern)
                modified = True
            else:
                print(f"无法获取图片 URL: {product_name}")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"已更新文件: {file_path}")
        return True
    else:
        print(f"文件无需更新: {file_path}")
        return False

def process_files_in_batches(files, token, batch_size=5, pause_between_batches=60):
    """分批处理文件，每批之间暂停一段时间"""
    total_files = len(files)
    print(f"总共需要处理 {total_files} 个文件，每批 {batch_size} 个，批次间暂停 {pause_between_batches} 秒")
    
    for i in range(0, total_files, batch_size):
        batch = files[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_files + batch_size - 1) // batch_size
        
        print(f"\n开始处理第 {batch_num}/{total_batches} 批文件...")
        
        for file_path in batch:
            fix_markdown_file(file_path, token)
        
        # 如果不是最后一批，暂停一段时间
        if i + batch_size < total_files:
            print(f"\n第 {batch_num}/{total_batches} 批处理完成，暂停 {pause_between_batches} 秒后继续...")
            time.sleep(pause_between_batches)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='修复 Markdown 文件中缺失的图片链接')
    parser.add_argument('--start-date', help='开始日期 (YYYY-MM-DD)', default='2025-02-22')
    parser.add_argument('--end-date', help='结束日期 (YYYY-MM-DD)', default='2025-03-10')
    parser.add_argument('--file', help='指定要修复的单个文件路径')
    parser.add_argument('--all', action='store_true', help='修复 data 目录下的所有文件')
    parser.add_argument('--batch-size', type=int, default=5, help='每批处理的文件数量')
    parser.add_argument('--pause', type=int, default=60, help='批次间暂停的秒数')
    args = parser.parse_args()
    
    # 获取 Product Hunt 访问令牌
    token = get_producthunt_token()
    
    if args.file:
        # 修复指定的单个文件
        if os.path.exists(args.file):
            fix_markdown_file(args.file, token)
        else:
            print(f"文件不存在: {args.file}")
    elif args.all:
        # 修复 data 目录下的所有文件
        files = glob.glob('data/producthunt-daily-*.md')
        process_files_in_batches(sorted(files), token, args.batch_size, args.pause)
    else:
        # 修复指定日期范围内的文件
        try:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
            end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError:
            print("日期格式错误，请使用 YYYY-MM-DD 格式")
            return
        
        # 收集指定日期范围内的所有文件
        files = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            file_path = f"data/producthunt-daily-{date_str}.md"
            
            if os.path.exists(file_path):
                files.append(file_path)
            else:
                print(f"文件不存在: {file_path}")
            
            current_date += timedelta(days=1)
        
        # 分批处理文件
        if files:
            process_files_in_batches(files, token, args.batch_size, args.pause)
        else:
            print("没有找到需要处理的文件")

if __name__ == "__main__":
    main() 