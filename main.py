import os
import yaml
import chalk
import inquirer
import time
from msvcrt import getch


moneyData = {}
screen = "main"
editIndex = -1
dayIndex = 0
editDaySelected = ""


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


def backupData():
    if os.path.exists("data.yml"):
        os.rename("data.yml", "data Backup.yml")


def isHasBackup():
    if os.path.exists("data Backup.yml"):
        return True
    return False


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

    isValidData = isValidFile("data.yml")
    if isValidData != True and isValidData != "File not found":
        backupData()

    if isValidData == True:
        loadData()

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

    if isHasBackup():
        print(chalk.red("\n/!\\ WARNING: Backup file found (data Backup.yml) /!\\"))
        print(
            chalk.red(f"with error message: {isValidFile('data Backup.yml')}"))
        print(chalk.red("Delete 'data Backup.yml' to dismiss this warning"))

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

    selectedMonth = inquirer.prompt([inquirer.List("monthYear", message="Select month",
                                                   choices=allMonth)])["monthYear"]

    dayInMonth = []
    for eachDay in moneyData:
        dayData = eachDay.split("-")
        if dayData[:2] == selectedMonth.split("-"):
            dayInMonth.append(
                f"{eachDay}\t({moneyData[eachDay] < 0 and '-' or '+' } {abs(moneyData[eachDay])})")
    dayInMonth = sorted(dayInMonth)

    selectedDay = inquirer.prompt([inquirer.List("day", message="Select day",
                                                 choices=dayInMonth)])["day"]

    choice = inquirer.prompt([inquirer.List("cmd", message=f"Editing {selectedDay}?",
                                            choices=["Yes", "No (Back to menu)"])])["cmd"]

    if choice == "Yes":
        editDaySelected = selectedDay.split("\t")[0]
        screen = "editDay"
    else:
        screen = "main"


def editDay():
    global moneyData, editDaySelected, screen
    print(chalk.white(f"EDIT DAY {editDaySelected}", bold=True))
    if moneyData[editDaySelected] >= 0:
        print(chalk.green(f"\t {moneyData[editDaySelected]} Baht"))
    else:
        print(chalk.red(f"\t {moneyData[editDaySelected]} Baht"))

    print("\n")
    newData = input("Enter new data : ").strip()

    if newData == "":
        cmd = inquirer.prompt([inquirer.List("cmd", message=f"Zero data?",
                                             choices=[f"{editDaySelected} = 0", "Delete"])])["cmd"]
        if cmd == "Delete":
            del moneyData[editDaySelected]
            saveData()
            print(chalk.red(f"\t{editDaySelected} deleted..."))
            time.sleep(2)
        else:
            moneyData[editDaySelected] = 0
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

    print(chalk.white("INSERT NEW MONEY DATA...", bold=True))
    print("\n")
    print(chalk.magenta("Select date"))
    selectedDay = inquirer.prompt([inquirer.List(
        "day", message="Select day", choices=suggestDates + ["Custom Insert", "Done"])])["day"]

    if selectedDay == "Custom Insert":
        screen = "insertSelectCustom"
        customSelectDay = thisDay
        customSelectMonth = thisMonth
        customSelectYear = thisYear
        dayIndex = 0

    elif selectedDay == "Done":
        screen = "main"
    else:
        screen = "editDay"
        editDaySelected = selectedDay
        moneyData[editDaySelected] = 0


def insertSelectCustom():
    global screen, moneyData, dayIndex, editDaySelected, customSelectDay, customSelectMonth, customSelectYear

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
        print(chalk.magenta(f"{customSelectDay:02d}"), end="")
        print(f"    {customSelectMonth:02d}", end="")
        print(f"    {customSelectYear:04d}")
    elif dayIndex == 1:
        print(f"{customSelectDay:02d}", end="")
        print(f"    {customSelectMonth:02d}", end="")
        print(f"    {customSelectYear:04d}")
    elif dayIndex == 2:
        print(f"{customSelectDay:02d}", end="")
        print(f"    {customSelectMonth:02d}", end="")
        print(f"    {customSelectYear:04d}")

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
            print(chalk.red("ERROR"))
            print(chalk.red("Not implemented yet"))
            screen = "main"
            time.sleep(1)
            continue
