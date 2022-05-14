# 下载起始页 默认 1
start_page = 1

# 下载结束页 默认 100
end_page = 100

# 同时下载的线程数 默认 8
max_workers = 8

# 图片保存路径 默认为 yande.re, 不存在自动创建
filepath = "yande.re"

# http代理 不填默认没有代理/系统代理
# "http://localhost:7890"
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
