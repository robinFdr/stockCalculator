def get_item_of_list_by_class(lst: tuple, clazz):
    for item in lst:
        if (type(item) == clazz):
            return item

class FormelSymbol:
    aliases = []
    
    def symbol(self) -> str:
        return type(self).__name__
    
    def formula(self) -> str:
        pass
    
    def __calculateValue(self, symbols:list)->float:
        pass
    
    def __init__(self, value:float=None, symbols:tuple=()):
        if (value != None):
            self.value = value
        else:
            self.value = self.__calculateValue(symbols)

class r_E(FormelSymbol):
    pass

class EPercent(FormelSymbol):
    def symbol(self):return 'E%'
    pass

class r_pfd(FormelSymbol):
    pass
    
class PPercent(FormelSymbol):
    def symbol(self):
        return 'P%'
    
class r_D(FormelSymbol):
    pass
    
class T_C(FormelSymbol):
    pass

class DPercent(FormelSymbol):
    def symbol(self) -> str:
        return 'D%'


class WACC(FormelSymbol):
    symbol = 'r_wacc'
    aliases = ['wacc', '(AssetCostOfCapital)']
    
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
    
if __name__ == '__main__':
    symbolz=(r_E(0.126), EPercent(53.24/67.541), r_pfd(0.0408), PPercent(221/67.541),r_D(0.0281),T_C(0.35), DPercent(14.08/67.541))
    wacc = WACC(symbols=symbolz)
    print('Result', wacc.value)