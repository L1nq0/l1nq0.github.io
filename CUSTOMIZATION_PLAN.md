# Hugo FixIt 博客定制化计划

## 当前状态（2026-05-01）

本文档保留原始路线图；当前准确状态请优先参考 [PROJECT_STATUS.md](./PROJECT_STATUS.md)。

- 已完成：Hexo 文章迁移、31 篇文章 page bundle 化、1,308 张图片引用检查、基础站点配置、主页 profile、About/Links 页面、导航、TagCloud、footer 品牌信息移除、链接样式优化。
- 已完成并验证：Fuse 搜索上线、Open Graph/Twitter Cards 基础图片、SEO author/publisher/app title、`public/robots.txt` 与 `public/sitemap.xml` 生产域名输出。
- 未启用或待决策：评论系统、Analytics、阅读进度条、PWA、CDN、图片性能优化、部署流水线。
- 构建注意：默认 Codex sandbox shell 中 `hugo` 不在 `PATH`，但授权使用非沙箱 PowerShell 后 `hugo` 构建通过；版本为 `v0.160.1+extended`。

## 📋 分析总结

### exp10it.io 博客设计特点

通过访问和分析，该博客使用 **Astro 框架**（非 Hugo），具有以下设计特点：

1. **极简主义风格**
   - 干净的排版，大量留白
   - 简洁的导航：Posts, Tags, Links, About
   - 纯文本为主，无过多装饰

2. **主页设计**
   - 大标题显示作者名（X1r0z）
   - 简短的个人简介（Web Security | X1cT34m | Nu1L Team）
   - Social Links 显著位置展示
   - Recent Posts 列表显示最新文章

3. **文章列表卡片**
   - 标题 + 日期 + 简短描述
   - 无特色图片，纯文本展示
   - 悬停效果：下划线装饰

4. **配色方案**
   - Light/Dark 模式切换
   - Accent color 用于链接和重点
   - 高对比度，易读性强

### FixIt 主题优势

- 功能更丰富（搜索、TOC、评论、分享等）
- SEO 优化更好
- 中文支持完善
- 可高度自定义

## 🎯 定制化步骤

### 第一阶段：完善基础配置和主页排版

#### 1.1 完善 hugo.toml 基础配置
- [x] 设置正确的 baseURL
- [x] 配置网站 description 和 keywords
- [x] 设置作者信息和头像
- [x] 配置社交链接
- [x] 启用必要的功能（RSS 已启用；搜索输出已配置但 UI 未启用）

#### 1.2 优化主页展示
- [x] 启用 profile 模式，展示个人信息
- [x] 配置主页 posts 列表显示数量
- [x] 设置 summary 显示方式
- [x] 优化文章卡片布局

#### 1.3 完善其他页面
- [x] 配置 Archives 页面
- [x] 设置 Categories 和 Tags 页面
- [x] 创建 About 页面
- [x] 添加 Links 友链页面

#### 1.4 SEO 优化
- [x] 配置 sitemap（`public/sitemap.xml` 已确认生产域名；根目录旧副本已清理）
- [x] 设置 robots.txt（`public/robots.txt` 已确认生产域名；根目录旧副本已清理）
- [x] 配置 Open Graph 和 Twitter Cards（基础图片使用 `/1.jpg`）
- [x] 添加网站图标 favicon（需视觉与标签复核）

### 第二阶段：进阶功能配置

#### 2.1 搜索功能
- [x] 启用 Fuse.js 搜索（当前 `params.search.enable = true`）
- [x] 配置搜索参数
- [ ] 测试搜索效果

#### 2.2 文章增强功能
- [x] 启用 TOC（目录）
- [x] 配置代码高亮
- [x] 启用数学公式支持（KaTeX）
- [ ] 配置图片处理/优化

#### 2.3 互动功能
- [ ] 配置评论系统（可选：Giscus/Waline）
- [x] 启用文章分享功能
- [ ] 添加阅读进度条
- [ ] 配置页面浏览统计

#### 2.4 性能优化
- [ ] 配置 CDN
- [ ] 优化图片加载
- [ ] 启用 PWA（可选）

### 第三阶段：深度定制（参考 exp10it.io 设计）

#### 3.1 自定义样式
创建 `assets/css/_custom.scss`：
- [ ] 自定义配色方案
- [ ] 调整字体和行距
- [ ] 优化卡片样式
- [ ] 自定义 hover 效果

#### 3.2 自定义模板
创建自定义模板覆盖：
- [ ] `layouts/summary.html` - 文章摘要卡片
- [ ] `layouts/partials/home/profile.html` - 主页个人信息
- [ ] `layouts/partials/header.html` - 页头
- [ ] `layouts/_default/section.html` - 分类/标签页

#### 3.3 自定义组件
- [ ] 创建简洁的文章列表样式
- [ ] 自定义导航栏
- [ ] 优化 footer
- [ ] 添加自定义 shortcodes

#### 3.4 响应式优化
- [ ] 移动端适配
- [ ] 平板端适配
- [ ] 触摸交互优化

## 📚 参考资源

### 官方文档
- [FixIt 主题文档](https://fixit.lruihao.cn/)
- [Advanced Usage](https://fixit.lruihao.cn/documentation/advanced)
- [Configure FixIt](https://fixit.lruihao.cn/documentation/getting-started/configuration/)
- [Content Management](https://fixit.lruihao.cn/documentation/content-management/introduction/)

### 设计参考
- [exp10it.io](https://exp10it.io/) - 极简主义风格
- [FixIt Demo](https://demo.fixit.lruihao.cn/) - 官方示例
- [Hugo Themes Showcase](https://themes.gohugo.io/)

### 技术文档
- [Hugo 官方文档](https://gohugo.io/documentation/)
- [Hugo Page Resources](https://gohugo.io/content-management/page-resources/)
- [Hugo Templates](https://gohugo.io/templates/)

## 🚀 实施建议

1. **循序渐进**：先完成基础配置，再进行深度定制
2. **备份优先**：修改前备份配置和文件
3. **测试验证**：每次修改后测试效果
4. **文档记录**：记录自定义的内容，方便后续维护
5. **版本控制**：使用 Git 管理配置变更

## 📝 注意事项

1. **主题升级**：深度定制可能影响主题升级，建议：
   - 使用 `_override.scss` 而非直接修改主题文件
   - 使用 `layouts/` 目录覆盖而非修改主题模板
   - 记录所有自定义内容

2. **性能考虑**：
   - 避免过多 JavaScript
   - 优化图片大小
   - 合理使用缓存

3. **兼容性**：
   - 测试不同浏览器
   - 确保移动端体验
   - 检查 RSS 输出

## ✅ 完成标准

- [x] 主页美观，信息展示完整
- [x] 文章列表清晰易读
- [ ] 搜索功能正常工作
- [ ] 移动端体验良好（需重新视觉验证）
- [x] SEO 基础文件验证（robots/sitemap 已使用生产域名）
- [x] SEO 搜索污染清理（`content/posts_backup_20260428_111421` 已移出内容源）
- [ ] 性能达标（PageSpeed > 90）
- [ ] 所有链接正常（需运行链接检查）
- [ ] RSS 正常输出
