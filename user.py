# coding: utf-8
import msgpack
import uuid
import hashlib
import base64
import fgourl
import mytime
import gacha
import webhook
import main
import logging
import json
import os
import subprocess
import re
import sys
import binascii
import random
import time
import requests
import shutil



from urllib.parse import quote_plus
from libs.GetSubGachaId import GetGachaSubIdFP
from fake_useragent import UserAgent

class ParameterBuilder:
    def __init__(self, uid: str, auth_key: str, secret_key: str):
        self.uid_ = uid
        self.auth_key_ = auth_key
        self.secret_key_ = secret_key
        self.content_ = ''
        self.idempotency_key_ = str(uuid.uuid4()) 
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', self.idempotency_key_), 
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]

    def get_idempotency_key(self):
        return self.idempotency_key_

    def AddParameter(self, key: str, value: str):
        self.parameter_list_.append((key, value))
        

    def Build(self) -> str:
        self.parameter_list_.sort(key=lambda tup: tup[0])
        temp = ''
        for first, second in self.parameter_list_:
            if temp:
                temp += '&'
                self.content_ += '&'
            escaped_key = quote_plus(first)
            if not second:
                temp += first + '='
                self.content_ += escaped_key + '='
            else:
                escaped_value = quote_plus(second)
                temp += first + '=' + second
                self.content_ += escaped_key + '=' + escaped_value

        temp += ':' + self.secret_key_
        self.content_ += '&authCode=' + \
            quote_plus(base64.b64encode(
                hashlib.sha1(temp.encode('utf-8')).digest()))

        return self.content_

    def Clean(self):
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]


class Rewards:
    def __init__(self, stone, level, ticket, goldenfruit, silverfruit, bronzefruit, bluebronzesapling, bluebronzefruit, pureprism, sqf01, holygrail):
        self.stone = stone
        self.level = level
        self.ticket = ticket
        self.goldenfruit = goldenfruit
        self.silverfruit = silverfruit
        self.bronzefruit = bronzefruit
        self.bluebronzesapling = bluebronzesapling
        self.bluebronzefruit = bluebronzefruit
        self.pureprism = pureprism
        self.sqf01 = sqf01
        self.holygrail = holygrail


class Login:
    def __init__(self, name, login_days, total_days, act_max, act_recover_at, now_act, add_fp, total_fp, name1, fpids1, remaining_ap):
        self.name = name
        self.login_days = login_days
        self.total_days = total_days
        self.act_max = act_max
        self.act_recover_at = act_recover_at
        self.now_act = now_act
        self.add_fp = add_fp
        self.total_fp = total_fp
        self.name1 = name1
        self.fpids1 = fpids1
        self.remaining_ap = remaining_ap



class Bonus:
    def __init__(self, message, items, bonus_name, bonus_detail, bonus_camp_items):
        self.message = message
        self.items = items
        self.bonus_name = bonus_name
        self.bonus_detail = bonus_detail
        self.bonus_camp_items = bonus_camp_items


