import datetime


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


def dayOfWeekNumToStr(numDay):
    days = ["???", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return days[numDay]


def getDayOfWeek(year, month, day):
    return datetime.date(year, month, day).weekday() + 1


def getDayOfWeekStr(year, month, day):
    return dayOfWeekNumToStr(getDayOfWeek(year, month, day))


def getSuffixNumberOrder(num):
    if num % 100 in [11, 12, 13]:
        return "th"
    else:
        if num % 10 == 1:
            return "st"
        elif num % 10 == 2:
            return "nd"
        elif num % 10 == 3:
            return "rd"
        else:
            return "th"


def getFullDateStr(day, month, year):
    return "{} {}{} {} {}".format(dayOfWeekNumToStr(getDayOfWeek(year, month, day)), day, getSuffixNumberOrder(day), monthNumToStr(month), year)


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


def clearAfterCursor():
    print("\033[J", end="", flush=True)


def compareDate(day1, month1, year1, day2, month2, year2):
    if year1 > year2:
        return 1
    elif year1 < year2:
        return -1
    else:
        if month1 > month2:
            return 1
        elif month1 < month2:
            return -1
        else:
            if day1 > day2:
                return 1
            elif day1 < day2:
                return -1
            else:
                return 0
