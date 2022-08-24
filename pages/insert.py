import time
from util import *
import dataManager as dataMan
import chalk
import inquirer
from msvcrt import getch
from pages.edit import editDay
import os


def selectDayCustom():
    moneyData = dataMan.getMoneyData()
    customSelectDay = time.localtime(time.time()).tm_mday
    customSelectMonth = time.localtime(time.time()).tm_mon
    customSelectYear = time.localtime(time.time()).tm_year
    dayIndex = 0

    while True:
        os.system("cls")

        customSelectDay = min(customSelectDay, getDaysInMonth(
            customSelectYear, customSelectMonth))

        print(chalk.white("Select Custom Date", bold=True))
        print("\n\n")
        print("  " + chalk.blue("DAY", underline=True) + "  "
              + chalk.blue("MONTH", underline=True) + "  "
              + chalk.blue("YEAR", underline=True))

        # ? Arrow
        if dayIndex == 0:
            # ?                    DAY  MONTH  YEAR
            print(chalk.magenta("   ^              "))
        elif dayIndex == 1:
            # ?                    DAY  MONTH  YEAR
            print(chalk.magenta("         ^         "))
        elif dayIndex == 2:
            # ?                    DAY  MONTH  YEAR
            print(chalk.magenta("                ^  "))

        # ? Number
        print("  ", end="")
        if dayIndex == 0:
            print(chalk.magenta(f"{customSelectDay:02d}", bold=True), end="")
            print(f"    {customSelectMonth:02d}", end="")
            print(f"    {customSelectYear:04d}")
        elif dayIndex == 1:
            print(f"{customSelectDay:02d}", end="")
            print(chalk.magenta(
                f"    {customSelectMonth:02d}", bold=True), end="")
            print(f"    {customSelectYear:04d}")
        elif dayIndex == 2:
            print(f"{customSelectDay:02d}", end="")
            print(f"    {customSelectMonth:02d}", end="")
            print(chalk.magenta(f"    {customSelectYear:04d}", bold=True))

        # ? Arrow
        if dayIndex == 0:
            # ?                    DAY  MONTH  YEAR
            print(chalk.magenta("   v              "))
        elif dayIndex == 1:
            # ?                    DAY  MONTH  YEAR
            print(chalk.magenta("         v         "))
        elif dayIndex == 2:
            # ?                    DAY  MONTH  YEAR
            print(chalk.magenta("                v  "))

        dayStr = f"{customSelectYear}-{customSelectMonth:02d}-{customSelectDay:02d}"
        if dayStr in moneyData:
            print(chalk.red("Can't insert duplicate date!"))
        else:
            print()
        print("\n")

        print("Use 'A' and 'S' to Move Left and Right")
        print("Use 'W' and 'S' to Move Up and Down (change date)")
        print("Use 'Enter' to Select")
        key = ord(getch())

        if key != 13 and key != 27:
            try:
                keyChar = chr(key).upper()
            except:
                return

        if key == 13:
            # ? Enter
            if dayStr not in moneyData:
                return dayStr

        elif key == 27:
            # ? ESC
            return None
        elif keyChar == 'W':
            if dayIndex == 0:
                customSelectDay = min(customSelectDay + 1, 31)
            elif dayIndex == 1:
                customSelectMonth = min(customSelectMonth + 1, 12)
            elif dayIndex == 2:
                customSelectYear = min(customSelectYear + 1, 9999)
        elif keyChar == 'S':
            if dayIndex == 0:
                customSelectDay = max(customSelectDay - 1, 1)
            elif dayIndex == 1:
                customSelectMonth = max(customSelectMonth - 1, 1)
            elif dayIndex == 2:
                customSelectYear = max(customSelectYear - 1, 1)
        elif keyChar == 'A':
            dayIndex = max(dayIndex - 1, 0)
        elif keyChar == 'D':
            dayIndex = min(dayIndex + 1, 2)


def screen():

    moneyData = dataMan.getMoneyData()

    thisMonth = time.localtime(time.time()).tm_mon
    thisYear = time.localtime(time.time()).tm_year
    thisDay = time.localtime(time.time()).tm_mday
    thisMonthDaysStart = min(getDaysInMonth(thisYear, thisMonth), thisDay)
    suggestDates = []
    for day in range(thisMonthDaysStart, 0, -1):
        dayStr = f"{thisYear}-{thisMonth:02d}-{day:02d}"
        if dayStr not in moneyData:
            suggestDates.append(dayStr)

    print(chalk.white("INSERT NEW MONEY DATA...", bold=True))
    print("\n")
    print(chalk.magenta("Select date"))
    selectedDay = inquirer.prompt([inquirer.List(
        "day", message="Select day", choices=suggestDates + ["Custom Insert", "Done"])])["day"]

    if selectedDay == "Done":
        return "main"

    if selectedDay == "Custom Insert":
        selectedDay = selectDayCustom()

        if selectedDay == None:
            return "main"

    editDay(selectedDay)
    return "main"
