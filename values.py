'''
The content of this module enables us to work 
with values with units.
'''

class Value:
    '''
        Class to represent a simple value with a unit or currency.
    '''
    
    def __init__(self, value, unit=None):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f'{self.value} {self.unit}'

    def __eq__(self, value):
        return self.__dict__ == value.__dict__

    def __add__(self, value):
        if None in [self.value, value.value]:
            new_value = None

        else:
            new_value = self.value + value.value

        if self.unit == value.unit:
            return Value(new_value, self.unit)
        
        elif None in [self.unit, value.unit]:
            return Value(None)
        
        else:
            raise TypeError(f'different units encountered: {[self.unit, value.unit]}')

    def __sub__(self, value):
        if None in [self.value, value.value]:
            new_value = None

        else:
            new_value = self.value - value.value

        if self.unit == value.unit:
            return Value(new_value, self.unit)
        
        elif None in [self.unit, value.unit]:
            return Value(None)
        
        else:
            raise TypeError(f'different units encountered: {[self.unit, value.unit]}')
        
    def __mul__(self, value):
        if None in [self.value, value.value]:
            new_value = None
            new_unit = None

        else:
            new_value = self.value * value.value

            if self.unit is None and value.unit is None:
                new_unit = None

            elif self.unit is None:
                new_unit = value.unit

            elif value.unit is None:
                new_unit = self.unit

            else:
                new_unit = f'{self.unit}*{value.unit}'

        return Value(new_value, new_unit)
    
    def __truediv__(self, value):
        if None in [self.value, value.value] or value.value == 0:
            new_value = None
            new_unit = None

        else:
            new_value = self.value / value.value

            if (self.unit is None and value.unit is None) or (self.unit == value.unit):
                new_unit = None

            elif self.unit is None:
                new_unit = f'1/{value.unit}'

            elif value.unit is None:
                new_unit = self.unit

            else:
                new_unit = self.unit + '/' + value.unit

        return Value(new_value, new_unit)
            

class ValueList:
    def __init__(self, values=[]):
        self.values = [value for value in values]

    def __repr__(self):
        return str(self.values)

    def __getitem__(self, index):
        return self.values[index]
    
    def __setitem__(self, index, value):
        if isinstance(value, Value):
            self.values[index] = value

        else:
            raise TypeError(f'can only append Value objects, not {type(value)} objects')
    
    def __eq__(self, value_list):
        return self.__dict__ == value_list.__dict__
    
    def __len__(self):
        return len(self.values)
    
    def append(self, value):
        if isinstance(value, Value):
            self.values.append(value)

        else:
            raise TypeError(f'can only append Value objects, not {type(value)} objects')
    
    def __add__(self, value_list):
        new_value_list = ValueList()

        for value_1, value_2 in zip(self.values, value_list.values):
                new_value_list.append(value_1 + value_2)

        return new_value_list
    
    def __sub__(self, value_list):
        new_value_list = ValueList()

        for value_1, value_2 in zip(self.values, value_list.values):
                new_value_list.append(value_1 - value_2)

        return new_value_list
    
    def __mul__(self, multiplier):
        if isinstance(multiplier, int) or isinstance(multiplier, float) or isinstance(multiplier, Value):
            return ValueList([value*multiplier for value in self.values])
        
        elif isinstance(multiplier, list) or isinstance(multiplier, ValueList):
            return ValueList([value*factor for value, factor in zip(self.values, multiplier)])
        
    def __truediv__(self, divisor):
        if isinstance(divisor, int) or isinstance(divisor, float) or isinstance(divisor, Value):
            return ValueList([value/divisor for value in self.values])
        
        elif isinstance(divisor, list) or isinstance(divisor, ValueList):
            return ValueList([value/factor for value, factor in zip(self.values, divisor)])


def get_unit(values):
    units = {value.unit for value in values}

    if None in units:
        units.remove(None)

    if len(units) == 0:
        return None
    
    elif len(units) == 1:
        return units.pop()

    else:
        raise TypeError(f'different units encountered: {units}')