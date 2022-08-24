import inquirer
import chalk
import dataManager as dataMan
import time
import os


def editDay(editDaySelected: str):
    os.system("cls")

    moneyData = dataMan.getMoneyData()

    if editDaySelected not in moneyData:
        moneyData[editDaySelected] = 0

    print(chalk.white(f"EDIT DAY {editDaySelected}", bold=True))
    if moneyData[editDaySelected] >= 0:
        print(chalk.green(f"\t {moneyData[editDaySelected]} Baht"))
    else:
        print(chalk.red(f"\t {moneyData[editDaySelected]} Baht"))

    print("\n")
    newData = input("Enter new data : ").strip()

    if newData == "":
        cmd = inquirer.prompt([inquirer.List("cmd", message=f"Zero data?",
                                             choices=[f"{editDaySelected} = 0", chalk.red("Delete", bold=True)])])["cmd"]
        if cmd == chalk.red("Delete", bold=True):
            del moneyData[editDaySelected]
            dataMan.saveData()
            print(chalk.red(f"\t{editDaySelected} deleted..."))
            time.sleep(2)
        else:
            moneyData[editDaySelected] = 0
            dataMan.saveData()
        return

    try:
        newData = int(newData)
    except:
        return

    moneyData[editDaySelected] = newData
    dataMan.saveData()


def screen():
    moneyData = dataMan.getMoneyData()

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
        editDay(editDaySelected)
    return "main"
