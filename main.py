import os
import chalk
import time
from util import *

from pages.main import screen as mainScreen
from pages.insert import screen as insertScreen
from pages.edit import screen as editScreen

if __name__ == "__main__":
    funcCallMapper = {
        "main": mainScreen,
        "insert": insertScreen,
        "edit": editScreen
    }
    screen = "main"
    while True:
        os.system("cls")

        if "main" not in funcCallMapper:
            print(chalk.red("Error: main screen not found"))
            exit(69)

        if screen not in funcCallMapper:
            print(chalk.red("Invalid screen"))
            screen = "main"
            time.sleep(1)
            continue

        screen = funcCallMapper[screen]()
