
def printGreen(*values, end="\n", sep=" "):

    print(f"\033[92m", end="")
    print(sep.join(map(str, values)), end="")
    print(f"\033[00m", end=end)


def printYellow(*values, end="\n", sep=" "):

    print(f"\033[93m", end="")
    print(sep.join(map(str, values)), end="")
    print(f"\033[00m", end=end)


def printRed(*values, end="\n", sep=" "):

    print(f"\033[91m", end="")
    print(sep.join(map(str, values)), end="")
    print(f"\033[00m", end=end)


def printBold(*values, end="\n", sep=" "):

    print(f"\033[1m", end="")
    print(sep.join(map(str, values)), end="")
    print(f"\033[00m", end=end)


def printBlue(*values, end="\n", sep=" "):

    print(f"\033[94m", end="")
    print(sep.join(map(str, values)), end="")
    print(f"\033[00m", end=end)


def printMagenta(*values, end="\n", sep=" "):

    print(f"\033[95m", end="")
    print(sep.join(map(str, values)), end="")
    print(f"\033[00m", end=end)


if __name__ == "__main__":
    printGreen("Hello", "World", "!")
    printYellow("Hello", "World", "!")
    printRed("Hello", "World", "!")
