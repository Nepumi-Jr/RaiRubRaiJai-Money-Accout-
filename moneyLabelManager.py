import configparser

theConfig = configparser.ConfigParser()
theConfig.read('moneyLabel.ini', encoding='utf-8')


class MoneyLabel:
    label: str = None  # Only one character
    description: str = None  # The description of the label

    def __init__(self, label: str = None, description: str = None):
        self.label = label
        self.description = description

    def __str__(self):
        return f"[{self.label}] {self.description}"


def getIncomeLabel(id: int):
    if str(id) not in theConfig['income']:
        return MoneyLabel("❓", "Unknown")
    data = theConfig['income'][str(id)].strip()
    return MoneyLabel(data[0], data[1:].strip())


def getCostLabel(id: int):
    if str(id) not in theConfig['cost']:
        return MoneyLabel("❓", "Unknown")
    data = theConfig['cost'][str(id)].strip()
    return MoneyLabel(data[0], data[1:].strip())


def getLabel(isIncome: bool, id: int):
    if isIncome:
        return getIncomeLabel(id)
    else:
        return getCostLabel(id)


def getAllLabelId(isIncome: bool):
    if isIncome:
        return list(map(int, theConfig['income'].keys()))
    else:
        return list(map(int, theConfig['cost'].keys()))


if __name__ == '__main__':
    print(getIncomeLabel(69))
