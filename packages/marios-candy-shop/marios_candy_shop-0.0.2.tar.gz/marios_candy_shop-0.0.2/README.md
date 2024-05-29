# Mario's Candy Shop
[![Test Coverage](https://img.shields.io/badge/Test%20Coverage-100%25-success)](https://github.com/jacob-h-barrow/SiemChirps)
[![Security](https://img.shields.io/badge/Secure-True-informational)](https://github.com/jacob-h-barrow/SiemChirps)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2020%2B-critical)](https://github.com/jacob-h-barrow/SiemChirps)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-critical)](https://github.com/jacob-h-barrow/SiemChirps)
[![MIT License](https://img.shields.io/badge/License-MIT-lightgrey)](https://github.com/jacob-h-barrow/SiemChirps)

- Created By Jacob H Barrow

## Why Was It Created
- Data is gold, so learning cybersecurity can be tricky without simulated testbeds.
- Use this package to test supply chain fundamentals.


## Usage
``` python
>>> from marios_candy_shop import Shop, simulate_sampling
>>>
>>> shop1 = Shop()
>>>
>>> candies = (('Chocolate Bar', 4, 1), ('Gumdrops', 3, 0.3), ('Gobstopper', 5, 3))
>>>
>>> delicacies = [Delicacy(*item) for item in candies]
>>>
>>> try:
>>>     new_order = shop1.get_1000_units(delicacies[0], price_percent=80)
>>>     print()
>>>     print(f'Original price of first item: {delicacies[0].price}')
>>>     print(f'New price of first item: {new_order[0][0][0].price}')
>>> except:
>>>    print(f'Couldnt fulfill order!')
```
