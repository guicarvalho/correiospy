# coding: utf-8

from errors import InvalidZipCodeError
import re


class VerifyZipCode(object):

    def is_valid_zip_code(self, *zip_code_list):
        match = re.compile('\d{8}$')

        if type(zip_code_list[0]) is list or type(zip_code_list[0]) is tuple:
            zip_code_list = zip_code_list[0]

        try:
            for zip_code in zip_code_list:
                match.match(str(zip_code)).group(0)
        except Exception:
            raise InvalidZipCodeError("{} ins't valid zip code.".format(zip_code))
