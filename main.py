import os
import time
from util import *
from printUtil import *

from pages.main import screen as mainScreen
from pages.edit import screen as editScreen

if __name__ == "__main__":
    funcCallMapper = {
        "main": mainScreen,
        "edit": editScreen
    }
    screen = "main"
    while True:
        os.system("cls")

        if "main" not in funcCallMapper:
            printRed("Error: main screen not found")
            exit(69)

        if screen not in funcCallMapper:
            printRed("Invalid screen")
            screen = "main"
            time.sleep(1)
            continue

        screen = funcCallMapper[screen]()
