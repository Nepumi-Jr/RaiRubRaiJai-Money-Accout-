import os
import yaml
import moneyDataModel as mData


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
                yaml.load(f, Loader=yaml.Loader)
        except yaml.YAMLError as e:
            return e
    else:
        return "File not found"

    if not isinstance(moneyData, dict):
        return False

    if len(moneyData) > 0:
        if not isinstance(list(moneyData.keys())[0], str):
            return False
        if not isinstance(list(moneyData.values())[0], list):
            return False

        if len(list(moneyData.values())[0]) > 0 and not isinstance(list(moneyData.values())[0][0], mData.MoneyData):
            return False

    return True


def loadData():
    global moneyData, accumulatedMoney
    v3Validating = isValidV3File("dataV3.yml")
    v2Validating = isValidV2File("dataV2.yml")
    v1Validating = isValidFile("data.yml")

    if v3Validating == False:
        doBackupData()

    if v3Validating == True:
        with open("dataV3.yml", "r") as f:
            moneyData = yaml.load(f, Loader=yaml.Loader)
    elif v2Validating == True:
        # ? Convert dataV2.yml to dataV3.yml
        with open("dataV2.yml", "r") as f:
            oldMoneyData = yaml.load(f, Loader=yaml.FullLoader)
        for key in oldMoneyData:
            moneyData[key] = []
            moneyData[key].append(mData.MoneyData(oldMoneyData[key][0], 9999))
            moneyData[key].append(mData.MoneyData(-oldMoneyData[key][1], 9999))
        saveData()
    elif v1Validating == True:
        # ? Convert data.yml to dataV3.yml
        with open("dataV2.yml", "r") as f:
            oldMoneyData = yaml.load(f, Loader=yaml.FullLoader)
        for key in oldMoneyData:
            moneyData[key] = [mData.MoneyData(oldMoneyData[key], 9999)]
    else:
        moneyData = {}
        saveData()

    reloadAccumulatedMoney()


def reloadAccumulatedMoney():
    global accumulatedMoney
    accumulatedMoney = {}
    total = 0
    for key in sorted(list(moneyData.keys())):
        for money in moneyData[key]:
            total += money.amount
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
    if os.path.exists("dataV3.yml"):
        if os.path.exists("data Backup.yml"):
            os.remove("data Backup.yml")
        os.rename("dataV3.yml", "data Backup.yml")


def isHasBackup():
    if os.path.exists("data Backup.yml"):
        return True
    return False


def saveData():
    with open("dataV3.yml", "w") as f:
        yaml.dump(moneyData, f)


def getMoneyData():
    loadData()
    return moneyData


def insert(day, moneyAmount, labelId):
    global moneyData
    if day in moneyData:
        moneyData[day].append(mData.MoneyData(moneyAmount, labelId))
    else:
        moneyData[day] = [mData.MoneyData(moneyAmount, labelId)]
    reloadAccumulatedMoney()
    saveData()


def modify(day, index, newMoneyAmount, newLabelId):
    global moneyData
    if day in moneyData:
        moneyData[day][index] = mData.MoneyData(newMoneyAmount, newLabelId)
    reloadAccumulatedMoney()
    saveData()


def deleteMoneyData(day, index):
    global moneyData
    if day in moneyData:
        del moneyData[day][index]
        if len(moneyData[day]) == 0:
            del moneyData[day]
        reloadAccumulatedMoney()
        saveData()


def deleteDayData(day):
    global moneyData
    if day in moneyData:
        del moneyData[day]
        reloadAccumulatedMoney()
        saveData()
