import feedparser
import os
from github import Github
import requests
import random
import time

def fetch_page(url):
    # 设置常见浏览器的 User-Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    ]
    
    # 随机选择 User-Agent
    headers = {'User-Agent': random.choice(user_agents)}
    
    # 模拟随机延迟
    time.sleep(random.uniform(1, 3))
    
    try:
        # 发送 HTTP GET 请求
        response = requests.get(url, headers=headers)
        
        # 确保响应成功
        if response.status_code == 200:
            # 返回响应内容的字符串形式
            return response.text
        else:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to fetch {url}: {str(e)}")
        return ''

# GitHub 仓库信息
REPO_OWNER = 'WendaoLee'
REPO_NAME = 'rss'

# RSS 订阅链接
RSS_FEED_URLS = [
    'https://unbug.github.io/feed.xml',
    'https://www.ruanyifeng.com/blog/atom.xml',
    'https://rsshub.app/jike/user/35224A78-8B11-469E-B307-16B58688FBEC'
]

# 创建或更新 Issue
def create_or_update_issue(title, content):
    github_token = os.getenv('GITHUB_TOKEN')
    github_client = Github(github_token)
    repo = github_client.get_repo(f'{REPO_OWNER}/{REPO_NAME}')
    
    # 查找是否已存在同名的 Issue
    issues = repo.get_issues(state='open')
    existing_issue = None
    for issue in issues:
        if issue.title == title:
            existing_issue = issue
            break
    
    # 创建或更新 Issue
    if existing_issue:
        existing_issue.edit(body=content)
    else:
        repo.create_issue(title=title, body=content)

# 解析 RSS 并将内容推送到 Issue
def rss_to_issue():
    for url in RSS_FEED_URLS:
        feed = feedparser.parse(url)
        if not feed.entries:
            print(f'url:{url} not parsed correctly,trying fetch another way')
            res = fetch_page(url)
            feed = feedparser.parse(res)
            if not feed.entries:
                print(f'url:{url} not parsed correctly')
                continue
    
        latest_entry = feed.entries[0]
        title = latest_entry.title
        content = latest_entry.link
    
        create_or_update_issue(title, content)


if __name__ == '__main__':
    # os.environ['GITHUB_TOKEN'] = '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'
    rss_to_issue()
