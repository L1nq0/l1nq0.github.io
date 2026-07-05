# 后续开发计划

最后更新：2026-05-02

## 当前基线

- Hugo + FixIt 站点已完成 Hexo 迁移、基础样式、About/Links、导航、SEO 基础配置和 Fuse 搜索上线。
- `python check_images.py` 已验证 31 篇文章图片引用正常。
- `hugo --cleanDestinationDir` 已验证可构建，当前输出不含 `posts_backup` / `localhost` 污染。
- 当前主线目标：先把站点做到稳定、可上线、可维护，再选择性增加交互功能。

## 总体原则

1. **先稳定后增强**：优先处理能影响上线质量的问题，评论、统计、PWA 等后置。
2. **少改主题源码**：优先改 `hugo.toml`、`assets/css/_custom.scss`、`layouts/` 覆盖文件。
3. **每步可验证**：每个阶段至少跑 `hugo --cleanDestinationDir` 和 `python check_images.py`。
4. **避免生成物污染内容源**：备份、临时文件、旧输出不得放进 `content/`。
5. **视觉保持克制**：继续保持简洁阅读体验，避免堆叠过多动画和第三方脚本。

## Phase 1：上线前验收

目标：确认当前站点可直接部署，不再有明显 SEO、搜索、资源或移动端问题。

### 任务

- 浏览器级搜索 smoke test：测试 `Editorial`、`反序列化`、`phpcms`。
- 检查首页、文章页、Tags、Categories、Archives、About、Links 的桌面和移动端布局。
- 检查 favicon、Apple touch icon、OG/Twitter 图片实际输出。
- 检查 RSS、sitemap、robots 输出是否符合生产域名。
- 明确 `public/` 策略：提交生成物，或由部署环境构建。

### 验收标准

- 搜索弹窗在桌面和移动端都可用。
- `public/search.json` 不包含备份目录、临时内容和 localhost。
- `public/sitemap.xml` / `public/robots.txt` 只使用 `https://sw1mblu3.fun/`。
- 移动端无明显横向滚动、导航遮挡或文章阅读问题。

## Phase 2：视觉与阅读体验收口

状态：按当前决策跳过，不作为近期执行项。

目标：在不破坏 FixIt 结构的前提下，把博客体验统一到简洁、可读、稳定。

### 任务

- 复核 `assets/css/_custom.scss`，清理重复或临时样式。
- 优化文章列表卡片：标题、日期、摘要、标签间距保持一致。
- 优化文章页正文宽度、代码块、表格、图片、TOC 的移动端表现。
- 复核 Links / About 页面语气与排版，保持英文为主，中文文章内容不改。
- 统一 hover、下划线、外链、社交图标视觉规则。

### 验收标准

- 首页、列表页、文章页视觉风格一致。
- 长代码块和宽表格在移动端可读，不破坏页面宽度。
- 样式改动集中在 `assets/css/_custom.scss` 或必要的覆盖文件。

## Phase 3：部署与仓库卫生

状态：当前采用方案 A，继续提交 `public/` 作为部署产物；`resources/` 作为 Hugo 生成缓存忽略。

目标：让项目后续维护成本降低，避免生成物、缓存和临时文件继续干扰状态判断。

### 任务

- 确定部署方式：
  - 方案 A：提交 `public/` 作为部署产物。（当前采用）
  - 方案 B：忽略 `public/`，由 CI / 部署环境执行 Hugo 构建。
- 基于部署方式完善 `.gitignore`。
- 清理或归档历史迁移脚本、阶段文档和旧计划文档。
- 增加固定验证命令说明，保证每次改动后有一致检查流程。

### 验收标准

- `git status --short` 能清晰区分源码改动和生成物改动。
- README 明确说明构建、预览、图片检查命令。
- 不再出现 `tmpclaude-*`、`.hugo_build.lock`、备份内容目录进入 Git 状态。

## Phase 4：可选交互功能

状态：开始执行。当前只启用阅读进度条；评论、Analytics、相关文章和 PWA 保持关闭，等部署稳定后再评估。

目标：只开启确实有价值且维护成本可控的功能。

### 候选项

- 评论系统：优先评估 Giscus，适合 GitHub 体系；不开启也可以。
- Analytics：优先选择轻量方案，避免过重的第三方脚本。
- 阅读进度条：低成本，但需要确认不破坏极简风格。
- 相关文章：当前关闭；如开启，需要确认标签质量和推荐准确性。
- PWA：后置，除非明确需要离线访问。

### 决策标准

- 不影响加载速度和阅读体验。
- 不显著增加隐私、维护或配置成本。
- 开启后有明确验证方式。

## Phase 5：性能与内容质量

目标：提升长期访问体验和内容可维护性。

### 任务

- 检查图片体积，优先处理超大 favicon / 头像 / 页面图片。
- 评估图片懒加载、压缩和现代格式策略。
- 做一次内部链接与外链检查。
- 检查文章 front matter 的 `summary`、`tags`、`categories` 一致性。
- 逐步补齐高价值文章摘要，提升搜索和列表阅读体验。

### 验收标准

- 关键页面资源体积可控。
- 图片引用检查稳定为 0 问题。
- 文章分类和标签没有明显重复、乱码或无效项。

## 推荐执行顺序

1. Phase 1：上线前验收。
2. Phase 3：部署与仓库卫生。
3. Phase 4：按需选择低风险交互功能。
4. Phase 5：性能与内容质量长期优化。

Phase 2 当前跳过，不进入近期执行顺序。

## 下一步执行项

建议下一次直接执行 Phase 1：

```bash
hugo server -D
python check_images.py
hugo --cleanDestinationDir
```

浏览器中重点检查：

- 搜索：`Editorial`、`反序列化`、`phpcms`
- 页面：首页、任意中文文章、任意英文文章、Tags、Archives、About、Links
- 输出：`/search.json`、`/sitemap.xml`、`/robots.txt`
