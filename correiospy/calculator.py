# coding: utf-8

import urllib
import urllib2
import json
import xml.etree.ElementTree as ET

from config import NOT_SERVICE_VALUE, URL_WS_CORREIOS, URI_NAMESPACE
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
                 declared_value='0',
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

        self.order_weight = str(order_weight)

        order_formats = OrderFormats(order_format)
        try:
            self.order_format = order_formats.get_order_format()[0]
        except InvalidOrderFormatError as error:
            raise error

        if not order_length:
            raise ValueError("The order length can't be null.")
        self.order_length = str(order_length)

        if not order_height:
            raise ValueError("The order height can't be null.")
        self.order_height = str(order_height)

        if not order_width:
            raise ValueError("The order width can't be null.")
        self.order_width = str(order_width)

        if not order_diameter:
            raise ValueError("The order diameter can't be null.")
        self.order_diameter = str(order_diameter)

        self.own_hand = own_hand

        self.declared_value = str(declared_value)

        self.receiving_notice = receiving_notice

        service_codes = ServiceCodes()
        try:
            self.service_code = service_codes.is_value_service_code(service_code)
        except InvalidServiceCodeError as error:
            raise error

    def calculate(self):
        return self._get_as_json()

    def _get_as_json(self):
        content = self._return_values()
        return json.dumps(content)

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

        return ET.fromstring(response.read())

    def _return_values(self):
        content = self._get()

        elem_services = content.getchildren()[0]
        cservice_list = elem_services.findall(ET.QName(URI_NAMESPACE, 'cServico').text)

        dict_return = {}

        for c_service in cservice_list:
            code = c_service.find(ET.QName(URI_NAMESPACE, 'Codigo').text).text
            dict_return[code] = {
                'code': code,
                'value': c_service.find(ET.QName(URI_NAMESPACE, 'Valor').text).text,
                'deadline': c_service.find(ET.QName(URI_NAMESPACE, 'PrazoEntrega').text).text,
                'own_hand': c_service.find(ET.QName(URI_NAMESPACE, 'ValorMaoPropria').text).text,
                'receiving_notice': c_service.find(ET.QName(URI_NAMESPACE, 'ValorAvisoRecebimento').text).text,
                'declared_value': c_service.find(ET.QName(URI_NAMESPACE, 'ValorValorDeclarado').text).text,
                'home_delivery': c_service.find(ET.QName(URI_NAMESPACE, 'EntregaDomiciliar').text).text,
                'saturday_delivery': c_service.find(ET.QName(URI_NAMESPACE, 'EntregaSabado').text).text,
                'additional_valueless': c_service.find(ET.QName(URI_NAMESPACE, 'ValorSemAdicionais').text).text
            }
        return dict_return
