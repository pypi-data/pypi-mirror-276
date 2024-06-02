import re

from sanatio.utils.utils import all_country, regexs
from sanatio.utils.checksum import checksum_aadhar, checksum_credit_card


class DocumentValidator:
    def __init__(self) -> None:
        pass

    def isAadharCard(self, value)-> bool:
        """ check if the string is Aadhar card or not """
        regex = "^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$"  # need to improve regex for space and hyphen
        value = value.strip().replace(" ", "")
        if self.isLength(value, 12, 12):
            if isinstance(value, int):
                value = str(value)

            if value[0] != '0' or value[0] != '1':
                if re.match(regex, value):
                    if checksum_aadhar(value):
                        return True

    def isLicensePlate(self, value, locale: str) -> bool:
        """ check if the string is license plate or not """
        value = value.upper()
        country_data = all_country[locale]

        LicensePlate = country_data['LicensePlate']
        Format = LicensePlate['Format']
        Regex = LicensePlate['Regex']
        MinLength = LicensePlate['MinLength']
        MaxLength = LicensePlate['MaxLength']


        if re.match(Format, value) and re.match(Regex, value) \
            and self.isLength(value, MinLength, MaxLength):
                return True

        return False

    def isPassportNumber(self, value, locale: str)-> bool:  # TODO: research more about passport number
        """ check if the string is passport number or not """
        country_data = all_country[locale]

        PassportNumberRegex = country_data['PassportNumberRegex']
        if re.match(PassportNumberRegex, value):
            return True
        return False

    def isCreditCard(self, value: str) -> bool:  # checksum not implemented
        regex = regexs['credit_card_regex']
        if re.match(regex, value):
            if checksum_credit_card(value):
                return True
        return False
