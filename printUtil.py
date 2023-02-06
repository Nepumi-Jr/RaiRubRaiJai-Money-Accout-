
class ANSIColorCode:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    GREY = '\u001b[38;5;239m'


def paintTextFormat(msg, ansiColorCode, dim=False, bold=False, italic=False, underline=False) -> str:
    ANSICode = getAnsicode(dim, bold, italic, underline) + ansiColorCode
    return ANSICode + msg + '\033[0m'


def getAnsicode(dim, bold, italic, underline) -> str:
    result = ""
    if bold:
        result += "\033[1m"
    if italic:
        result += "\033[3m"
    if underline:
        result += "\033[4m"
    if dim:
        result += "\033[2m"

    return result


def printRed(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, ANSIColorCode.RED,
                          dim, bold, italic, underline), **kwargs)


def printGreen(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, ANSIColorCode.GREEN,
                          dim, bold, italic, underline), **kwargs)


def printYellow(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, ANSIColorCode.YELLOW,
                          dim, bold, italic, underline), **kwargs)


def printBlue(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, ANSIColorCode.BLUE,
                          dim, bold, italic, underline), **kwargs)


def printMagenta(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, ANSIColorCode.MAGENTA,
                          dim, bold, italic, underline), **kwargs)


def printStyle(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, "",
                          dim, bold, italic, underline), **kwargs)


def printGrey(msg, bold: bool = False, italic: bool = False, underline: bool = False, dim: bool = False, **kwargs):
    print(paintTextFormat(msg, ANSIColorCode.GREY,
                          dim, bold, italic, underline), **kwargs)


if __name__ == "__main__":
    printRed("Hello World", bold=True, underline=True)
    print("next")
    printGreen("Hello World", bold=True)
    print("next")
    printStyle("Hello World", italic=True)
    print("next")
    printStyle("Hello World", dim=True)
    print("next")
    printGrey("Hello World")
    print("ended")

    print(paintTextFormat("BIG Hello World",
          "\033[38;5;39m", bold=True, underline=True))  # ? big green or blue