class user:
    def __init__(self, user_id: str, auth_key: str, secret_key: str):
        self.name_ = ''
        self.user_id_ = (int)(user_id)
        self.s_ = fgourl.NewSession()
        self.builder_ = ParameterBuilder(user_id, auth_key, secret_key)

    def Post(self, url):
        res = fgourl.PostReq(self.s_, url, self.builder_.Build())
        self.builder_.Clean()
        return res

    def topLogin_s(self):
        DataWebhook = []  
        
        idk = self.builder_.get_idempotency_key()
        idempotency_key_signature = os.environ.get('IDEMPOTENCY_KEY_SIGNATURE_SECRET')
        device_info = os.environ.get('DEVICE_INFO_SECRET')
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        url = f'{idempotency_key_signature}userId={self.user_id_}&idempotencyKey={idk}'
        result = requests.get(url, headers=headers, verify=False).text
        
        lastAccessTime = self.builder_.parameter_list_[5][1]
        userState = (-int(lastAccessTime) >>
                     2) ^ self.user_id_ & fgourl.data_server_folder_crc_

        self.builder_.AddParameter(
            'assetbundleFolder', fgourl.asset_bundle_folder_)
        self.builder_.AddParameter('idempotencyKeySignature', result)
        self.builder_.AddParameter('deviceInfo', device_info)
        self.builder_.AddParameter('isTerminalLogin', '1')
        self.builder_.AddParameter('userState', str(userState))

        data = self.Post(
            f'{fgourl.server_addr_}/login/top?_userId={self.user_id_}')

        responses = data['response']
        
        with open('login.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        self.name_ = hashlib.md5(
            data['cache']['replaced']['userGame'][0]['name'].encode('utf-8')).hexdigest()
        stone = data['cache']['replaced']['userGame'][0]['stone']
        lv = data['cache']['replaced']['userGame'][0]['lv']
        ticket = 0
        goldenfruit = 0
        silverfruit = 0
        bronzefruit = 0
        bluebronzesapling = 0
        bluebronzefruit = 0
        pureprism = 0
        sqf01 = 0
        holygrail = 0

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 4001:
                ticket = item['num']
                break
        
        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 100:
                goldenfruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 101:
                silverfruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 102:
                bronzefruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 103:
                bluebronzesapling = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 104:
                bluebronzefruit = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 46:
                pureprism = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 16:
                sqf01 = item['num']
                break

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 7999:
                holygrail = item['num']
                break

        
        rewards = Rewards(stone, lv, ticket, goldenfruit, silverfruit, bronzefruit, bluebronzesapling, bluebronzefruit, pureprism, sqf01, holygrail)

        DataWebhook.append(rewards)

        login_days = data['cache']['updated']['userLogin'][0]['seqLoginCount']
        total_days = data['cache']['updated']['userLogin'][0]['totalLoginCount']
        name1 = data['cache']['replaced']['userGame'][0]['name']
        fpids1 = data['cache']['replaced']['userGame'][0]['friendCode']

        act_max = data['cache']['replaced']['userGame'][0]['actMax']
        act_recover_at = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        carryOverActPoint = data['cache']['replaced']['userGame'][0]['carryOverActPoint']
        serverTime = data['cache']['serverTime']
        ap_points = act_recover_at - serverTime
        remaining_ap = 0
    
        if ap_points > 0:
            lost_ap_point = (ap_points + 299) // 300
            if act_max >= lost_ap_point:
                remaining_ap_int = act_max - lost_ap_point
                remaining_ap = int(remaining_ap_int)
            else:
                main.logger.info("失去的AP点超过了当前actMax值-计算失败")
        
        now_act = (act_max - (act_recover_at - mytime.GetTimeStamp()) / 300)

        add_fp = data['response'][0]['success']['addFriendPoint']
        total_fp = data['cache']['replaced']['tblUserGame'][0]['friendPoint']

        login = Login(
            self.name_,
            login_days,
            total_days,
            act_max, act_recover_at,
            now_act,
            add_fp,
            total_fp,
            name1,
            fpids1,
            remaining_ap
        )

        DataWebhook.append(login)

        if 'seqLoginBonus' in data['response'][0]['success']:
            bonus_message = data['response'][0]['success']['seqLoginBonus'][0]['message']

            items = []
            items_camp_bonus = []

            for i in data['response'][0]['success']['seqLoginBonus'][0]['items']:
                items.append(f'{i["name"]} x{i["num"]}')

            if 'campaignbonus' in data['response'][0]['success']:
                bonus_name = data['response'][0]['success']['campaignbonus'][0]['name']
                bonus_detail = data['response'][0]['success']['campaignbonus'][0]['detail']

                for i in data['response'][0]['success']['campaignbonus'][0]['items']:
                    items_camp_bonus.append(f'{i["name"]} x{i["num"]}')
            else:
                bonus_name = None
                bonus_detail = None

            bonus = Bonus(bonus_message, items, bonus_name,
                          bonus_detail, items_camp_bonus)
            DataWebhook.append(bonus)
        else:
            DataWebhook.append("No Bonus")

        webhook.topLogin(DataWebhook)
        

    def buyBlueApple(self):
        with open('login.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            actRecoverAt = data['cache']['replaced']['userGame'][0]['actRecoverAt']
            actMax = data['cache']['replaced']['userGame'][0]['actMax']
            carryOverActPoint = data['cache']['replaced']['userGame'][0]['carryOverActPoint']
            serverTime = data['cache']['serverTime']
            
            bluebronzesapling = 0 
            for item in data['cache']['replaced']['userItem']:
                if item['itemId'] == 103:
                    bluebronzesapling = item['num']
                    break
                    
            ap_points = actRecoverAt - serverTime
            
            if ap_points > 0:
               lost_ap_point = (ap_points + 299) // 300
               
               if actMax >= lost_ap_point:
                   remaining_ap = actMax - lost_ap_point
                   remaining_ap_int = int(remaining_ap)


               if bluebronzesapling > 0:
                   quantity = remaining_ap_int // 40
                   if bluebronzesapling < quantity:
                       num_to_purchase = bluebronzesapling
                   else:
                       num_to_purchase = quantity

                   self.builder_.AddParameter('id', '13000000')
                   self.builder_.AddParameter('num', str(num_to_purchase))

                   data = self.Post(f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}')
                   responses = data['response']

                   for response in responses:
                       resCode = response['resCode']
                       resSuccess = response['success']
                       nid = response["nid"]

                       if (resCode != "00"):
                           continue

                       if nid == "purchase":
                           if "purchaseName" in resSuccess and "purchaseNum" in resSuccess:
                               purchaseName = resSuccess['purchaseName']
                               purchaseNum = resSuccess['purchaseNum']

                               main.logger.info(f"\n========================================\n[+] {purchaseNum}x {purchaseName} 购买成功\n========================================")
                               webhook.shop(purchaseName, purchaseNum)
               else:
                   main.logger.info(f"\n ======================================== \n ＞︿＜ 青銅の苗木が足りないヽ (*。>Д<)o゜ \n ======================================== " )
    

    def drawFP(self):
        self.builder_.AddParameter('storyAdjustIds', '[]')
        self.builder_.AddParameter('gachaId', '1')
        self.builder_.AddParameter('num', '10')
        self.builder_.AddParameter('ticketItemId', '0')
        self.builder_.AddParameter('shopIdIndex', '1')

        if main.fate_region == "NA":
            gachaSubId = GetGachaSubIdFP("NA")
            if gachaSubId is None:
                gachaSubId = "0" 
            self.builder_.AddParameter('gachaSubId', gachaSubId)
            main.logger.info(f"\n ======================================== \n [+] 召唤卡池GachaSubId ： {gachaSubId} \n ======================================== " )
        else:
            gachaSubId = GetGachaSubIdFP("JP")
            if gachaSubId is None:
                gachaSubId = "0" 
            self.builder_.AddParameter('gachaSubId', gachaSubId)
            main.logger.info(f"\n ======================================== \n [+] 召唤卡池GachaSubId ： {gachaSubId} \n ======================================== " )

        data = self.Post(
            f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')

        responses = data['response']

        servantArray = []
        missionArray = []

        for response in responses:
            resCode = response['resCode']
            resSuccess = response['success']

            if (resCode != "00"):
                continue

            if "gachaInfos" in resSuccess:
                for info in resSuccess['gachaInfos']:
                    servantArray.append(
                        gacha.gachaInfoServant(
                            info['isNew'], info['objectId'], info['sellMana'], info['sellQp']
                        )
                    )

            if "eventMissionAnnounce" in resSuccess:
                for mission in resSuccess["eventMissionAnnounce"]:
                    missionArray.append(
                        gacha.EventMission(
                            mission['message'], mission['progressFrom'], mission['progressTo'], mission['condition']
                        )
                    )

        webhook.drawFP(servantArray, missionArray)

    def topHome(self):
        self.Post(f'{fgourl.server_addr_}/home/top?_userId={self.user_id_}')


    def lq001(self):
         # https://game.fate-go.jp/present/list?_userId=
          
        data = self.Post(
            f'{fgourl.server_addr_}/present/list?_userId={self.user_id_}')
        
        responses = data['response']
        main.logger.info(f"\n ======================================== \n [+] 读取礼物盒 \n ======================================== " )

    def lq002(self):
         # https://game.fate-go.jp/present/receive?_userId=
        with open('login.json', 'r', encoding='utf-8')as f:
            data = json.load(f)

        present_ids = []
        for item in data['cache']['replaced']['userPresentBox']:
            if item['objectId'] in [2, 6, 11, 16, 3, 46, 18, 48, 4001, 100, 101, 102, 103, 104, 1, 4, 7998, 7999, 1000, 2000, 6999, 9570400, 9670400]: #添加你需要领取的物品 Id 或者 baseSvtId 进入筛选列表
                present_ids.append(str(item['presentId']))

        with open('JJM.json', 'w') as f:
            json.dump(present_ids, f, ensure_ascii=False, indent=4)

        main.logger.info(f"\n ======================================== \n [+] 礼物盒内容解析完成 \n ======================================== " )

        time.sleep(1)

        if os.path.exists('JJM.json'):
            with open('JJM.json', 'r', encoding='utf-8') as file:
                data1 = json.load(file)

            data = data1

            msgpack_data = msgpack.packb(data)

            base64_encoded_data = base64.b64encode(msgpack_data).decode()

            self.builder_.AddParameter('presentIds', base64_encoded_data)
            self.builder_.AddParameter('itemSelectIdx', '0')
            self.builder_.AddParameter('itemSelectNum', '0')

            data = self.Post(
                f'{fgourl.server_addr_}/present/receive?_userId={self.user_id_}')
    
            responses = data['response']

            main.logger.info(f"\n ======================================== \n [+] 领取成功 \n ======================================== " )
        else:
            main.logger.info(f"\n ======================================== \n [+] 没有物品可领取 \n ======================================== " )
