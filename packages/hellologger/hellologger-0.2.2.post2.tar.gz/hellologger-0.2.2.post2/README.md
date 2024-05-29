# HelloLogger

Push your log to everywhere!

-----

PyPi: https://pypi.org/project/hellologger/

## 简介

HelloLogger是一个基于Loguru的同时向多个来源投送日志的日志框架，便于快速配置和接入Aliyun、AWS等SaaS；快速投递到ClickHouse、ElasticSearch、GreptimeDB、MongoDB等时序数据库或文档数据库；快速投递到Syslog或调用WebHook

希望这个日志库能帮助您解决复杂项目中留痕和云观测的难题。

## 数据驱动

### `file_local` (**`local`**)

可用的日志源：

* loguru

可用的数据驱动：

* loguru.default

可配置项：

* batch_time: 如果使用loguru，可以设定是否按照时间或者大小分批
* batch_size: 如果使用loguru，可以设定是否按照时间或者大小分批

### `file_s3` (**`s3`**)

**WIP**

其实就是本地文件一样的逻辑，只不过考虑不要落盘，全部在内存中进行。需要有好的S3驱动。

### `saas_aliyun_sls` (**`aliyun`**)

可用的日志源：

* loguru

可用的数据驱动：

* aliyun-restful-api (WIP)
* aliyun-log-python-sdk

#### 配置指南（aliyun-restful-api）

暂无，可参考官方文档手搓HTTP请求：https://help.aliyun.com/zh/sls/developer-reference/api-postlogstorelogs

#### 配置指南（aliyun-log-python-sdk）

该数据驱动依赖[aliyun/aliyun-log-python-sdk](https://github.com/aliyun/aliyun-log-python-sdk)项目，您需要提前安装对应package：

```bash
pip install aliyun-log-python-sdk
```

您需要配置2个本地环境变量：

* `ALIYUN_ACCESSKEY_ID`
* `ALIYUN_ACCESSKEY_SECRET`

需要注意的有：

1. 环境变量设置后请重启
2. 请确保您提供的AccessKey具有SLS的写权限。您可以在RAM中进行权限管理。
3. 即使开通了SLS服务，并创建了一个项目，创建了一个logstore，也必须手动在logstor管理界面进行一次“数据接入”操作，才算实质性开通，否则不允许从python-sdk上传日志。

警告：**该数据驱动依赖的包protobuf锁定在较为久远的版本，易与本地其他包依赖的protobuf冲突。建议如果必须采用，可使用如`pip install protobuf==3.20.3`来强制指定版本。**

### `saas_aws_cloudwatch` (**`aws`**)

**WIP**

似乎CloudWatch必须有本地客户端才能打日志，没法直接RESTful API调用。

### `db_clickhouse` (**`clickhouse`**)

**WIP**

### `db_elasticsearch` (**`elasticsearch`**)

**WIP**

计划依赖 https://pypi.org/project/elasticsearch-logging-handler/

### `protocal_syslog` (**`syslog`**)

**WIP**

详见 https://docs.render.com/log-streams#sumo-logic

### `protocal_webhook` (**`webhook`**)

**WIP**

计划支持包括但不仅限于如下平台的WebHook模板：
* Discord (官方文档：[配置](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)、[参数](https://discord.com/developers/docs/resources/webhook))
* Slack
* Telegram (官方文档：[botfather](https://core.telegram.org/bots)、[例程](https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py))

其中，Discord平台计划提供两个数据驱动，一个依赖loguru-discord，一个仍调用restful api

WebHook需要传入配置文件，以适配不同平台。如果没有指定，就默认Discord的。

## 日志源和未来架构愿景

目前仅有一个日志源loguru

提供的logger是loguru的logger，直接暴露，没有重新封装

在未来可能会封装出一个专门的logger，如：

```python
hellologger.log(level:str,message:str,device:str)
```

并可指定logging或者loguru来完成任务，避免有部分平台loguru就是打不上去的也能用本项目打上去。

引用hellologger从此一身轻！

## 杂谈

Q：为什么要叫这个名字？

A：因为当时想了很多，包括什么logcat、magiclog等。然后在路过的招牌的塑料袋上看到一个hello，干脆就叫hellologger了，因为无论如何都要体现出log嘛。之后就去搜有没有撞车知名项目，然后只发现了[soongoo/HelloLogger](https://github.com/soongoo/HelloLogger)和[larse514/HelloLogger](https://github.com/larse514/HelloLogger)两个项目，都已经看起来停止维护了，就开工了！

