import os
import yaml

moneyData = {}


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


def loadData():
    global moneyData
    if isValidFile("data.yml") == True:
        with open("data.yml", "r") as f:
            moneyData = yaml.load(f, Loader=yaml.FullLoader)


def doBackupData():
    if os.path.exists("data.yml"):
        os.rename("data.yml", "data Backup.yml")


def isHasBackup():
    if os.path.exists("data Backup.yml"):
        return True
    return False


def saveData():
    with open("data.yml", "w") as f:
        yaml.dump(moneyData, f)


def getMoneyData():
    loadData()
    return moneyData


def insertOrModify(day, money):
    global moneyData
    moneyData[day] = money
    saveData()


def deleteData(day):
    global moneyData
    if day in moneyData:
        del moneyData[day]
        saveData()
