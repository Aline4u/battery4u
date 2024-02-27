class Battery:
    def __init__(self, url, brand, capacityMAh, voltage, price, model=None):
        self.url = url
        self.brand = brand
        self.capacityMAh = capacityMAh
        self.voltage = voltage
        self.price = price
        self.model = model
        self.reqVoltage = float(51.2)
        self.KwHcost = getKwHcost(self.price, self.capacityMAh, self.voltage)
        self.minCost = getMinCost(self.price, self.voltage)
        self.kw4MinCost = self.reqVoltage * (self.capacityMAh / 1000) / 1000

def getKwHcost(priceIn, capacity, voltage: float, NumCells4ReqVoltage: float):
    capacity_Ah: float = self.capacity/1000
    price = float(priceIn)
    voltagePrice = NumCells4ReqVoltage * price
    actKwh = NumCells4ReqVoltage * float(voltage) * float(capacity_Ah / 1000)
    act1Kwh = 1 / actKwh
    cost4ReqKw = act1Kwh * voltagePrice
    return float(cost4ReqKw)


def getMinCost(price, voltage):
    numCells4ReqVolt = ceil(reqVoltage / float(voltage))
    return numCells4ReqVolt * float(price)


