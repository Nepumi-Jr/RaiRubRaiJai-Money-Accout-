from readchar import key, readkey
import dataManager as dataMan
import time
import os
import inquirer

from util import *
from printUtil import *

editingDataMoney = None


def editDay(editDaySelected: str):
    global editingDataMoney
    os.system("cls")

    moneyData = dataMan.getMoneyData()

    print(paintTextFormat(f"Edit {editDaySelected}",
          "\033[38;5;39m", bold=True, underline=True), "\n")

    if editingDataMoney == None:
        printYellow("\t No data")
    else:
        printGreen(f"\t +{editingDataMoney[0]}$", end="")
        printRed(f"   -{editingDataMoney[1]}$")

    print("\n")

    inputMode = "money"
    pInputMode = inputMode
    selectedCmdInd = 0
    strMoney = ""
    print(paintTextFormat("Enter",
                          ANSIColorCode.YELLOW), "amount of money or move", paintTextFormat("arrow key",
                                                                                            ANSIColorCode.YELLOW), "to select command")

    cmdModes = [("continue to edit", "resume", ANSIColorCode.YELLOW),
                ("reset income(+) data (for today)",
                 "reset Pos", ANSIColorCode.YELLOW),
                ("reset cost(-) data (for today)",
                 "reset Cost", ANSIColorCode.YELLOW),
                ("remove this data", "remove", ANSIColorCode.RED),
                ("cancel this edit", "cancel", ANSIColorCode.YELLOW),
                ("save and exit", "save", ANSIColorCode.GREEN)]
    printYellow(f"$ : ", end="", flush=True)
    while True:
        keyInput = readkey()

        # ? process
        if inputMode == "money":
            if keyInput == key.BACKSPACE:
                strMoney = strMoney[:-1]
            elif keyInput == key.ENTER:
                newMoney = parseNumFromStr(strMoney)
                if newMoney != []:
                    if editingDataMoney == None:
                        editingDataMoney = [0, 0]
                    if newMoney > 0:
                        editingDataMoney[0] += newMoney
                    else:
                        editingDataMoney[1] += -newMoney
                return False
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

                if cmdModes[selectedCmdInd][1] == "resume":
                    return False
                elif cmdModes[selectedCmdInd][1] == "reset Pos":
                    editingDataMoney = [0, editingDataMoney[1]]
                    return False
                elif cmdModes[selectedCmdInd][1] == "reset Cost":
                    editingDataMoney = [editingDataMoney[0], 0]
                    return False
                elif cmdModes[selectedCmdInd][1] == "remove":
                    cmd = inquirer.prompt([inquirer.List("cmd", message=f"Are you sure?",
                                                         choices=["yes", "no"], default="no")])["cmd"]
                    if cmd == "yes":
                        cmd = inquirer.prompt([inquirer.List("cmd", message=f"This data will be removed? (cannot undo)",
                                                             choices=["YESSSS", "no..."], default="no...")])["cmd"]
                        if cmd == "YESSSS":
                            editingDataMoney = None
                            dataMan.deleteData(editDaySelected)
                            printRed(f"\t{editDaySelected} deleted...")
                            time.sleep(2)
                            return True
                        else:
                            return False
                    else:
                        return False
                elif cmdModes[selectedCmdInd][1] == "cancel":
                    strRevert = "(revert to NO DATA)"
                    if editDaySelected in moneyData:
                        strRevert = f"(revert to +{moneyData[editDaySelected][0]}$ -{moneyData[editDaySelected][1]}$)"

                    cmd = inquirer.prompt([inquirer.List("cmd", message=f"Are you sure? (the edit data will be lost) {strRevert}",
                                                         choices=["yes", "no"])])["cmd"]
                    if cmd == "yes":
                        editingDataMoney = None
                        return True
                    else:
                        return False
                elif cmdModes[selectedCmdInd][1] == "save":
                    return True

            elif keyInput == key.ESC:
                inputMode = "money"
                strMoney = ""
            elif keyInput in "0123456789.+-":
                inputMode = "money"
                strMoney = keyInput

        # ? reset
        moveCursor(left=9999)
        if pInputMode == "cmd":
            moveCursor(up=len(cmdModes) + 1)
        clearAfterCursor()

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

        pInputMode = inputMode


