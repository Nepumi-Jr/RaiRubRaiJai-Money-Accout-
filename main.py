import os
import yaml
import time
from msvcrt import getch

from message import *

moneyData = {}
screen = "main"
editIndex = -1
dayIndex = 0
editDaySelected = ""


def loadData():
    global moneyData
    if os.path.exists("data.yml"):
        with open("data.yml", "r") as f:
            moneyData = yaml.load(f, Loader=yaml.FullLoader)

    if not isinstance(moneyData, dict):
        moneyData = {}


def saveData():
    with open("data.yml", "w") as f:
        yaml.dump(moneyData, f)


def isInt(strContent):
    try:
        int(strContent)
        return True
    except:
        return False


def monthNumToStr(numMonth):
    months = ["???", "Jan", "Feb", "Mar", "Apr", "May",
              "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[numMonth]


def parseNumFromStr(strContent: str, nNum: int = 1):
    nums = []
    l = 0
    while l < len(strContent):
        if strContent[l].isdigit() or strContent[l] == "-":
            lastR = l
            for r in range(l + 1, len(strContent)):
                if isInt(strContent[l:(r + 1)]):
                    lastR = r
                else:
                    break
            nums.append(int(strContent[l:(lastR + 1)]))
            l = lastR + 1
        else:
            l += 1

    if len(nums) > nNum:
        nums = nums[:nNum]

    if len(nums) == 1:
        return nums[0]

    return nums


def mainScreen():
    global screen, moneyData, editIndex, dayIndex
    loadData()

    thisTime = time.localtime(time.time())
    sumMoney = 0
    for eachDay in moneyData:
        sumMoney += moneyData[eachDay]

    printBold("\nMONEY SUMMARY...")
    if sumMoney >= 200:
        printGreen("\t->", sumMoney, "Baht")
    elif sumMoney >= 0:
        printYellow("\t->", sumMoney, "Baht")
    else:
        printRed("\t->", sumMoney, "Baht")

    # ? Monthly Summary
    sumMoney = 0
    print("\n")
    printBold("MONTHLY SUMMARY...")
    prefixYearMonth = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}"
    for day in moneyData:
        if day.startswith(prefixYearMonth):
            sumMoney += moneyData[day]

    printMagenta("  [", monthNumToStr(thisTime.tm_mon), thisTime.tm_year, "]")
    if sumMoney >= 200:
        printGreen("\t->", sumMoney, "Baht")
    elif sumMoney >= 0:
        printYellow("\t->", sumMoney, "Baht")
    else:
        printRed("\t->", sumMoney, "Baht")

    todayStr = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}-{thisTime.tm_mday:02d}"

    printBold("\nTODAY'S MONEY...")
    if todayStr in moneyData:
        if moneyData[todayStr] >= 0:
            printGreen("\t  ", moneyData[todayStr], "Baht")
        else:
            printRed("\t  ", moneyData[todayStr], "Baht")
    else:
        printYellow("\t  ", "No data")

    print("\n")
    printBold("Last 7 days...")
    allDay = list(moneyData.keys())
    sorted(allDay, reverse=True)
    for eachDay in allDay[:-7:-1]:
        if moneyData[eachDay] >= 0:
            printGreen("\t", eachDay, ":", moneyData[eachDay], "Baht")
        else:
            printRed("\t", eachDay, ":", moneyData[eachDay], "Baht")

    print("\n")
    print("'edit' for edit money data")
    print("'insert' for insert new money data")
    print()
    print("'exit' for exit")

    inputCmd = input("Enter money or command : ").strip().lower()
    allNums = parseNumFromStr(inputCmd)
    if isinstance(allNums, list):
        # ? cmd
        if inputCmd.startswith("ed"):
            screen = "edit"
            editIndex = -1
            dayIndex = 0
        elif inputCmd.startswith("ex"):
            exit(0)
        elif inputCmd.startswith("i"):
            screen = "insert"
            dayIndex = 0
    else:
        newMoney = allNums

        if todayStr in moneyData:
            moneyData[todayStr] += newMoney
        else:
            moneyData[todayStr] = newMoney

        saveData()


