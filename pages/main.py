import dataManager as dataMan
import time
import chalk
from readchar import key, readkey
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

    if dataMan.isHasBackup():
        print(chalk.red("\n/!\\ WARNING: Backup file found (data Backup.yml) /!\\"))
        print(
            chalk.red(f"with error message: {dataMan.isValidFile('data Backup.yml')}"))
        print(chalk.red("Delete 'data Backup.yml' to dismiss this warning"))

    inputMode = "money"
    selectedCmdInd = 0
    strMoney = ""
    print("Enter amount of money or move arrow to select command")

    cmdModes = [("editing money data", lambda: "edit"),
                ("insert new money data", lambda: "insert"),
                ("exit program", lambda: exit(0))]
    print(chalk.yellow(f"$ : "), end="", flush=True)
    while True:
        keyInput = readkey()
        # ? reset
        moveCursor(left=9999)
        if inputMode == "cmd":
            moveCursor(up=len(cmdModes) + 1)
        print("\033[0J", end="", flush=True)

        # ? process
        if inputMode == "money":
            if keyInput == key.BACKSPACE:
                strMoney = strMoney[:-1]
            elif keyInput == key.ENTER:
                newMoney = parseNumFromStr(strMoney)
                if todayStr in moneyData:
                    newMoney += moneyData[todayStr]
                dataMan.insertOrModify(todayStr, newMoney)
                return "main"
            elif keyInput in "0123456789.+-":
                strMoney += keyInput
            elif keyInput == key.UP or keyInput == key.DOWN:
                inputMode = "cmd"
                selectedCmdInd = 0

        elif inputMode == "cmd":
            if keyInput == key.UP:
                selectedCmdInd = max(selectedCmdInd - 1, 0)
            elif keyInput == key.DOWN:
                selectedCmdInd = min(selectedCmdInd + 1, len(cmdModes) - 1)
            elif keyInput == key.ENTER:
                moveCursor(left=9999, up=9999)
                print("\033[0J", end="", flush=True)
                return cmdModes[selectedCmdInd][1]()
            elif keyInput in "0123456789.+-":
                inputMode = "money"
                strMoney = keyInput

        # ? display
        if inputMode == "money":
            thisNum = parseNumFromStr(strMoney)
            if thisNum == []:
                print(chalk.yellow(f"$ : {strMoney}"), end="", flush=True)
            elif thisNum >= 0:
                print(chalk.green(f"$ : {strMoney}"), end="", flush=True)
            else:
                print(chalk.red(f"$ : {strMoney}"), end="", flush=True)

        elif inputMode == "cmd":
            for i in range(len(cmdModes)):
                if i == selectedCmdInd:
                    print(chalk.yellow(f"-> {cmdModes[i][0]}"))
                else:
                    print(f"   {cmdModes[i][0]}")
