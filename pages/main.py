import dataManager as dataMan
import time
import chalk
from util import *


def screen():

    moneyData = dataMan.getMoneyData()

    isValidData = dataMan.isValidFile("data.yml")
    if isValidData != True and isValidData != "File not found":
        dataMan.backupData()

    if isValidData == True:
        dataMan.loadData()

    thisTime = time.localtime(time.time())
    sumMoney = 0
    for eachDay in moneyData:
        sumMoney += moneyData[eachDay]

    print(chalk.magenta("\nMONEY", bold=True, underline=True),
          chalk.magenta("SUMMARY...", bold=True, underline=True))
    if sumMoney >= 200:
        print(chalk.green(f"\t-> {sumMoney} Baht"))
    elif sumMoney >= 0:
        print(chalk.yellow(f"\t-> {sumMoney} Baht"))
    else:
        print(chalk.red(f"\t-> {sumMoney} Baht"))

    # ? Monthly Summary
    sumMoney = 0
    print(chalk.magenta("\nMONTY SUMMARY...", bold=True))
    prefixYearMonth = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}"
    for day in moneyData:
        if day.startswith(prefixYearMonth):
            sumMoney += moneyData[day]

    print(chalk.magenta(
        f"  [ {monthNumToStr(thisTime.tm_mon)} {thisTime.tm_year} ]"))
    if sumMoney >= 200:
        print(chalk.green(f"\t-> {sumMoney} Baht"))
    elif sumMoney >= 0:
        print(chalk.yellow(f"\t-> {sumMoney} Baht"))
    else:
        print(chalk.red(f"\t-> {sumMoney} Baht"))

    todayStr = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}-{thisTime.tm_mday:02d}"

    print(chalk.white("\nTODAY'S MONEY...", bold=True))
    if todayStr in moneyData:
        if moneyData[todayStr] >= 0:
            print(chalk.green(f"\t-> {moneyData[todayStr]} Baht"))
        else:
            print(chalk.red(f"\t-> {moneyData[todayStr]} Baht"))
    else:
        print(chalk.yellow("\t   No data"))

    print("\n")
    print(chalk.white("Last 7 days...", bold=True))
    allDay = list(moneyData.keys())
    sorted(allDay, reverse=True)
    for eachDay in allDay[:-7:-1]:
        if moneyData[eachDay] >= 0:
            print(chalk.green(f"\t-> {eachDay} : {moneyData[eachDay]} Baht"))
        else:
            print(chalk.red(f"\t-> {eachDay} : {moneyData[eachDay]} Baht"))

    print("\n")
    print("'edit' for edit money data")
    print("'insert' for insert new money data")
    print()
    print("'exit' for exit")

    if dataMan.isHasBackup():
        print(chalk.red("\n/!\\ WARNING: Backup file found (data Backup.yml) /!\\"))
        print(
            chalk.red(f"with error message: {dataMan.isValidFile('data Backup.yml')}"))
        print(chalk.red("Delete 'data Backup.yml' to dismiss this warning"))

    inputCmd = input("Enter money or command : ").strip().lower()
    allNums = parseNumFromStr(inputCmd)
    if isinstance(allNums, list):
        # ? cmd
        if inputCmd.startswith("ed"):
            return "edit"
        elif inputCmd.startswith("ex"):
            exit(0)
        elif inputCmd.startswith("i"):
            return "insert"
    else:
        newMoney = allNums

        if todayStr in moneyData:
            moneyData[todayStr] += newMoney
        else:
            moneyData[todayStr] = newMoney

        dataMan.saveData()
        return "main"
