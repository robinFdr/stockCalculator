import math


class Stock:
    def __init__(self, basePrice: float, sellingPrice: float, transactionCost: float = 2.0):
        self.basePrice = basePrice
        self.transactionCost = transactionCost
        self.estimatedEarningsPerStock = sellingPrice - basePrice

    def estimatedEarningsForNumberOfStocks(self, number: int):
        return number*self.estimatedEarningsPerStock - self.transactionCost
    
    def breakEvenStocksNumber(self):
        return math.ceil(self.transactionCost / self.estimatedEarningsPerStock)
    
    def breakEvenPrice(self):
        return self.basePrice * self.breakEvenStocksNumber()
    
    def numberOfStocksToBuyForEarning(self, earnings: float):
        return math.ceil(self.transactionCost / self.estimatedEarningsPerStock + earnings / self.estimatedEarningsPerStock)
    
    def costOfStocksToBuyForEarning(self, earnings: float):
        return self.numberOfStocksToBuyForEarning(earnings=earnings)*self.basePrice
    
    def __str__(self):
        return "BasePrice: " + str(self.basePrice) + "\nEstimated Earnings per Stock: "+ str(self.estimatedEarningsPerStock) +"\nBreakEven Stocknumber: " + str(self.breakEvenStocksNumber()) + "\nBreakEven Price: " + str(self.breakEvenPrice())
