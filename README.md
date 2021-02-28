# About The Project

爬取`yande.re`网站上的所有图片  
下载给定页数区间的图片，已经下载的会自动跳过

## 环境要求

python >=3.8 (用了:=)
python lib: requests

## Getting start

### 下载项目

```sh
git clone https://github.com/oldshensheep/YandeReSpider.git
```

或者下载 zip 解压

### 运行前配置

安装依赖 requests，这个应该都安装了

```sh
pip3 install requests
```

打开 `config.ini` 按照文件里的提示配置, 国内要配置代理，支持 http 代理，不填用系统代理设置
这里列出了文件内容

```ini
;自定义配置

; 下载起始页 默认 1
start_page = 1

; 下载结束页 默认 100
end_page = 100

; 同时下载的线程数 默认10个线程
max_workers = 10

; 图片保存路径 默认为 yande.re, 不存在自动创建
filepath = /mnt/d/Codespaces/Code/.io/yande.re

; http代理 默认没有代理/系统代理
proxy = http://localhost:7890

; 连接错误重试次数 默认 2
max_retries = 2

; 连接超时 默认 4
timeout = 5

; 画质 'original jpeg sample 画质由好到差
quality = original
```

### 运行

```sh
python3 run.py
```

## 提示

- 下载的文件会根据画质选项分类
- 如果全部下载建议选择 `sample` 画质（空间多当我没说），`original` 画质平均文件大小在 3.5MB  
  ~~测试~~ **的时候不知不觉下载了 4000 多张差不多占了 17GB 的空间……**

## TODO

1. 添加下载画质的选项
2. 用数据库存储 id 的 tag 等信息，方便查询
3. add more todo
