import moneyLabelManager as label


class MoneyData():
    amount: int = 0
    labelID: int = 0

    def __init__(self, amount: int = 0, labelID: int = 0):
        self.amount = amount
        self.labelID = labelID

    def isIncome(self):
        return self.amount >= 0

    def getLabel(self):
        if self.isIncome():
            return label.getIncomeLabel(self.labelID)
        else:
            return label.getCostLabel(self.labelID)

    def __str__(self):
        return f"{self.getLabel()} : {self.amount}"


if __name__ == '__main__':
    testData = [
        MoneyData(69, 0),
        MoneyData(42, 1),
        MoneyData(-420, 1),
        MoneyData(-42, 999)
    ]
    for data in testData:
        print(data)

    # ? test dump to yaml
    import yaml
    print(yaml.dump(testData))

    # ? test load from yaml
    print(">>>>", yaml.load(yaml.dump(testData), Loader=yaml.Loader))
