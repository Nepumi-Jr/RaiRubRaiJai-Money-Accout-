import tkinter as tk
from tkinter import E, filedialog
import dataManager as dataMan
import moneyLabelManager as label
from util import *
import time
import os


def screen():
    print("Saving at...")
    moneyData = dataMan.getMoneyData()
    saveLocation = filedialog.asksaveasfilename(filetypes=[('csv', "*.csv")])
    if not saveLocation.endswith(".csv"):
        saveLocation += ".csv"
    print(f"exporting to '{saveLocation}' ...")
    print("please wait...", end="")

    csvData = "Description,Income,Expense,Total income,Total Expense\n\n"
    pMonth, pYear = 0, 0
    totalIncome, totalCost = 0, 0
    summary = 0
    for e in sorted(moneyData.keys()):
        year, month, day = map(int, e.split("-"))
        if pMonth != month or pYear != year:
            if pYear != 0:
                summary += totalIncome + totalCost
                csvData += f"Total in this month,,,{totalIncome},{totalCost}\n"
                csvData += f",,,Summary,{summary}\n\n"
                totalIncome, totalCost = 0, 0
            csvData += f"{monthNumToStr(month)} {year},,,,\n"
            pMonth, pYear = month, year

        csvData += f"{getFullDateStr(day, month, year)},,,,\n"
        for ee in moneyData[e]:

            if ee.isIncome():
                if ee.amount != 0:
                    csvData += f"{label.getIncomeLabel(ee.labelID)},{ee.amount},,,\n"
                totalIncome = totalIncome + ee.amount
            else:
                csvData += f"{label.getCostLabel(ee.labelID)},,{ee.amount},,\n"
                totalCost = totalCost + ee.amount

    summary += totalIncome + totalCost
    csvData += f"Total in this month,,,{totalIncome},{totalCost}\n"
    csvData += f"Summary,,,,{summary}\n\n"

    with open(saveLocation, "w", encoding="utf8") as f:
        f.write(csvData)

    os.system(f'explorer /select,"{os.path.realpath(saveLocation)}"')

    print("done")
    print("go back to main screen in 3 seconds...")
    time.sleep(3)

    return "main"
