# pycorreios
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
```

# Use mode:

You can calculate informing only one service code or many. For to calculate with one, see below:

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
content_plain_text = calc.calculate('plain/text')

print u'Retorno em JSON:\n{0}\nRetorno em texto:\n{1}\n'.format(content_json, content_plain_text)
```
