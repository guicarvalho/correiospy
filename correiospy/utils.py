# coding: utf-8

from errors import InvalidZipCodeError
import re


class VerifyZipCode(object):

    def is_valid_zip_code(self, *zip_code_list):
        match = re.compile('\d{8}$')

        try:
            for zip_code in zip_code_list:
                match.match(zip_code).group(0)
        except Exception:
            raise InvalidZipCodeError("{} ins't valid zip code.".format(zip_code))
