import os
import yaml

moneyData = {}
accumulatedMoney = {}


def isValidFile(fileName):
    if os.path.exists(fileName):
        try:
            with open(fileName, "r") as f:
                yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            return e
    else:
        return "File not found"

    if not isinstance(moneyData, dict):
        return "data.yml is not a valid yaml file"

    return True


def isValidV2File(fileName):
    if os.path.exists(fileName):
        try:
            with open(fileName, "r") as f:
                yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            return e
    else:
        return "File not found"

    if not isinstance(moneyData, dict):
        return "dataV2.yml is not a valid yaml file"

    if len(moneyData) > 0:
        if not isinstance(list(moneyData.keys())[0], str):
            return "dataV2.yml is not a valid yaml file"
        if not isinstance(list(moneyData.values())[0], list):
            return "dataV2.yml is not a valid yaml file"
        if not isinstance(list(moneyData.values())[0][0], int) and not isinstance(list(moneyData.values())[0][1], int):
            return "dataV2.yml is not a valid yaml file"

        if len(list(moneyData.values())[0]) != 2:
            return "dataV2.yml is not a valid yaml file"

    return True


def isValidV3File(fileName):
    if os.path.exists(fileName):
        try:
            with open(fileName, "r") as f:
                yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            return e
    else:
        return "File not found"

    if not isinstance(moneyData, dict):
        return "dataV2.yml is not a valid yaml file"

    if len(moneyData) > 0:
        if not isinstance(list(moneyData.keys())[0], str):
            return "dataV2.yml is not a valid yaml file"
        if not isinstance(list(moneyData.values())[0], list):
            return "dataV2.yml is not a valid yaml file"
        if not isinstance(list(moneyData.values())[0][0], int) and not isinstance(list(moneyData.values())[0][1], int):
            return "dataV2.yml is not a valid yaml file"

        if len(list(moneyData.values())[0]) != 2:
            return "dataV2.yml is not a valid yaml file"

    return True


def loadData():
    global moneyData, accumulatedMoney
    v2Validating = isValidV2File("dataV2.yml")
    v1Validating = isValidFile("data.yml")

    if v2Validating == "dataV2.yml is not a valid yaml file":
        doBackupData()

    if v2Validating == True:
        with open("dataV2.yml", "r") as f:
            moneyData = yaml.load(f, Loader=yaml.FullLoader)
    elif v1Validating == True:
        # TODO: Convert data.yml to dataV2.yml
        with open("data.yml", "r") as f:
            moneyData = yaml.load(f, Loader=yaml.FullLoader)
        for key in moneyData:
            if moneyData[key] > 0:
                moneyData[key] = [moneyData[key], 0]
            else:
                moneyData[key] = [0, -moneyData[key]]

        saveData()
    else:
        moneyData = {}
        saveData()

    reloadAccumulatedMoney()


def reloadAccumulatedMoney():
    global accumulatedMoney
    accumulatedMoney = {}
    total = 0
    for key in sorted(list(moneyData.keys())):
        total += moneyData[key][0]
        total -= moneyData[key][1]
        accumulatedMoney[key] = total


def getLastAccumulatedMoney(day: str):
    global accumulatedMoney
    # ? day format: YYYY-MM-DD

    if len(accumulatedMoney) == 0:
        return 0

    # ? binary search
    lInd = 0
    rInd = len(accumulatedMoney) - 1
    result = "-1"
    while lInd <= rInd:
        mid = (lInd + rInd) // 2
        midStr = list(accumulatedMoney.keys())[mid]
        if midStr < day:
            result = midStr
            lInd = mid + 1
        else:
            rInd = mid - 1
    if result == "-1":
        return 0
    return accumulatedMoney[result]


def doBackupData():
    if os.path.exists("dataV2.yml"):
        os.rename("dataV2.yml", "data Backup.yml")


def isHasBackup():
    if os.path.exists("data Backup.yml"):
        return True
    return False


def saveData():
    with open("dataV2.yml", "w") as f:
        yaml.dump(moneyData, f)


def getMoneyData():
    loadData()
    return moneyData


def insertOrModify(day, money):
    global moneyData
    if day in moneyData:
        if money > 0:
            moneyData[day][0] += money
        else:
            moneyData[day][1] += -money
    else:
        if money > 0:
            moneyData[day] = [money, 0]
        else:
            moneyData[day] = [0, -money]
    reloadAccumulatedMoney()
    saveData()


def resetData(day, pos: bool = False, neg: bool = False):
    global moneyData
    insertOrModify(day, 0)
    if day in moneyData:
        if pos:
            moneyData[day][0] = 0
        if neg:
            moneyData[day][1] = 0
        reloadAccumulatedMoney()
        saveData()


def deleteData(day):
    global moneyData
    if day in moneyData:
        del moneyData[day]
        reloadAccumulatedMoney()
        saveData()
