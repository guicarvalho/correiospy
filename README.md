# correiospy
Calculates the amount of supplies through zip code. The values are found at WS the Correios in Brazil.

# Installation

You can to install using pip:

```sh
pip install correiospy
```

Or through of source code with:

```sh
git clone https://github.com/guicarvalho/correiospy.git
cd correiospy
python setup.py install
```

For to verify success of installation run this command in shell:

```sh
python -c "import correiospy; print correiospy.VERSION"
[some version of code here]
```

# Use mode:

You can calculate the freight and delivery time informing only one service code or many. For to calculate with one, see below:

```python
# coding: utf-8

from correiospy.calculator import CalcPriceDeadline
from correiospy.format_order_codes import OrderFormats
from correiospy.service_codes import ServiceCodes


values = {'zip_code_sender': '14808400',
          'zip_code_receiver': '14805362',
          'order_weight': 0.100,
          'order_format': OrderFormats.BOX_PACKAGE_FORMAT,
          'order_length': 27,
          'order_height': 27,
          'order_width': 27,
          'order_diameter': 27,
          'declared_value': 0,
          'service_code': ServiceCodes.SEDEX_VAREJO_CODE
          }

calc = CalcPriceDeadline(**values)

content_json = calc.calculate()

print content_json
```

And for to calculate with many service code:

```python
# coding: utf-8

from correiospy.calculator import CalcPriceDeadline
from correiospy.format_order_codes import OrderFormats
from correiospy.service_codes import ServiceCodes


values = {'zip_code_sender': '14808400',
          'zip_code_receiver': '14805362',
          'order_weight': '0.100',
          'order_format': OrderFormats.BOX_PACKAGE_FORMAT,
          'order_length': '27',
          'order_height': '27',
          'order_width': '27',
          'order_diameter': '27',
          'declared_value': '0',
          'service_code': [ServiceCodes.SEDEX_VAREJO_CODE, ServiceCodes.SEDEX_10_VAREJO_CODE]
          }

calc = CalcPriceDeadline(**values)

content_json = calc.calculate()

print content_json
```

The response is a JSON object, and must look like this:

```json
// one service code

{"40010": {"own_hand": "0,00", "receiving_notice": "0,00", "code": "40010", "deadline": "1", "declared_value": "0,00", "saturday_delivery": "S", "additional_valueless": "14,00", "home_delivery": "S", "value": "14,00"}}

// many service code

{"40045": {"own_hand": "0,00", "receiving_notice": "0,00", "code": "40045", "deadline": "0", "declared_value": "0,00", "saturday_delivery": null, "additional_valueless": "0,00", "home_delivery": null, "value": "0,00"}, "40215": {"own_hand": "0,00", "receiving_notice": "0,00", "code": "40215", "deadline": "1", "declared_value": "0,00", "saturday_delivery": "S", "additional_valueless": "22,60", "home_delivery": "S", "value": "22,60"}, "40010": {"own_hand": "0,00", "receiving_notice": "0,00", "code": "40010", "deadline": "1", "declared_value": "0,00", "saturday_delivery": "S", "additional_valueless": "14,00", "home_delivery": "S", "value": "14,00"}, "40290": {"own_hand": "0,00", "receiving_notice": "0,00", "code": "40290", "deadline": "0", "declared_value": "0,00", "saturday_delivery": null, "additional_valueless": "0", "home_delivery": null, "value": "0"}, "41106": {"own_hand": "0,00", "receiving_notice": "0,00", "code": "41106", "deadline": "3", "declared_value": "0,00", "saturday_delivery": "N", "additional_valueless": "13,70", "home_delivery": "S", "value": "13,70"}}
```

This package is under development.
