from typing import Final, NoReturn, Tuple, List, Any, Union, TypeAlias
from random import uniform
from copy import deepcopy

import numpy as np

Str: TypeAlias = str
Number: TypeAlias = int | float

Unit: TypeAlias = Tuple[str, float]
Units: TypeAlias = List[Unit]
Order: TypeAlias = Tuple[Unit, float]

class Delicacy:
    def __init__(self, name: Str, price: Number, weight: Number) -> None:
        self.name: Final = name
        self.__price = price
        self.weight: Final = weight
    
    # Changes instance price
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: Number) -> NoReturn:
        if new_price < 0:
            raise Exception(f'Cant give money and product for free: {sale_percent}')

        self.__price *= new_price / 100

    def __str__(self) -> Str:
        return f'{self.name} weighs {self.weight} and sells for {self.__price}'

### Discount Strategies: make_sale_item and christmas_sale
#### Would need to modify shop to implement this for the client
def make_sale_item(item: Delicacy, price_percent: Number) -> Delicacy:
    if price_percent < 0:
        raise Exception(f'Cant give money and product for free: {sale_percent}')

    copied_item = deepcopy(item)
    copied_item.price = price_percent
    return copied_item

def christmas_sale(item: Delicacy) -> Delicacy:
    price_percent: float = 0.50
    if price_percent < 0:
        raise Exception(f'Cant give money and product for free: {sale_percent}')

    copied_item = deepcopy(item)
    copied_item.price = price_percent
    return copied_item

class Shop:
    units_processed = 0
    weight_processed = 0

    # Not needed if not defining
    def __init__(self) -> None:
        pass

    def get_unit(self, item: Delicacy, price_percent: Number) -> Unit:
        # packaging weight
        return make_sale_item(item, price_percent), uniform(item.weight + 0.2, item.weight + 0.5)

    def commit_unit(self, unit: Unit) -> NoReturn:
        self.weight_processed += unit[1]
        self.units_processed += 1

    # Type may be different
    # Should be hidden from client
    def get_units(self, item: Delicacy, number: Number, price_percent: Number) -> Units:
        # Not bounds defined... Ranges here... get with it Python community
        return [self.get_unit(item, price_percent) for unit in range(number)]

    def get_1000_units(self, item: Delicacy, weight_limit: Number = 1_000_000, price_percent: Number = 100) -> Order: #Tuple[Units, T]:
        print('New order coming in!')

        count = 100
        
        while (count := count - 1):
            units = self.get_units(item, 1000, price_percent) 
            
            if (total_weight := sum([unit[0].weight for unit in units])) <= weight_limit:
                for unit in units:
                    self.commit_unit(unit)

                print(self.__str__())

                return units, total_weight

        raise Exception(f'Could not meet your requirement')

    def __str__(self) -> Str:
        return f'Total units processed: {self.units_processed}\nTotal weight_processed: {self.weight_processed}'
        
def simulate_sampling(obj_series, sample_amount, trials, replacement: bool = False, transformer: str = 'mean'):
    res = []
    
    for i in range(trials):
        tmp = obj_series.sample(sample_amount, replace=replacement)
        
        match transformer:
            case 'mean':
                res.append(np.mean(tmp))
            case 'std':
                res.append(np.std(tmp))
            case _:
                res.append(tmp)
                
    return res
        
if __name__ == "__main__":
    shop1 = Shop()

    candies = (('Chocolate Bar', 4, 1), ('Gumdrops', 3, 0.3), ('Gobstopper', 5, 3))

    delicacies = [Delicacy(*item) for item in candies]

    try:
        new_order = shop1.get_1000_units(delicacies[0], price_percent=80)
        print()
        print(f'Original price of first item: {delicacies[0].price}')
        print(f'New price of first item: {new_order[0][0][0].price}')
    except:
        print(f'Couldnt fulfill order!')
