import feedparser
import os
from github import Github

# GitHub 仓库信息
REPO_OWNER = 'WendaoLee'
REPO_NAME = 'rss'

# RSS 订阅链接
RSS_FEED_URLS = [
    'https://unbug.github.io/feed.xml',
    'https://www.ruanyifeng.com/blog/atom.xml'
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
            return
    
        latest_entry = feed.entries[0]
        title = latest_entry.title
        content = latest_entry.link
    
        create_or_update_issue(title, content)


if __name__ == '__main__':
    rss_to_issue()
