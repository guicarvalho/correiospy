# coding: utf-8

from errors import InvalidOrderFormatError


class OrderFormats(object):

    BOX_PACKAGE_FORMAT = 1
    ROLL_PRISM_FORMAT = 2
    ENVELOPE_FORMAT = 3

    def __init__(self, number):
        self.formats = {
            self.BOX_PACKAGE_FORMAT: 'Box/Package format',
            self.ROLL_PRISM_FORMAT: 'Roll/Prism format',
            self.ENVELOPE_FORMAT: 'Envelope format'
        }

        self.number = number

    def get_order_format(self):
        format_order_value = self.formats.get(int(self.number))

        if not format_order_value:
            raise InvalidOrderFormatError('Not exists a order format with this number.')

        return (self.number, format_order_value)
