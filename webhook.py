import main
import requests
import user
import json


def topLogin(data: list) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]
    with open('login.json', 'r', encoding='utf-8')as f:
        data22 = json.load(f)

        name1 = data22['cache']['replaced']['userGame'][0]['name']
        fpids1 = data22['cache']['replaced']['userGame'][0]['friendCode']
    
    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name != None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO登录系统 - " + main.fate_region,
                "description": f"登录成功。列出角色信息.\n\n{messageBonus}",
                "color": 563455,
                "fields": [
                    {
                        "name": "御主名",
                        "value": f"{name1}",
                        "inline": True
                    },
                    {
                        "name": "朋友ID",
                        "value": f"{fpids1}",
                        "inline": True
                    },
                    {
                        "name": "等级",
                        "value": f"{rewards.level}",
                        "inline": True
                    },
                    {
                        "name": "呼符", 
                        "value": f"{rewards.ticket}",
                        "inline": True
                    },                    
                    {
                        "name": "圣晶石",
                        "value": f"{rewards.stone}",
                        "inline": True
                    },
                    {
                        "name": "圣晶片",
                        "value": f"{rewards.sqf01}",
                        "inline": True
                    },
                    {
                        "name": "金苹果",
                        "value": f"{rewards.goldenfruit}",
                        "inline": True
                    },
                    {
                        "name": "银苹果",
                        "value": f"{rewards.silverfruit}",
                        "inline": True
                    },
                    {
                        "name": "铜苹果",
                        "value": f"{rewards.bronzefruit}",
                        "inline": True
                    },
                    {
                        "name": "蓝苹果",
                        "value": f"{rewards.bluebronzefruit}",
                        "inline": True
                    },
                    {
                        "name": "蓝苹果树苗",
                        "value": f"{rewards.bluebronzesapling}",
                        "inline": True
                    },
                    {
                        "name": "连续登录天数",
                        "value": f"{login.login_days}",
                        "inline": True
                    },
                    {
                        "name": "累计登录天数",
                        "value": f"{login.total_days}",
                        "inline": True
                    },
                    {
                        "name": "白方块",
                        "value": f"{rewards.pureprism}",
                        "inline": True
                    },
                    {
                        "name": "友情点",
                        "value": f"{login.total_fp}",
                        "inline": True
                    },
                    {
                        "name": "今天 获得的友情点",
                        "value": f"+{login.add_fp}",
                        "inline": True
                    },
                    {
                        "name": "当前AP",
                        "value": f"{login.remaining_ap}",
                        "inline": True
                    },
                    {
                        "name": "圣杯",
                        "value": f"{rewards.holygrail}",
                        "inline": True
                    },
                    
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara01.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def shop(item: str, quantity: str) -> None:
    endpoint = main.webhook_discord_url
    
    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO自动购物系统 - " + main.fate_region,
                "description": f"购买成功.",
                "color": 5814783,
                "fields": [
                    {
                        "name": f"商店",
                        "value": f"消费 {40 * quantity}Ap 购买 {quantity}x {item}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo2/images/commnet_chara10.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def drawFP(servants, missions) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""
    
    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            svt = svt_dict[servant.objectId]
            message_servant += f"`{svt['name']}` "

    if(len(missions) > 0):
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO自动抽卡系统 - " + main.fate_region,
                "description": f"完成当日免费友情抽卡。列出抽卡结果.\n\n{message_mission}",
                "color": 5750876,
                "fields": [
                    {
                        "name": "友情卡池",
                        "value": f"{message_servant}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara02_rv.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)
