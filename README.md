# About The Project

爬取`yande.re`网站上的所有图片  
下载给定页数区间的图片，已经下载的会自动跳过  
下载速度应该是很快的，破校园网，53 代理破解再加 clash 代理可以跑到差不多 50Mbs  
下载后看看下面的[提示](#提示)，还有`config.ini`根据自身需求修改

## 环境要求

python >=3.8
python lib: requests

## Getting start

### 下载项目

```sh
git clone https://github.com/oldshensheep/crawl-yande.re.git
```

或者下载 zip 解压

### 运行前配置

安装依赖 requests，这个应该都安装了。

```sh
pip3 install requests
```
配置文件是一个python文件，程序启动时会运行它。  
打开 `config.py` 按照文件里的提示配置, 国内要配置代理，支持 http 代理，不填用系统代理设置  
如果打开了 clash，v2ray 等代理软件，并且开启系统代理应该不用填代理设置  
这里列出了配置文件文件内容

```python
# 下载起始页 默认 1
start_page = 1

# 下载结束页 默认 100
end_page = 100

# 同时下载的线程数 默认 8
max_workers = 8

# 图片保存路径 默认为 yande.re, 不存在自动创建
filepath = "yande.re"

# http代理 不填默认没有代理/系统代理
proxy = None

# 云函数代理 默认无代理 CloudFlare Workers 代理，不需要爬墙代理啦，每天10W次请求(UTC+0)
# 部分地区/宽带 用这个可能还是下载不了或者很慢，建议使用http代理。
# "https://http-proxy.oldshensheep.workers.dev"
hproxy = None

# 连接错误重试次数 默认 2
max_retries = 2

# 连接超时 默认 4 出现Read timed out可尝试增大此值
timeout = 5

# 画质 'original jpeg sample 画质由好到差
quality = "jpeg"

```

### 运行

```sh
python3 run.py
```

## 提示

- 下载的文件会根据画质选项分类
- 如果全部下载建议选择 `sample` 画质（空间多当我没说），`original` 画质平均文件大小在 3.5MB  
~~测试~~ **的时候不知不觉下载了 4000 多张差不多占了 17GB 的空间……**  
- 如果你看到了似乎是一样的图片，那不是重复下载了，或者 yande.re 有重复的图片。（你应该小心的放大图片对比看看有什么不同(*/ω＼*)）

## TODO

1. ~~添加下载画质的选项~~
2. 用数据库存储 id 的 tag 等信息，方便查询
3. 添加按 tag 下载的功能
4. ~~支持云函数代理 https://xxxxx.workers.dev/https://yande.re/post.json 用云函数代理，这样就可以省点流量了……(~~
5. ~~存储 log，更友好的爬取详细输出~~
6. 完善注释？
7. 并行化请求图片 url 的过程
8. add more todo

## License

[MIT License](https://github.com/oldshensheep/crawl-yande.re/blob/main/LICENSE)
