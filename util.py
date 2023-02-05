def isInt(strContent):
    try:
        int(strContent)
        return True
    except:
        return False


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
            if isInt(strContent[l:(lastR + 1)]):
                nums.append(int(strContent[l:(lastR + 1)]))
            l = lastR + 1
        else:
            l += 1

    if len(nums) > nNum:
        nums = nums[:nNum]

    if len(nums) == 1:
        return nums[0]

    return nums


def monthNumToStr(numMonth):
    months = ["???", "Jan", "Feb", "Mar", "Apr", "May",
              "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[numMonth]


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


def moveCursor(left=0, down=0, up=0, right=0):
    print("\033[{}A".format(up), end="")
    print("\033[{}B".format(down), end="")
    print("\033[{}C".format(right), end="")
    print("\033[{}D".format(left), end="", flush=True)
