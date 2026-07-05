#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hexo to Hugo FixIt Migration Script
从 Hexo 博客迁移文章到 Hugo FixIt 主题
"""

import os
import re
import shutil
from pathlib import Path

# 配置
SOURCE_DIR = r"F:\Tools\CyberSec_Tools\program\Blog\blog-demo\source\_posts"
TARGET_DIR = r"F:\Tools\CyberSec_Tools\program\Blog\hugo\my-blog\content\posts"

def create_slug(filename):
    """将文件名转换为 URL 友好的 slug"""
    # 移除 .md 扩展名
    basename = os.path.splitext(filename)[0]

    # 移除开头的数字
    basename = re.sub(r'^[0-9]+', '', basename)

    # 转换为小写并替换特殊字符
    slug = basename.lower()
    slug = re.sub(r'[^a-z0-9\u4e00-\u9fa5_-]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)  # 合并多个连字符
    slug = slug.strip('-')  # 移除首尾连字符

    # 如果 slug 为空，使用原始文件名
    if not slug:
        slug = basename.lower().replace(' ', '-')

    return slug

def convert_front_matter(content, slug):
    """转换 Hexo front matter 到 Hugo FixIt 格式"""
    # 提取 front matter 和正文
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not fm_match:
        print(f"    Warning: No front matter found")
        return content

    front_matter = fm_match.group(1)
    body = fm_match.group(2)

    # 转换 tags 格式：['tag1', 'tag2'] -> YAML 列表格式
    tags_match = re.search(r"tags:\s*\[([^\]]+)\]", front_matter)
    if tags_match:
        tags_str = tags_match.group(1)
        # 提取标签（处理单引号和双引号）
        tags = [t.strip().strip("'\"") for t in tags_str.split(',')]
        tags_yaml = '\n  - '.join(tags)
        front_matter = re.sub(r"tags:.*", f"tags:\n  - {tags_yaml}", front_matter)

    # 转换 excerpt 为 summary
    front_matter = re.sub(r'excerpt:', 'summary:', front_matter)

    # 添加 Hugo FixIt 必需字段
    if 'slug:' not in front_matter:
        front_matter += f"\nslug: {slug}"

    if 'draft:' not in front_matter:
        front_matter += "\ndraft: false"

    if 'author:' not in front_matter:
        front_matter += "\nauthor:\n  name: L1nq\n  link:\n  email:\n  avatar:"

    if 'comment:' not in front_matter:
        front_matter += "\ncomment: false"

    if 'weight:' not in front_matter:
        front_matter += "\nweight: 0"

    # 添加 FixIt 主题隐藏配置
    if 'hiddenFromHomePage:' not in front_matter:
        front_matter += "\nhiddenFromHomePage: false"

    if 'hiddenFromSearch:' not in front_matter:
        front_matter += "\nhiddenFromSearch: false"

    if 'hiddenFromRelated:' not in front_matter:
        front_matter += "\nhiddenFromRelated: false"

    if 'hiddenFromFeed:' not in front_matter:
        front_matter += "\nhiddenFromFeed: false"

    # 重新组装内容
    new_content = f"---\n{front_matter}\n---\n{body}"

    return new_content

def fix_image_paths(content, folder_name):
    """修正图片路径，将 folder/image.png 改为 image.png"""
    # 匹配 ![alt](folder/image.ext) 格式
    pattern = rf'\((\s*){re.escape(folder_name)}/([^)]+)\)'
    replacement = r'(\2)'

    new_content = re.sub(pattern, replacement, content)

    return new_content

def migrate_post(md_file):
    """迁移单篇文章"""
    filename = os.path.basename(md_file)
    basename = os.path.splitext(filename)[0]

    # 生成 slug
    slug = create_slug(filename)

    print(f"Processing: {basename}")
    print(f"  -> Slug: {slug}")

    # 创建目标目录
    target_post_dir = os.path.join(TARGET_DIR, slug)
    os.makedirs(target_post_dir, exist_ok=True)

    # 读取原始 markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查同名图片文件夹
    image_folder = os.path.join(SOURCE_DIR, basename)
    if os.path.isdir(image_folder):
        print(f"  -> Copying images from {basename}/")

        # 复制所有图片文件
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp']
        for img_file in os.listdir(image_folder):
            if any(img_file.lower().endswith(ext) for ext in image_extensions):
                src = os.path.join(image_folder, img_file)
                dst = os.path.join(target_post_dir, img_file)
                shutil.copy2(src, dst)

        # 修正图片路径
        content = fix_image_paths(content, basename)
        print(f"  -> Fixed image paths")

    # 转换 front matter
    content = convert_front_matter(content, slug)
    print(f"  -> Converted front matter")

    # 写入 index.md
    index_file = os.path.join(target_post_dir, 'index.md')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] Done\n")
    return True

def main():
    """主函数"""
    print("=== Hexo to Hugo FixIt Migration Script ===")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print()

    # 确保目标目录存在
    os.makedirs(TARGET_DIR, exist_ok=True)

    # 查找所有 .md 文件
    md_files = [
        os.path.join(SOURCE_DIR, f)
        for f in os.listdir(SOURCE_DIR)
        if f.endswith('.md') and os.path.isfile(os.path.join(SOURCE_DIR, f))
    ]

    total = len(md_files)
    success = 0
    errors = 0

    print(f"Found {total} markdown files\n")

    for md_file in sorted(md_files):
        try:
            if migrate_post(md_file):
                success += 1
        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}\n")
            errors += 1

    print("\n=== Migration Complete ===")
    print(f"Total: {total}")
    print(f"Success: {success}")
    print(f"Errors: {errors}")

if __name__ == '__main__':
    main()