def edit():
    global screen, moneyData, editIndex, dayIndex, editDaySelected
    allMonth = set()
    for eachDay in moneyData:
        dayData = eachDay.split("-")
        allMonth.add("-".join(dayData[:2]))
    allMonth = sorted(list(allMonth))

    if editIndex > len(allMonth) or editIndex < 0:
        thisTime = time.localtime(time.time())
        thisMonth = f"{thisTime.tm_year}-{thisTime.tm_mon:02d}"
        if thisMonth in allMonth:
            editIndex = allMonth.index(thisMonth)
        else:
            editIndex = len(allMonth) - 1

    dayInMonth = []
    for eachDay in moneyData:
        dayData = eachDay.split("-")
        if dayData[:2] == allMonth[editIndex].split("-"):
            dayInMonth.append(eachDay)
    dayInMonth = sorted(dayInMonth)

    printBold("\nEDIT MONEY DATA...")
    printBold(" <   ", allMonth[editIndex], "   >")
    for i, eachDay in enumerate(dayInMonth):

        if i == dayIndex:
            printYellow(" [", eachDay, "is", moneyData[eachDay], "Baht ]")
        else:
            print("  ", eachDay, "is", moneyData[eachDay], "Baht")

    if dayIndex == len(dayInMonth):
        printBlue("  [Done]")
    else:
        print("  -Done-")

    print("\n\n")
    print("Use 'A' and 'D' to change month")
    print("Use 'W' and 'S' to change day")
    print("Use 'Enter' to Select")
    key = ord(getch())

    if key != 13 and key != 27:
        try:
            keyChar = chr(key).upper()
        except:
            return

    if key == 13:
        # ? Enter
        if dayIndex == len(dayInMonth):
            screen = "main"
        else:
            screen = "editDay"
            editDaySelected = dayInMonth[dayIndex]
    elif key == 27:
        # ? ESC
        screen = "main"
    elif keyChar == 'A':
        editIndex = max(editIndex - 1, 0)
    elif keyChar == 'D':
        editIndex = min(editIndex + 1, len(allMonth) - 1)
    elif keyChar == 'W':
        dayIndex = max(dayIndex - 1, 0)
    elif keyChar == 'S':
        dayIndex = min(dayIndex + 1, len(dayInMonth))


def editDay():
    global moneyData, editDaySelected, screen
    printBold("EDIT DAY", editDaySelected)
    if moneyData[editDaySelected] >= 0:
        printGreen("\t", moneyData[editDaySelected], "Baht")
    else:
        printRed("\t", moneyData[editDaySelected], "Baht")

    print("\n")
    newData = input("Enter new data : ").strip()

    if newData == "":
        cmd = input("'Z'ero or 'D'elete : ")
        if cmd.upper() == "Z":
            moneyData[editDaySelected] = 0
            saveData()
        elif cmd.upper() == "D":
            del moneyData[editDaySelected]
            saveData()
        screen = "main"
        return

    try:
        newData = int(newData)
    except:
        return

    moneyData[editDaySelected] = newData
    saveData()
    screen = "main"


def getDaysInMonth(year, month):
    if month == 2:
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    # ? leap year
                    return 29
                else:
                    return 28
            else:
                # ? leap year
                return 29
        else:
            return 28

    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31


customSelectDay = 1
customSelectMonth = 1
customSelectYear = 1


