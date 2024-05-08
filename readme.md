
<img width="50%" style="border: 1px solid black" src="https://i.imgur.com/azBO1qu.png">

# FGO每日自动登录

🤓这么多年来…就目前来说有那么亿点点封号风险(^_-)-☆

⚠️注意事项
 - 2024年5月7日起 连接绑定 Aniplex Online 后的游戏账号文件 可能无法使用



该修改版项目源及原作者

- [hexstr](https://github.com/hexstr) 

- [FGODailyBonus](https://github.com/hexstr/FGODailyBonus)


它具有以下特点：
- 不会产生日志
- 全自动游戏版本更新同步
- 向你的Discord频道发送登录结果等信息
- 只支持 JP 版本游戏(日服)😛


# 提取您的 游戏账号数据
您需要提取账号数据才能执行此操作。
很简单，您所需要做的就是用文件管理器到以下路径并获取以下文件（可能需要ROOT）： 

| 版本 | 文件路径 | 文件名称 |
| --- | --- | --- | 
| JP | `android/data/com.aniplex.fategrandorder/files/data/` | 54cc790bf952ea710ed7e8be08049531 |

# 解密您的游戏账号数据

请小心处理这些数据，您不应将此数据传递给其他人，这是直接与服务器通信的关键数据，能直接盗你的号！

1. 下载 FGO-ADET ，查看解密方法, 并解密文件! [FGO-ADET](https://github.com/DNNDHH/FGO-ADET)
2. 获取您设备（手机或模拟器）的用户代理:
    1. 使用 ADB 連接到你的手機
    2. 輸入 `adb shell getprop ro.build.version.release` 取得自己手機的 `{Release build}`
    3. 輸入 `adb shell getprop ro.product.model` 取得自己手機的 `{Model}`
    4. 輸入 `adb shell getprop ro.build.id` 取得自己手機的 `{Id}`
    5. 輸入 `adb shell getprop ro.product.manufacturer` 取得自己手機的 `{Manufacturer}`
    6. 輸入 `adb shell getprop ro.build.version.sdk` 取得自己手機的 `{API level}`
    7. 輸入 `adb shell getprop ro.build.version.incremental` 取得自己手機的 `{Incremental}`
    8. 將 1 ~ 6 步驟取得的值依照下列大括號中的名稱進行替換(如不清楚如何替換可以參考[下面的範例](https://github.com/Zhen-Bo/F-D-L/blob/master/readme.md#%E5%A1%AB%E5%86%99-%E6%B8%B8%E6%88%8F%E8%B4%A6%E5%8F%B7%E5%AF%86%E9%92%A5%E5%92%8Cpost%E9%85%8D%E7%BD%AE))
        1. USER_AGENT_SECRET_2 = `Dalvik/2.1.0 (Linux; U; Android {Release build}; {Model} Build/{Id})`
        2. DEVICE_INFO_SECRET = `{Manufacturer} {Model} / Android OS {Release build} / API-{API level} ({Id}/{Incremental})`

# 创建 Discord 消息通知机器人
要创建 webhook Discord，您需要在 Discord 中创建一个服务器 并在该频道的 设置中 创建一个 文本频道
`integration > webhook > create webhook > copy url webhook`

# 执行定时签到任务/定时登录

定时登录 FGO的时间 [世界时](https://time.is/zh/compare/utc/Beijing) 

| 版本 | 自动登录时间   |
|--------|-------------|
| JP     | 30 19 * * * |


🫠 代码格式 30 19 * * * 是指 UTC时间 19：30 = 天朝时间 凌晨3点半 ，参考 [世界时](https://time.is/zh/compare/utc/Beijing) 

修改 自动流程 [这里](https://github.com/DNNDHH/F-D-L/blob/master/.github/workflows/run.yml) 的代码 自定义 自动登录时间
 ```console
  schedule:
    - cron: "00 03 * * *"
    - cron: "30 03 * * *"
    - cron: "30 13 * * *"
    - cron: "30 17 * * *"
  ```  


# 填写 游戏账号密钥和POST配置
将下列 密钥类型 和 账号密钥 添加到 `右上角 > settings > Secrets and variables > actions`
<img width="75%" style="border: 1px solid black" src="https://i.imgur.com/J7jb6TX.png">

需要登录多个账号时使用 英文逗号
 ```console
,
  ```
隔开！ 注意填写 账号密钥 时 顺序相同 ！

| 密钥类型 | 账号密钥 样本 |
| --- | --- |
| GAME_AUTHKEYS | RaNdOmStRiNg1234:randomAAAAA=,RaNdOmStRiNg1235:randomAAAAA= |
| GAME_SECRETKEYS | RaNdOmStRiNg1234:randomAAAAA=,RaNdOmStRiNg1235:randomAAAAA= |
| GAME_USERIDS | 1234,1235 |
| GAME_REGION | JP |
| USER_AGENT_SECRET_2 | Dalvik/2.1.0 (Linux; U; Android 14; Pixel 5 Build/UP1A.231105.001) 建议不要照抄 |
| IDEMPOTENCY_KEY_SIGNATURE_SECRET |  https://fgo.xiaoheimao.workers.dev/getSignature?    https://worker.chaldea.center/api/v4/tool/sign-data  选择一个|
| DEVICE_INFO_SECRET | Google Pixel 5 / Android OS 14 / API-34 (UP1A.231105.001/10817346) 建议不要照抄 |
| DISCORD_WEBHOOK | https://discord.com/api/webhooks/randomNumber/randomString |

# 已完成 
- [x] 自动每日友情点召唤
- [x] 自动种蓝苹果🍎
- [x] 自动领取礼物盒

# 未来计划 （咕咕咕🤣）
- [ ] ....想要什么功能。。你来说。。

# 感谢
- [hexstr](https://github.com/hexstr) 

