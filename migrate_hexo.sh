#!/bin/bash

# Hexo to Hugo FixIt Migration Script
# 从 Hexo 博客迁移文章到 Hugo FixIt 主题

SOURCE_DIR="F:/Tools/CyberSec_Tools/program/Blog/blog-demo/source/_posts"
TARGET_DIR="content/posts"

echo "=== Hexo to Hugo FixIt Migration Script ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# 统计信息
total_files=0
success_count=0
error_count=0

# 查找所有 .md 文件
find "$SOURCE_DIR" -maxdepth 1 -type f -name "*.md" | while read -r md_file; do
    total_files=$((total_files + 1))

    # 获取文件名（不含路径和扩展名）
    basename=$(basename "$md_file" .md)

    # 创建 slug（URL友好的目录名）
    # 移除开头的数字和特殊字符，转换为小写
    slug=$(echo "$basename" | sed 's/^[0-9]*//g' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9\u4e00-\u9fa5_-]/-/g' | sed 's/--*/-/g' | sed 's/^-//g' | sed 's/-$//g')

    # 如果 slug 为空，使用原始文件名
    if [ -z "$slug" ]; then
        slug=$(echo "$basename" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]/-/g')
    fi

    echo "Processing: $basename -> $slug"

    # 创建目标目录
    target_post_dir="$TARGET_DIR/$slug"
    mkdir -p "$target_post_dir"

    # 复制 markdown 文件并重命名为 index.md
    cp "$md_file" "$target_post_dir/index.md"

    # 检查是否存在同名图片文件夹
    image_dir="$SOURCE_DIR/$basename"
    if [ -d "$image_dir" ]; then
        echo "  -> Copying images from $basename/"
        # 复制所有图片文件
        find "$image_dir" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" \) -exec cp {} "$target_post_dir/" \;

        # 修改 index.md 中的图片路径
        # 将 ![alt](文件夹名/图片.png) 替换为 ![alt](图片.png)
        sed -i "s|(\s*$basename/|\(|g" "$target_post_dir/index.md"

        echo "  -> Updated image paths"
    fi

    # 转换 front matter (Hexo -> Hugo)
    # 添加 Hugo FixIt 需要的字段
    python3 - << 'EOF' "$target_post_dir/index.md" "$slug"
import sys
import re

file_path = sys.argv[1]
slug = sys.argv[2]

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 front matter
fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
if fm_match:
    front_matter = fm_match.group(1)
    body = fm_match.group(2)

    # 转换 tags 格式：['tag1', 'tag2'] -> - tag1
    tags_match = re.search(r"tags:\s*\['?([^'\]]+)'?\]", front_matter)
    if tags_match:
        tags = [t.strip().strip("'\"") for t in tags_match.group(1).split(',')]
        tags_yaml = '\n  - '.join(tags)
        front_matter = re.sub(r"tags:.*", f"tags:\n  - {tags_yaml}", front_matter)

    # 添加 Hugo FixIt 特定字段
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

    # 转换 excerpt 为 summary
    front_matter = re.sub(r'excerpt:', 'summary:', front_matter)

    # 添加隐藏字段
    if 'hiddenFromHomePage:' not in front_matter:
        front_matter += "\nhiddenFromHomePage: false"
    if 'hiddenFromSearch:' not in front_matter:
        front_matter += "\nhiddenFromSearch: false"
    if 'hiddenFromRelated:' not in front_matter:
        front_matter += "\nhiddenFromRelated: false"
    if 'hiddenFromFeed:' not in front_matter:
        front_matter += "\nhiddenFromFeed: false"

    # 重构内容
    new_content = f"---\n{front_matter}\n---\n{body}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  -> Converted front matter")
else:
    print(f"  -> Warning: No front matter found")
EOF

    echo "  ✓ Done"
    echo ""
    success_count=$((success_count + 1))
done

echo ""
echo "=== Migration Complete ==="
echo "Total processed: $total_files"
echo "Success: $success_count"
echo "Errors: $error_count"
