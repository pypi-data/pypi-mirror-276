# color_mapper

A package for normalizing values and mapping them to a color gradient.

## Installation

```bash
pip install color_mapper
```

### Usage

```bash

from color_mapper import value_to_color

values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
color_bases = ['blue', 'yellow', 'red']
color_mapped_values = value_to_color(values, color_bases)
for item in color_mapped_values:
    print(f"Value: {item['value']}, Color: {item['color']}")
```