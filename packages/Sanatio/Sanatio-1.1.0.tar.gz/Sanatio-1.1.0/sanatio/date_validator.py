from datetime import datetime
from dateutil.parser import parse
from dateutil.parser import parse


class DateValidator:
    def __init__(self) -> None:
        pass

    def isLeapYear(self, year) -> bool:
        """ check if the year is leap year or not """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def isAfter(self, date1, date2=datetime.now()) -> bool:
        """ check if date1 is after date2 default date2 is current date

        Args:
            date1 (str): date in string format
            date2 (str): date in string format default is current date

        """
        if isinstance(date1, str):
            date1 = datetime.strptime(date1, '%Y-%m-%d')
        if isinstance(date2, str):
            date2 = datetime.strptime(date2, '%Y-%m-%d')

        return date1 > date2

    def isBefore(self, date1, date2=datetime.now()) -> bool:
        """
        check if date1 is before date2 default date2 is current date

        Args:
            date1 (str): date in string format
            date2 (str): date in string format default is current date
        """
        if isinstance(date1, str):
            date1 = datetime.strptime(date1, '%Y-%m-%d')
        if isinstance(date2, str):
            date2 = datetime.strptime(date2, '%Y-%m-%d')

        return date1 < date2

    def isDate(self, value) -> bool:
        """ check if the string is date or not """
        if not self.isvalidString(value):
            return False
        try:
            date_obj = parse(value)
            if date_obj:
                return True
        except Exception:
            return False
        return False

    def toDate(self, value, format='%Y-%m-%d'):  # need to improve this function
        """ convert string to date """
        if self.isDate(value):
            date = datetime.strptime(value, format)
            return date
        else:
            return None
