#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查所有文章的图片引用是否正确
"""

import os
import re
from pathlib import Path

POSTS_DIR = r"F:\Tools\CyberSec_Tools\program\Blog\hugo\my-blog\content\posts"

def extract_image_refs(content):
    """提取 Markdown 中的图片引用"""
    # 匹配 ![alt](path) 和 ![](path) 格式
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)
    return [match[1] for match in matches]

def check_post_images(post_dir):
    """检查单篇文章的图片"""
    index_file = os.path.join(post_dir, 'index.md')

    if not os.path.exists(index_file):
        return None

    # 读取文章内容
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取图片引用
    image_refs = extract_image_refs(content)

    if not image_refs:
        return None

    # 获取实际存在的图片文件
    actual_images = []
    for file in os.listdir(post_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            actual_images.append(file)

    # 检查每个引用的图片是否存在
    missing_images = []
    broken_refs = []

    for ref in image_refs:
        # 清理路径
        ref = ref.strip()

        # 跳过外部链接
        if ref.startswith('http://') or ref.startswith('https://'):
            continue

        # 检查是否包含路径分隔符（说明路径没有正确转换）
        if '/' in ref or '\\' in ref:
            broken_refs.append(ref)
            continue

        # 检查文件是否存在
        if ref not in actual_images:
            missing_images.append(ref)

    post_name = os.path.basename(post_dir)

    result = {
        'post': post_name,
        'total_refs': len(image_refs),
        'actual_images': len(actual_images),
        'missing': missing_images,
        'broken_refs': broken_refs,
        'has_issues': len(missing_images) > 0 or len(broken_refs) > 0
    }

    return result

def main():
    """主函数"""
    print("=== Checking Images in All Posts ===\n")

    issues_found = []
    total_posts = 0
    posts_with_images = 0

    # 遍历所有文章目录
    for post_name in sorted(os.listdir(POSTS_DIR)):
        post_dir = os.path.join(POSTS_DIR, post_name)

        if not os.path.isdir(post_dir):
            continue

        total_posts += 1
        result = check_post_images(post_dir)

        if result is None:
            continue

        posts_with_images += 1

        if result['has_issues']:
            issues_found.append(result)
            print(f"[ISSUE] {result['post']}")
            print(f"  Total refs: {result['total_refs']}")
            print(f"  Actual files: {result['actual_images']}")

            if result['broken_refs']:
                print(f"  Broken refs ({len(result['broken_refs'])}):")
                for ref in result['broken_refs'][:5]:  # 只显示前5个
                    print(f"    - {ref}")
                if len(result['broken_refs']) > 5:
                    print(f"    ... and {len(result['broken_refs']) - 5} more")

            if result['missing']:
                print(f"  Missing images ({len(result['missing'])}):")
                for img in result['missing'][:5]:  # 只显示前5个
                    print(f"    - {img}")
                if len(result['missing']) > 5:
                    print(f"    ... and {len(result['missing']) - 5} more")
            print()

    print("\n=== Summary ===")
    print(f"Total posts: {total_posts}")
    print(f"Posts with images: {posts_with_images}")
    print(f"Posts with issues: {len(issues_found)}")

    if issues_found:
        print("\nPosts needing attention:")
        for result in issues_found:
            print(f"  - {result['post']}")

if __name__ == '__main__':
    main()
