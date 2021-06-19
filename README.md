# Getting Started

爬虫学习。

第一期为零基础学习。代码已全移至 [phase_1](./phase_1) 下。
第二期为增强学习。代码请见 [phase_2](./phase_2)

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [第二期目录](#第二期目录)
- [第一期目录](#第一期目录)
- [Learn More](#learn-more)

<!-- /code_chunk_output -->

## 第二期目录

- [爬取豆瓣电影排行 top250 单页](./phase_2/douban_movie_single.py)
- [爬取豆瓣电影排行 top250 翻页](./phase_2/douban_movie_flip.py)
- [爬取斗图吧表情包推荐](./phase_2/doutuba_emoji.py)
- [爬取 PPT 模板](./phase_2/ppt_template.py)
- [小说下载器 (吞噬小说网)](./phase_2/novel_downloader.py)
- [动态页面爬取 - 分析法](./phase_2/dynamic_ajax_page.py)
- [动态页面爬取 - Selenium](./phase_2/dynamic_ajax_selenium.py)
- [模拟登陆 - 人为识别验证码](./phase_2/simulate_register.py)
- [爬取有声小说 (有声小说吧)](./phase_2/audio_novel.py)

---

## 第一期目录

- demo1 -- 爬取豆瓣电影 top250 单页
- demo2 -- 爬取豆瓣电影 top250 翻页
  - 分析 url 方式
  - 模拟点击下一页方式, 获取下一页 url
- demo3 -- 爬取斗图吧最新表情包推荐下载
  - 单张
  - 多张
- demo4 -- 小说下载器 (吞噬小说网)
  - 爬取小说名, 章节名, 单章内容
  - 小说下载器
- week1_test
  - 第一周爬虫学习周作业: 抓取 ppt 模板
- demo5 -- 动态页面爬取
  - 分析法
  - selenium
- demo6 -- 模拟登陆
  - 人工识别验证码
  - 第三方平台识别
  - pytesseract (OCR)
- demo7 -- 代理 IP 使用
  - 初体验
    - 获取本机 IP
    - 使用代理 IP
    - 使用 Selenium 发起使用代理 IP 的请求
  - 代理 IP 池
- week2_test
  - 第二周爬虫学习周作业: 模拟登陆
    - requests
    - selenium
- demo8 -- 异步爬虫
  - 同步方式
  - 多线程、线程池
    - 基础
    - 改写 demo8_1
  - 协程
    - 基础
    - 改写 demo8_1
- demo9 -- scrapy
  - 初见
  - 数据解析和分页抓取
  - 自动爬虫
  - 数据存储
    - 命令行 `scrapy crawl laosilaisi -o laosilaici.csv`
    - pipeline
    - 注意代码中对应位置需加上 `yield`!!!
- week3_test
  - 第三周爬虫学习周作业: 爬取京东无人机商品页
    - requests
    - selenium
- demo10 -- app 爬虫
  - fiddler + android 模拟器
- demo11 -- JS 逆向
  - 基础
  - 实战
- crypto_funcs -- 常见加密算法加解密
  - BASE64
  - 信息摘要算法
    - MD5
    - SHA1
    - SHA256
    - SHA512
  - 对称加密算法
    - AES
  - 非对称加密算法
    - RSA

## Learn More

:smile:个人学习所用，仅供参考。
