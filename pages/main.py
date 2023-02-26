import dataManager as dataMan
import time
from readchar import key, readkey
from util import *
from printUtil import *

import moneyLabelManager as label


def screen():

    moneyData = dataMan.getMoneyData()

    isValidData = dataMan.isValidV3File("dataV3.yml")
    if isValidData != True and isValidData != "File not found":
        dataMan.doBackupData()

    if isValidData == True:
        dataMan.loadData()

    thisTime = time.localtime(time.time())
    todayStr = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}-{thisTime.tm_mday:02d}"

    sumMoney = dataMan.getLastAccumulatedMoney(todayStr)

    # ? print money summary

    print(paintTextFormat("\nMONEY", ANSIColorCode.MAGENTA, bold=True, underline=True),
          paintTextFormat("SUMMARY...", ANSIColorCode.MAGENTA, bold=True, underline=True))
    if sumMoney >= 200:
        printGreen(f"\t-> {sumMoney} Baht")
    elif sumMoney >= 0:
        printYellow(f"\t-> {sumMoney} Baht")
    else:
        printRed(f"\t-> {sumMoney} Baht")

    # ? print today's money

    expectedCostMoneyToday = sumMoney // (getDaysInMonth(
        thisTime.tm_year, thisTime.tm_mon) - thisTime.tm_mday + 1)
    printStyle(
        f"\nTODAY'S MONEY... ({getFullDateStr(thisTime.tm_mday, thisTime.tm_mon, thisTime.tm_year)})", bold=True)
    if todayStr in moneyData:
        costToday = 0
        incomeToday = 0
        for e in moneyData[todayStr]:
            if e.isIncome():
                printGreen(f"\t{e.getLabel()} +{e.amount}$")
                incomeToday += e.amount
            else:
                printRed(f"\t{e.getLabel()} {e.amount}$")
                costToday += e.amount

        printGreen(f"\n\tTOTAL : +{incomeToday}$", end="")

        if abs(costToday) >= expectedCostMoneyToday:
            # ? exceed expected cost money
            printRed(f"   {costToday}$")
        else:
            printYellow(f"   {costToday}$")
    else:
        printYellow("\t   No data")
    printMagenta(
        f"\t-> Expected cost money: {expectedCostMoneyToday}$", italic=True)

    # ? print monthly summary
    printStyle("\nMONTHLY SUMMARY...", bold=True)
    costInMonth = 0
    incomeInMonth = 0
    for day in range(1, getDaysInMonth(thisTime.tm_year, thisTime.tm_mon) + 1):
        thisDayStr = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}-{day:02d}"
        if thisDayStr in moneyData:
            for e in moneyData[thisDayStr]:
                if e.isIncome():
                    incomeInMonth += e.amount
                else:
                    costInMonth += e.amount

    printGreen(f"\t+{incomeInMonth}$", end="")
    printRed(f"\t{costInMonth}$", end="")
    printMagenta(f"\tΔ {incomeInMonth + costInMonth}$", italic=True)

    # ? print last 7 days

    print("\n")
    printStyle("Last 7 days...", bold=True)

    allDay = list(moneyData.keys())
    allDay = sorted(allDay, reverse=True)[:7]

    for eachDay in allDay:
        eYear, eMonth = map(int, eachDay.split("-")[:2])
        expectedCostMoney = dataMan.getLastAccumulatedMoney(
            eachDay) // (getDaysInMonth(eYear, eMonth) - int(eachDay.split("-")[2]) + 1)
        print(f"\t{eachDay} : ", end="")

        incomeMoney = 0
        costMoney = 0
        for e in moneyData[eachDay]:
            if e.isIncome():
                incomeMoney += e.amount
            else:
                costMoney += e.amount

        printGreen(f"+{incomeMoney}$",
                   bold=(eachDay == todayStr), end="")

        if costMoney >= expectedCostMoney:  # ? 1 is index of cost money
            # ? exceed expected cost money
            printRed(f"\t{costMoney}$",
                     bold=(eachDay == todayStr), end="")
        else:
            printYellow(f"\t{costMoney}$",
                        bold=(eachDay == todayStr), end="")

        printMagenta(
            f"\t({expectedCostMoney}$)", bold=(eachDay == todayStr), italic=True)

    print("\n")

    if dataMan.isHasBackup():
        printRed("\n/!\\ WARNING: Backup file found (data Backup.yml) /!\\")
        printRed(
            f"with error message: {dataMan.isValidV3File('data Backup.yml')}")
        printRed("Delete 'data Backup.yml' to dismiss this warning")

    disp = "[[Enter]] amount of money, press [[up]] and [[down]] to select Label\npress [[esc]] to select command\n"
    disp = disp.replace("[[", ANSIColorCode.YELLOW)
    disp = disp.replace("]]", "\033[0m")
    print(disp)

    inputMode = "money"
    selectedCmdInd = 0
    strMoney = ""
    isIncome = True
    selectedLabelInd = 0  # ? Don't confuse with LabelID :D
    incomeLabelsId = label.getAllLabelId(True)
    costLabelsId = label.getAllLabelId(False)
    thisLabelId = costLabelsId[0]
    cmdModes = [("editing money data", "edit", "\033[38;5;39m"),
                ("export to CSV", "CSV", ANSIColorCode.GREEN),
                ("exit program", "exit", ANSIColorCode.RED)]

    # ? init display
    printGreen(f"{label.getLabel(isIncome, thisLabelId).description}",
               italic=True)
    print(label.getLabel(isIncome, thisLabelId).label, end="", flush=True)
    printGreen(f" : ", end="", flush=True)

    while True:
        keyInput = readkey()
        # ? reset
        moveCursor(left=9999, up=2)
        if inputMode == "cmd":
            moveCursor(up=len(cmdModes))
        clearAfterCursor()

        # ? process
        if inputMode == "money":
            if keyInput == key.BACKSPACE:
                strMoney = strMoney[:-1]
            elif keyInput == key.ENTER:
                newMoney = parseNumFromStr(strMoney)
                if newMoney != []:
                    dataMan.insert(
                        todayStr, newMoney if isIncome else -newMoney, thisLabelId)
                    return "main"
            elif keyInput in "0123456789":
                strMoney += keyInput
            elif keyInput == '+':
                if not isIncome:
                    selectedLabelInd = 0
                isIncome = True
            elif keyInput == '-':
                selectedLabelInd = 0
                isIncome = not isIncome
            elif keyInput == key.UP:
                selectedLabelInd = max(selectedLabelInd - 1, 0)
            elif keyInput == key.DOWN:
                if isIncome:
                    selectedLabelInd = min(
                        selectedLabelInd + 1, len(incomeLabelsId) - 1)
                else:
                    selectedLabelInd = min(
                        selectedLabelInd + 1, len(costLabelsId) - 1)

            elif keyInput == key.ESC:
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

                if cmdModes[selectedCmdInd][1] == "edit":
                    return "edit"
                elif cmdModes[selectedCmdInd][1] == "CSV":
                    return "csv"
                elif cmdModes[selectedCmdInd][1] == "exit":
                    exit(0)
                return "main"
            elif keyInput == key.ESC:
                inputMode = "money"
                strMoney = ""
            elif keyInput in "0123456789.+-":
                inputMode = "money"
                strMoney = keyInput

        thisLabelId = incomeLabelsId[selectedLabelInd] if isIncome else costLabelsId[selectedLabelInd]

        # ? display
        if inputMode == "money":
            thisNum = parseNumFromStr(strMoney)

            if isIncome:
                printGreen(
                    f"{label.getLabel(isIncome, thisLabelId).description}", italic=True)
                print(label.getLabel(isIncome, thisLabelId).label,
                      end="", flush=True)
                printGreen(f" : {strMoney}", end="", flush=True)
            else:
                printRed(
                    f"{label.getLabel(isIncome, thisLabelId).description}", italic=True)
                print(label.getLabel(isIncome, thisLabelId).label,
                      end="", flush=True)
                printRed(f" : -{strMoney}", end="", flush=True)

        elif inputMode == "cmd":
            for i in range(len(cmdModes)):
                if i == selectedCmdInd:
                    print(paintTextFormat(
                        f"-> {cmdModes[i][0]}", cmdModes[i][2]))
                else:
                    print(f"   {cmdModes[i][0]}")
