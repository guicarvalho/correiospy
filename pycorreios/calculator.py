# coding: utf-8

import urllib
import urllib2
import json

from config import NOT_SERVICE_VALUE, URL_WS_CORREIOS
from errors import InvalidServiceCodeError, InvalidZipCodeError, InvalidOrderFormatError
from format_order_codes import OrderFormats
from service_codes import ServiceCodes
from utils import VerifyZipCode


class CalcPriceDeadline(object):
    company_code = ''
    manager_password = ''
    declared_value = NOT_SERVICE_VALUE

    def __init__(self,
                 zip_code_sender,
                 zip_code_receiver,
                 order_weight,
                 order_format,
                 order_length,
                 order_height,
                 order_width,
                 order_diameter,
                 own_hand=NOT_SERVICE_VALUE,
                 declared_value=0,
                 receiving_notice=NOT_SERVICE_VALUE,
                 service_code=None
                 ):

        verify_zip_code = VerifyZipCode()
        try:
            verify_zip_code.is_valid_zip_code(zip_code_receiver, zip_code_sender)
        except InvalidZipCodeError as error:
            raise error

        self.zip_code_receiver = zip_code_receiver
        self.zip_code_sender = zip_code_sender

        self.order_weight = order_weight

        order_formats = OrderFormats(order_format)
        try:
            self.order_format = order_formats.get_order_format()[0]
        except InvalidOrderFormatError as error:
            raise error

        if not order_length:
            raise ValueError("The order length can't be null.")
        self.order_length = order_length

        if not order_height:
            raise ValueError("The order height can't be null.")
        self.order_height = order_height

        if not order_width:
            raise ValueError("The order width can't be null.")
        self.order_width = order_width

        if not order_diameter:
            raise ValueError("The order diameter can't be null.")
        self.order_diameter = order_diameter

        self.own_hand = own_hand

        self.declared_value = declared_value

        self.receiving_notice = receiving_notice

        service_codes = ServiceCodes()
        is_valid_service_code = service_codes.is_value_service_code(service_code)

        if not is_valid_service_code:
            raise InvalidServiceCodeError('Invalid service code, enter a valid service code.')
        self.service_code = service_code

    def calculate(self, format='json'):
        if format == 'plain/text':
            return self._get_as_plain_text()
        elif format == 'json':
            return self._get_as_json()

    def _get_as_plain_text(self):
        content = self._return_values()

        plain_text = u'{0:<25} => {1}\n'.format(u'Código', content['code'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Valor', content['value'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Prazo de entrega', content['deadline'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Valor mão propria', content['own_hand'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Valor aviso recebimento', content['receiving_notice'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Valor declarado', content['declared_value'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Entrega domiciliar', content['home_delivery'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Entrega sábado', content['saturday_delivery'])
        plain_text += u'{0:<25} => {1}\n'.format(u'Valor sem adicionais', content['additional_valueless'])

        return plain_text

    def _get_as_json(self):
        content = self._return_values()
        content = json.dumps(content)

        return content

    def _get(self):
        values = {
            'nCdEmpresa': self.company_code,
            'sDsSenha': self.manager_password,
            'nCdServico': self.service_code,
            'sCepOrigem': self.zip_code_sender,
            'sCepDestino': self.zip_code_receiver,
            'nVlPeso': self.order_weight,
            'nCdFormato': self.order_format,
            'nVlComprimento': self.order_length,
            'nVlAltura': self.order_height,
            'nVlLargura': self.order_width,
            'nVlDiametro': self.order_diameter,
            'sCdMaoPropria': self.own_hand,
            'nVlValorDeclarado': self.declared_value,
            'sCdAvisoRecebimento': self.receiving_notice
        }

        data = urllib.urlencode(values)
        req = urllib2.Request('{}/{}'.format(URL_WS_CORREIOS, 'CalcPrecoPrazo'), data)
        response = urllib2.urlopen(req)

        return response.read()

    def _return_values(self):
        content = self._get()

        ini, end = content.find('<Codigo>') + len('<Codigo>'), content.find('</Codigo>')
        code = content[ini:end]

        ini, end = content.find('<Valor>') + len('<Valor>'), content.find('</Valor>')
        value = content[ini:end]

        ini, end = content.find('<PrazoEntrega>') + len('<PrazoEntrega>'), content.find('</PrazoEntrega>')
        deadline = content[ini:end]

        ini, end = content.find('<ValorMaoPropria>') + len('<ValorMaoPropria>'), content.find('</ValorMaoPropria>')
        own_hand = content[ini:end]

        ini, end = content.find('<ValorAvisoRecebimento>') + len('<ValorAvisoRecebimento>'), content.find('</ValorAvisoRecebimento>')
        receiving_notice = content[ini:end]

        ini, end = content.find('<ValorValorDeclarado>') + len('<ValorValorDeclarado>'), content.find('</ValorValorDeclarado>')
        declared_value = content[ini:end]

        ini, end = content.find('<EntregaDomiciliar>') + len('<EntregaDomiciliar>'), content.find('</EntregaDomiciliar>')
        home_delivery = content[ini:end]

        ini, end = content.find('<EntregaSabado>') + len('<EntregaSabado>'), content.find('</EntregaSabado>')
        saturday_delivery = content[ini:end]

        ini, end = content.find('<ValorSemAdicionais>') + len('<ValorSemAdicionais>'), content.find('</ValorSemAdicionais>')
        additional_valueless = content[ini:end]

        return {'code': code,
                'value': value,
                'deadline': deadline,
                'own_hand': own_hand,
                'receiving_notice': receiving_notice,
                'declared_value': declared_value,
                'home_delivery': home_delivery,
                'saturday_delivery': saturday_delivery,
                'additional_valueless': additional_valueless
                }