def insert():
    global screen, moneyData, dayIndex, editDaySelected, customSelectDay, customSelectMonth, customSelectYear

    thisMonth = time.localtime(time.time()).tm_mon
    thisYear = time.localtime(time.time()).tm_year
    thisDay = time.localtime(time.time()).tm_mday
    thisMonthDaysStart = min(getDaysInMonth(thisYear, thisMonth), thisDay)
    suggestDates = []
    for day in range(thisMonthDaysStart, 0, -1):
        dayStr = f"{thisYear}-{thisMonth:02d}-{day:02d}"
        if dayStr not in moneyData:
            suggestDates.append(dayStr)

    printBold("\nINSERT NEW MONEY DATA...")
    print("\n")
    printMagenta("Suggested date : ")
    for i, eachDay in enumerate(suggestDates):
        if i == dayIndex:
            printYellow(" [", eachDay, "]")
        else:
            print("  ", eachDay)
    print("\n")

    if dayIndex == len(suggestDates):
        printBlue("  [Custom Insert]")
    else:
        print("  -Custom Insert-")

    if dayIndex == len(suggestDates) + 1:
        printBlue("  [Done]")
    else:
        print("  -Done-")

    print("Use 'W' and 'S' to Move Up and Down")
    print("Use 'Enter' to Select")
    key = ord(getch())

    if key != 13 and key != 27:
        try:
            keyChar = chr(key).upper()
        except:
            return

    if key == 13:
        # ? Enter
        if dayIndex == len(suggestDates):
            screen = "insertSelectCustom"
            customSelectDay = thisDay
            customSelectMonth = thisMonth
            customSelectYear = thisYear
            dayIndex = 0

        elif dayIndex == len(suggestDates) + 1:
            screen = "main"
        else:
            screen = "editDay"
            editDaySelected = suggestDates[dayIndex]
            moneyData[editDaySelected] = 0
    elif key == 27:
        # ? ESC
        screen = "main"
    elif keyChar == 'W':
        dayIndex = max(dayIndex - 1, 0)
    elif keyChar == 'S':
        dayIndex = min(dayIndex + 1, len(suggestDates) + 1)


def insertSelectCustom():
    global screen, moneyData, dayIndex, editDaySelected, customSelectDay, customSelectMonth, customSelectYear

    customSelectDay = min(customSelectDay, getDaysInMonth(
        customSelectYear, customSelectMonth))

    printBold("Select Custom Date")
    print("\n\n")
    printBlue("  DAY  MONTH  YEAR")

    # ? Arrow
    if dayIndex == 0:
        # ?             DAY  MONTH  YEAR
        printMagenta("   ^              ")
    elif dayIndex == 1:
        # ?             DAY  MONTH  YEAR
        printMagenta("         ^         ")
    elif dayIndex == 2:
        # ?             DAY  MONTH  YEAR
        printMagenta("                ^  ")

    # ? Number
    print("  ", end="")
    if dayIndex == 0:
        printMagenta(f"{customSelectDay:02d}", end="")
        print(f"    {customSelectMonth:02d}", end="")
        print(f"    {customSelectYear:04d}")
    elif dayIndex == 1:
        print(f"{customSelectDay:02d}", end="")
        printMagenta(f"    {customSelectMonth:02d}", end="")
        print(f"    {customSelectYear:04d}")
    elif dayIndex == 2:
        print(f"{customSelectDay:02d}", end="")
        print(f"    {customSelectMonth:02d}", end="")
        printMagenta(f"    {customSelectYear:04d}")

    # ? Arrow
    if dayIndex == 0:
        # ?             DAY  MONTH  YEAR
        printMagenta("   v              ")
    elif dayIndex == 1:
        # ?             DAY  MONTH  YEAR
        printMagenta("         v         ")
    elif dayIndex == 2:
        # ?             DAY  MONTH  YEAR
        printMagenta("                v  ")

    dayStr = f"{customSelectYear}-{customSelectMonth:02d}-{customSelectDay:02d}"
    if dayStr in moneyData:
        printRed("Can't insert duplicate date!")
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
            screen = "editDay"
            editDaySelected = dayStr
            moneyData[editDaySelected] = 0
    elif key == 27:
        # ? ESC
        screen = "main"
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


if __name__ == "__main__":
    while True:
        os.system("cls")
        if screen == "main":
            mainScreen()
        elif screen == "edit":
            edit()
        elif screen == "editDay":
            editDay()
        elif screen == "insert":
            insert()
        elif screen == "insertSelectCustom":
            insertSelectCustom()
        else:
            printRed("Not implemented yet")
            screen = "main"
            time.sleep(1)
            continue
