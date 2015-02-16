# coding: utf-8

from errors import InvalidServiceCodeError


class ServiceCodes(object):
    SEDEX_VAREJO_CODE = '40010'
    SEDEX_A_COBRAR_VAREJO_CODE = '40045'
    SEDEX_10_VAREJO_CODE = '40215'
    SEDEX_HOJE_VAREJO_CODE = '40290'
    PAC_VAREJO_CODE = '41106'

    def get_service_code_list(self):
        codes = [
            self.SEDEX_VAREJO_CODE,
            self.SEDEX_A_COBRAR_VAREJO_CODE,
            self.SEDEX_10_VAREJO_CODE,
            self.SEDEX_HOJE_VAREJO_CODE,
            self.PAC_VAREJO_CODE
        ]
        return codes

    def is_value_service_code(self, code_value_list):
        valid_code_value_list = [code for code in code_value_list if code in self.get_service_code_list()]

        if len(valid_code_value_list) != len(code_value_list):
            raise InvalidServiceCodeError('Invalid service code, enter a valid service code.')

        return ','.join(valid_code_value_list)
