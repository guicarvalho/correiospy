# coding: utf-8

import urllib2
import json

from config import URL_POSTMON
from errors import InvalidZipCodeError
from utils import VerifyZipCode


class FinderZipCode(object):

    def find_addess(self, *zip_code_list):

        verify = VerifyZipCode()

        dict_return = {}

        try:
            verify.is_valid_zip_code(zip_code_list)
        except InvalidZipCodeError as error:
            raise error

        for zip_code in zip_code_list:
            url = '{0}{1}'.format(URL_POSTMON, zip_code)
            response_str = urllib2.urlopen(url).read()
            dict_return[zip_code] = json.loads(response_str)

        return json.dumps(dict_return)
