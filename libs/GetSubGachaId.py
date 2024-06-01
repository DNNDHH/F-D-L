from typing import List

import requests

from mytime import GetTimeStamp


def isMatchedQuestCondition(region: str, userQuest: List, commonReleaseId: int):
    api = f"https://api.atlasacademy.io/nice/{region}/common-release/{commonReleaseId}"
    response = requests.get(api)
    response.raise_for_status()
    condition = response.json()
    if len(condition) > 0 and condition[0].get("condType", "") == "questClear":
        for quest in userQuest:
            condQuestId = condition[0]["condId"]
            condClearNum = condition[0]["condNum"]
            # Don't know quest["clearNum"] equl condClearNum is fine or not
            if quest["questId"] == condQuestId and quest["clearNum"] > condClearNum:
                return True
            elif quest["questId"] == condQuestId and quest["clearNum"] <= condClearNum:
                return False
        return False
    else:
        # please implement webhook sned error or etc here
        pass


# Get Friend Summon Gacha Sub Id
def GetGachaSubIdFP(region, userQuest: List = []):
    api = f"https://git.atlasacademy.io/atlasacademy/fgo-game-data/raw/branch/{region}/master/mstGachaSub.json"
    response = requests.get(api)
    data = list(response.json())
    data.reverse()

    timeNow = GetTimeStamp()
    actiaveGacha = []
    for gacha in data:
        if gacha["closedAt"] > timeNow and gacha["openedAt"] < timeNow:
            actiaveGacha.append(gacha)
        else:
            break

    if len(actiaveGacha) == 0:
        # please implement webhook sned error or etc here
        pass

    # Start by sorting from highest to lowest priority, then within the same priority, sort by commonReleaseId
    sortedGachaList = sorted(actiaveGacha, key=lambda x: (x["priority"], x["commonReleaseId"]), reverse=True)
    for gacha in sortedGachaList:
        if gacha["commonReleaseId"] != 0 and isMatchedQuestCondition(region, userQuest, gacha["commonReleaseId"]):
            return gacha["id"]
        elif gacha["commonReleaseId"] == 0:
            return gacha["id"]
    return 0  # If no event or commonReleaseId is matched, return 0