def screen():
    global editingDataMoney
    moneyData = dataMan.getMoneyData()
    thisTime = time.localtime(time.time())
    selectedYear = thisTime.tm_year
    selectedMonth = thisTime.tm_mon
    selectedDay = thisTime.tm_mday
    maxDay = getDaysInMonth(selectedYear, selectedMonth)

    DISPLAY_COLUMNS_CHOICE = max(
        min(os.get_terminal_size().lines - 13, maxDay), 7)

    print(paintTextFormat("Edit or Insert Day",
          "\033[38;5;39m", bold=True, underline=True), "\n")

    firstTime = True

    while True:

        if not firstTime:
            thisKey = readkey()
            # ? reset
            moveCursor(up=10 + DISPLAY_COLUMNS_CHOICE)
            clearAfterCursor()

            # ? process
            if thisKey == key.LEFT:
                selectedMonth -= 1
                maxDay = getDaysInMonth(selectedYear, selectedMonth)
                selectedDay = 1
                if selectedMonth == 0:
                    selectedMonth = 12
                    selectedYear -= 1

            elif thisKey == key.RIGHT:
                selectedMonth += 1
                maxDay = getDaysInMonth(selectedYear, selectedMonth)
                selectedDay = 1
                if selectedMonth == 13:
                    selectedMonth = 1
                    selectedYear += 1

            elif thisKey == key.UP:
                if selectedDay != 1:
                    selectedDay -= 1

            elif thisKey == key.DOWN:

                if selectedDay != maxDay:
                    selectedDay += 1

            elif thisKey == key.ESC:
                return "main"

            elif thisKey == key.ENTER:
                editingDataMoney = None
                editDaySelected = f"{selectedYear}-{selectedMonth:02d}-{selectedDay:02d}"
                if editDaySelected in moneyData:
                    editingDataMoney = moneyData[editDaySelected]
                while True:
                    isComplete = editDay(editDaySelected)
                    if isComplete:
                        if editingDataMoney != None:
                            dataMan.resetData(
                                editDaySelected, pos=True, neg=True)
                            dataMan.insertOrModify(
                                editDaySelected, editingDataMoney[0])
                            dataMan.insertOrModify(
                                editDaySelected, -editingDataMoney[1])
                        break
                return "main"

        # ? output
        # ? month row
        printYellow("\t\t<\t", end="")
        printMagenta(
            f"{monthNumToStr(selectedMonth)} {selectedYear}", bold=True, end="")
        printYellow("\t>")
        print("\n")

        printYellow("\t\t\t^")
        if selectedDay <= DISPLAY_COLUMNS_CHOICE//2:
            rangeDisplay = range(1, DISPLAY_COLUMNS_CHOICE + 1)
        elif selectedDay >= maxDay-DISPLAY_COLUMNS_CHOICE//2:
            rangeDisplay = range(maxDay-DISPLAY_COLUMNS_CHOICE+1, maxDay+1)
        else:
            rangeDisplay = range(selectedDay-DISPLAY_COLUMNS_CHOICE//2,
                                 (selectedDay-DISPLAY_COLUMNS_CHOICE//2) + DISPLAY_COLUMNS_CHOICE)

        for i in rangeDisplay:
            # ?'2022-07-02'
            dateStrKey = f"{selectedYear}-{selectedMonth:02d}-{i:02d}"
            displayDate = f"{getDayOfWeekStr(selectedYear, selectedMonth, i)} {i}{getSuffixNumberOrder(i)}"
            compareWithToday = compareDate(
                i, selectedMonth, selectedYear, thisTime.tm_mday, thisTime.tm_mon, thisTime.tm_year)
            isThisSelectedChoice = (i == selectedDay)

            if dateStrKey in moneyData:
                displayChoice = f"{displayDate}\t+{moneyData[dateStrKey][0]}$\t-{moneyData[dateStrKey][1]}$"
            else:
                if compareWithToday != 1:
                    displayChoice = f"{displayDate} (no data)"
                else:
                    displayChoice = f"{displayDate}"

            if isThisSelectedChoice:
                displayChoice = f"\t[\t{displayChoice}\t]"
            else:
                displayChoice = f"\t\t{displayChoice}"

            if dateStrKey in moneyData:
                printMagenta(displayChoice,
                             bold=(isThisSelectedChoice))
            else:

                if compareWithToday == 0:  # ? today
                    printBlue(displayChoice,
                              bold=(isThisSelectedChoice))
                elif compareWithToday == 1:  # ? future
                    printGrey(displayChoice, bold=(
                        isThisSelectedChoice), italic=(i != selectedDay))
                else:  # ? past
                    printStyle(displayChoice,
                               bold=(isThisSelectedChoice))
        printYellow("\t\t\tv\n")

        print("use", paintTextFormat("arrow key",
              ANSIColorCode.YELLOW), "to select day")
        print("press", paintTextFormat("enter", ANSIColorCode.GREEN), "to edit")
        print("press ", paintTextFormat(
            "esc", ANSIColorCode.RED), " to back to main menu")

        firstTime = False
