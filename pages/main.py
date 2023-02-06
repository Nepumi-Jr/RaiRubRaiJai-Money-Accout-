import dataManager as dataMan
import time
from readchar import key, readkey
from util import *
from printUtil import *


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

    print(paintTextFormat("\nMONEY", ANSIColorCode.MAGENTA, bold=True, underline=True),
          paintTextFormat("SUMMARY...", ANSIColorCode.MAGENTA, bold=True, underline=True))
    if sumMoney >= 200:
        printGreen(f"\t-> {sumMoney} Baht")
    elif sumMoney >= 0:
        printYellow(f"\t-> {sumMoney} Baht")
    else:
        printRed(f"\t-> {sumMoney} Baht")

    # ? Monthly Summary
    sumMoney = 0
    printMagenta("\nMONTY SUMMARY...", bold=True)
    prefixYearMonth = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}"
    for day in moneyData:
        if day.startswith(prefixYearMonth):
            sumMoney += moneyData[day]

    printMagenta(
        f"  [ {monthNumToStr(thisTime.tm_mon)} {thisTime.tm_year} ]")
    if sumMoney >= 200:
        printGreen(f"\t-> {sumMoney} Baht")
    elif sumMoney >= 0:
        printYellow(f"\t-> {sumMoney} Baht")
    else:
        printRed(f"\t-> {sumMoney} Baht")

    todayStr = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}-{thisTime.tm_mday:02d}"

    printStyle(
        f"\nTODAY'S MONEY... ({getFullDateStr(thisTime.tm_mday, thisTime.tm_mon, thisTime.tm_year)})", bold=True)
    if todayStr in moneyData:
        if moneyData[todayStr] >= 0:
            printGreen(f"\t-> {moneyData[todayStr]} Baht")
        else:
            printRed(f"\t-> {moneyData[todayStr]} Baht")
    else:
        printYellow("\t   No data")

    print("\n")
    printStyle("Last 7 days...", bold=True)
    allDay = list(moneyData.keys())
    sorted(allDay, reverse=True)
    for eachDay in allDay[:-7:-1]:
        if moneyData[eachDay] >= 0:
            printGreen(
                f"\t-> {eachDay} : {moneyData[eachDay]} Baht", bold=(eachDay == todayStr))
        else:
            printRed(
                f"\t-> {eachDay} : {moneyData[eachDay]} Baht", bold=(eachDay == todayStr))

    print("\n")

    if dataMan.isHasBackup():
        printRed("\n/!\\ WARNING: Backup file found (data Backup.yml) /!\\")
        printRed(
            f"with error message: {dataMan.isValidFile('data Backup.yml')}")
        printRed("Delete 'data Backup.yml' to dismiss this warning")

    inputMode = "money"
    selectedCmdInd = 0
    strMoney = ""
    print(paintTextFormat("Enter",
                          ANSIColorCode.YELLOW), "amount of money or move", paintTextFormat("arrow key",
                                                                                            ANSIColorCode.YELLOW), "to select command")

    cmdModes = [("editing money data", lambda: "edit"),
                ("exit program", lambda: exit(0))]
    printYellow(f"$ : ", end="", flush=True)
    while True:
        keyInput = readkey()
        # ? reset
        moveCursor(left=9999)
        if inputMode == "cmd":
            moveCursor(up=len(cmdModes) + 1)
        clearAfterCursor()

        # ? process
        if inputMode == "money":
            if keyInput == key.BACKSPACE:
                strMoney = strMoney[:-1]
            elif keyInput == key.ENTER:
                newMoney = parseNumFromStr(strMoney)
                if newMoney != []:
                    if todayStr in moneyData:
                        newMoney += moneyData[todayStr]
                    dataMan.insertOrModify(todayStr, newMoney)
                    return "main"
            elif keyInput in "0123456789.+-":
                strMoney += keyInput
            elif keyInput == key.UP or keyInput == key.DOWN or keyInput == key.ESC or keyInput == key.LEFT or keyInput == key.RIGHT:
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
            elif keyInput == key.ESC:
                inputMode = "money"
                strMoney = ""
            elif keyInput in "0123456789.+-":
                inputMode = "money"
                strMoney = keyInput

        # ? display
        if inputMode == "money":
            thisNum = parseNumFromStr(strMoney)
            if thisNum == []:
                printYellow(f"$ : {strMoney}", end="", flush=True)
            elif thisNum >= 0:
                printGreen(f"$ : {strMoney}", end="", flush=True)
            else:
                printRed(f"$ : {strMoney}", end="", flush=True)

        elif inputMode == "cmd":
            for i in range(len(cmdModes)):
                if i == selectedCmdInd:
                    if cmdModes[i][0] == "exit program":
                        printRed(f"-> {cmdModes[i][0]}")
                    else:
                        print(paintTextFormat(
                            f"-> {cmdModes[i][0]}", "\033[38;5;39m"))
                else:
                    print(f"   {cmdModes[i][0]}")
