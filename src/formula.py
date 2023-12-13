def get_item_of_list_by_class(lst: tuple, clazz):
    for item in lst:
        if (type(item) == clazz):
            return item

class FormelSymbol:
    aliases = []
    description = ""
    symbol = ""
    
    def formula() -> str:
        return FormelSymbol.symbol()
    
    def __calculateValue(self, symbols:list)->float:
        pass
    
    def __init__(self, value:float=None, symbols:tuple=()):
        self.symbol = type(__class__).__name__
        if (value != None):
            self.value = value
        else:
            self.value = self.__calculateValue(symbols)
    
    @classmethod
    def get_description(cls):
        return f"${cls.symbol()}$ = {cls.description}"

class r_E(FormelSymbol):
    pass

class EPercent(FormelSymbol):
    symbol = 'E%'
    pass

class r_pfd(FormelSymbol):
    pass
    
class PPercent(FormelSymbol):
    symbol = 'P%'
    
class r_D(FormelSymbol):
    symbol = "r_{D}"
    
class T_C(FormelSymbol):
    symbol = "T_{C}"

class DPercent(FormelSymbol):
    symbol = 'D%'


class WACC(FormelSymbol):
    symbol = 'r_{wacc}'
    aliases = ['wacc', '(WeightedAssetCostOfCapital)']
    description = "Weighted Asset Cost of Capital"
    
    def __init__(self, value: float = None, symbols: tuple = ()):
        if (value != None):
            self.value = value
        else:
            self.value = self.__calculateValue(symbols)
    
    def __calculateValue(self, symbols:tuple) -> float:
        rE = get_item_of_list_by_class(symbols, r_E)
        epct = get_item_of_list_by_class(symbols, EPercent)
        rpfd = get_item_of_list_by_class(symbols, r_pfd)
        ppct = get_item_of_list_by_class(symbols, PPercent)
        rd = get_item_of_list_by_class(symbols, r_D)
        tc = get_item_of_list_by_class(symbols, T_C)
        dpct = get_item_of_list_by_class(symbols, DPercent)
        return rE.value*epct.value + rpfd.value*ppct.value + rd.value*(1-tc.value)*dpct.value
    


class RiskFreeRate(FormelSymbol):
    def symbol():return 'r_\\$'

class StockRateOfReturn(FormelSymbol):
    def symbol():return 'r_{stockRateOfReturn}'

class MarketRateOfReturn(FormelSymbol):
    def symbol():return 'r_{marketRateOfReturn}'

class Beta(FormelSymbol):
    def symbol():return '\\beta'
    
    def __calculateValue(self, symbols: list):
        riskfreeRate = get_item_of_list_by_class(symbols, RiskFreeRate)
        stockRateOfReturn = get_item_of_list_by_class(symbols, StockRateOfReturn)
        marketRateOfReturn = get_item_of_list_by_class(symbols, MarketRateOfReturn)
        return (stockRateOfReturn - riskfreeRate) / (marketRateOfReturn - riskfreeRate)
    
    def formula() -> str:
        return "\\beta =\\frac{"+  StockRateOfReturn.symbol()+" - "+RiskFreeRate.symbol() +"}{"+MarketRateOfReturn.symbol()+"-"+RiskFreeRate.symbol()+"}"


def show_formula(formula:FormelSymbol):
    from IPython.display import Latex, display
    display(Latex("$"+formula.formula()+"$"))
    

class Mean(FormelSymbol):
    symbol = 'mean'
    
    def __init__(self, value: float = None, value_list: list[float] = []):
        self.value = self.__calculateValue(value_list)
    
    def __calculateValue(self, values: list) -> float:
        sum = 0
        for value in values:
            sum += value
        return sum / len(values)
    
class Variance(FormelSymbol):
    symbol = 'variance'
    aliases = ['std']
    description = 'Std. Variance of List'
    
    def __init__(self, value: float = None, value_list: list[float] = []):
        super().__init__(value, symbols)
    
    def __calculateValue(self, value_list:list[float]) -> float:
        sum = 0
        mean = Mean(value_list=value_list)
        # calculate standard variance of value_list 
        for value in value_list:
            sum += (value - mean.value)**2
        return sum / len(value_list)

class Covariance(FormelSymbol):
    symbol = 'covariance'
    aliases = ['cov']
    description = 'Covariance of two Lists'
    
    def __init__(self, value: float = None, values1:list=[], values2:list=[]):
        if (value != None):
            self.value = value
        else:
            self.value = self.__calculateValue(values1, values2)
        
    def __calculateValue(self, values1: list, values2:list) -> float:
        sum = 0
        mean1 = Mean(value_list=values1)
        mean2 = Mean(value_list=values2)
        for i in range(len(values1)):
            sum += (values1[i] - mean1.value)*(values2[i] - mean2.value)
        return sum / len(values1)
            
        
        

if __name__ == '__main__':
    symbols=(r_E(0.126), EPercent(53.24/67.541), r_pfd(0.0408), PPercent(221/67541),r_D(0.0281),T_C(0.35), DPercent(14.08/67.541))
    wacc = WACC(symbols=symbols)
    print('Result', wacc.value)