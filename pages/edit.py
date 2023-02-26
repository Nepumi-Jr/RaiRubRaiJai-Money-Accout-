from readchar import key, readkey
import dataManager as dataMan
import time
import os
import inquirer
from math import log10

import moneyDataModel as mData
import moneyLabelManager as label

from util import *
from printUtil import *

editingDataMoney = None


def editDay(editDaySelected: str):
    global editingDataMoney
    os.system("cls")

    moneyData = dataMan.getMoneyData()

    print(paintTextFormat(f"Edit {editDaySelected}",
          "\033[38;5;39m", bold=True, underline=True), "\n")

    if editDaySelected not in moneyData:
        printYellow("\t No data")
    else:
        incomeToday = 0
        costToday = 0
        for e in moneyData[editDaySelected]:
            if e.isIncome():
                incomeToday += e.amount
            else:
                costToday += e.amount
        sp2 = " "*max(0, (6 - int(log10(max(incomeToday, 1)))))
        printGreen(f"\t+{incomeToday}${sp2}", end="")
        printRed(f"{costToday}$")

    print("\n")

    choiceFormats = []
    if editDaySelected in moneyData:
        for i, e in enumerate(moneyData[editDaySelected]):
            choiceFormats.append(f"{i+1}: {e.getLabel()} {e.amount}$")
    choiceFormats.append("Add new")
    choiceFormats.append("Delete all (that day)")
    choiceFormats.append("Done")

    selectedOne = inquirer.prompt([inquirer.List("activity", message=f"Select the Activity",
                                                 choices=choiceFormats)])["activity"]
    if selectedOne == "Done":
        return "main"
    elif selectedOne == "Delete all (that day)":
        isSure = inquirer.prompt(
            [inquirer.Confirm("sure", message=f"Are you sure?")])["sure"]
        if isSure:
            isSure = inquirer.prompt(
                [inquirer.Confirm("sure", message=f"ARE YOU TRULY SURE???")])["sure"]
            if isSure:
                dataMan.deleteDayData(editDaySelected)
        return "main"
    elif selectedOne == "Add new":
        while True:
            try:
                newAmount = int(
                    input(f"Enter the amount : "))
            except:
                pass
            else:
                break

        newMoneyData = mData.MoneyData(newAmount, 0)
        genChoice = []
        for i, e in enumerate(label.getAllLabelId(newMoneyData.isIncome())):
            genChoice.append(
                f"{i+1}: {label.getLabel(newMoneyData.isIncome(), e)}")

        newLabel = inquirer.prompt([inquirer.List("label", message=f"Select the label",
                                                  choices=genChoice)])["label"]

        newLabelID = label.getAllLabelId(newMoneyData.isIncome())[
            int(newLabel.split(":")[0]) - 1]
        dataMan.insert(editDaySelected, newMoneyData.amount, newLabelID)
        return "main"

    selectedIndex = int(selectedOne.split(":")[0]) - 1
    selectedMoneyData = moneyData[editDaySelected][selectedIndex]
    action = inquirer.prompt([inquirer.List("action", message=f"What do you want to do?",
                                            choices=["Edit", "Delete", "Back to menu"])])["action"]
    if action == "Edit":
        while True:
            try:
                newAmount = int(
                    input(f"Enter the new amount : {selectedMoneyData.amount} ->  "))
            except:
                pass
            else:
                break

        newMoneyData = mData.MoneyData(newAmount, 0)
        genChoice = []
        for i, e in enumerate(label.getAllLabelId(newMoneyData.isIncome())):
            genChoice.append(
                f"{i+1}: {label.getLabel(newMoneyData.isIncome(), e)}")

        newLabel = inquirer.prompt([inquirer.List("label", message=f"Select the new label",
                                                  choices=genChoice)])["label"]

        newLabelID = label.getAllLabelId(newMoneyData.isIncome())[
            int(newLabel.split(":")[0]) - 1]
        dataMan.modify(editDaySelected, selectedIndex,
                       newMoneyData.amount, newLabelID)

        return "main"

    elif action == "Delete":
        isSure = inquirer.prompt(
            [inquirer.Confirm("sure", message=f"Are you sure?")])["sure"]
        if isSure:
            dataMan.deleteMoneyData(editDaySelected, selectedIndex)
        return "main"
    elif action == "Back to menu":
        return "main"


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
                editDaySelected = f"{selectedYear}-{selectedMonth:02d}-{selectedDay:02d}"
                return editDay(editDaySelected)

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
                costThatDay, incomeThatDay = 0, 0
                for e in moneyData[dateStrKey]:
                    if e.isIncome():
                        incomeThatDay += e.amount
                    else:
                        costThatDay += e.amount
                sp = " "*(10-len(displayDate))
                sp2 = " "*max(0, (6 - int(log10(max(incomeThatDay, 1)))))
                displayChoice = f"{displayDate}{sp}+{incomeThatDay}${sp2}{costThatDay}$"
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
