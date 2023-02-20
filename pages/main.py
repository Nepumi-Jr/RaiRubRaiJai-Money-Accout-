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
    todayStr = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}-{thisTime.tm_mday:02d}"

    sumMoney = dataMan.getLastAccumulatedMoney(todayStr)

    print(paintTextFormat("\nMONEY", ANSIColorCode.MAGENTA, bold=True, underline=True),
          paintTextFormat("SUMMARY...", ANSIColorCode.MAGENTA, bold=True, underline=True))
    if sumMoney >= 200:
        printGreen(f"\t-> {sumMoney} Baht")
    elif sumMoney >= 0:
        printYellow(f"\t-> {sumMoney} Baht")
    else:
        printRed(f"\t-> {sumMoney} Baht")

    # ? Monthly Summary
    # sumMoney = 0
    # printMagenta("\nMONTY SUMMARY...", bold=True)
    # prefixYearMonth = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}"
    # for day in moneyData:
    #     if day.startswith(prefixYearMonth):
    #         sumMoney += moneyData[day][0]
    #         sumMoney -= moneyData[day][1]

    # printMagenta(
    #     f"  [ {monthNumToStr(thisTime.tm_mon)} {thisTime.tm_year} ]")
    # if sumMoney >= 200:
    #     printGreen(f"\t-> {sumMoney} Baht")
    # elif sumMoney >= 0:
    #     printYellow(f"\t-> {sumMoney} Baht")
    # else:
    #     printRed(f"\t-> {sumMoney} Baht")

    expectedCostMoneyToday = sumMoney // (getDaysInMonth(
        thisTime.tm_year, thisTime.tm_mon) - thisTime.tm_mday + 1)
    printStyle(
        f"\nTODAY'S MONEY... ({getFullDateStr(thisTime.tm_mday, thisTime.tm_mon, thisTime.tm_year)})", bold=True)
    if todayStr in moneyData:
        printGreen(f"\t-> +{moneyData[todayStr][0]}$", end="")

        if moneyData[todayStr][1] >= expectedCostMoneyToday:  # ? 1 is index of cost money
            # ? exceed expected cost money
            printRed(f"   -{moneyData[todayStr][1]}$")
        else:
            printYellow(f"   -{moneyData[todayStr][1]}$")
    else:
        printYellow("\t   No data")
    printMagenta(
        f"\t-> Expected cost money: {expectedCostMoneyToday}$", italic=True)

    print("\n")
    printStyle("Last 7 days...", bold=True)

    allDay = list(moneyData.keys())
    allDay = sorted(allDay, reverse=True)[:7]

    for eachDay in allDay:
        eYear, eMonth = map(int, eachDay.split("-")[:2])
        expectedCostMoney = dataMan.getLastAccumulatedMoney(
            eachDay) // (getDaysInMonth(eYear, eMonth) - int(eachDay.split("-")[2]) + 1)
        print(f"\t{eachDay} : ", end="")

        printGreen(f"+{moneyData[eachDay][0]}$",
                   bold=(eachDay == todayStr), end="")

        if moneyData[eachDay][1] >= expectedCostMoney:  # ? 1 is index of cost money
            # ? exceed expected cost money
            printRed(f"\t-{moneyData[eachDay][1]}$",
                     bold=(eachDay == todayStr), end="")
        else:
            printYellow(f"\t-{moneyData[eachDay][1]}$",
                        bold=(eachDay == todayStr), end="")

        printMagenta(
            f"\t({expectedCostMoney}$)", bold=(eachDay == todayStr), italic=True)

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

    cmdModes = [("reset income(+) data (for today)", "reset Pos", ANSIColorCode.YELLOW),
                ("reset cost(-) data (for today)",
                 "reset Cost", ANSIColorCode.YELLOW),
                ("editing money data", "edit", "\033[38;5;39m"),
                ("exit program", "exit", ANSIColorCode.RED)]
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

                if cmdModes[selectedCmdInd][1] == "reset Pos":
                    dataMan.resetData(todayStr, pos=True)
                elif cmdModes[selectedCmdInd][1] == "reset Cost":
                    dataMan.resetData(todayStr, neg=True)
                elif cmdModes[selectedCmdInd][1] == "edit":
                    return "edit"
                elif cmdModes[selectedCmdInd][1] == "exit":
                    exit(0)
                return "main"
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
                    print(paintTextFormat(
                        f"-> {cmdModes[i][0]}", cmdModes[i][2]))
                else:
                    print(f"   {cmdModes[i][0]}")
