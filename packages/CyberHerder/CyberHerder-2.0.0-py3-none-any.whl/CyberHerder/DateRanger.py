import datetime
from dataclasses import dataclass
from typing import NewType, Tuple


@dataclass
class Date:
    """Date Object.

    Args:
        day (int): day of month.
        month (int): month of year.
        year (int): 4 digit year.
    """
    day: int
    month: int
    year: int

    def __str__(self) -> str:
        return self.datetimeFormat()

    def __int__(self):
        return self.day + (self.month + 1) * 100 + (self.year + 1) * 1000

    def pad(self, integer: int, padding=2):
        string = str(integer)
        while len(string) < padding:
            string = "0" + string
        return string

    def datetimeFormat(self) -> str:
        year = self.pad(self.year, padding=4)
        month = self.pad(self.month)
        day = self.pad(self.day)
        return f"{day}-{month}-{year}"


class DateRangeGenerator:
    """Date Iterable.

    Examples:
        >>> [str(date) for date in DateRangeGenerator(15, 1, 2022, count = 78, forward = False)][0]
        '15-01-2022'

    Args:
        day (int): starting day.
        month (int): starting month.
        year (int): starting year.
        count (int): amount of dates generated.
        forward (bool): dates going forward versus backwards.

    Returns:
        Iterable: Each object returned is of Date type.
    """
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    def __init__(
        self, day: int, month: int, year: int, count: int = 10, forward: bool = True
    ):
        if month > 12 or month < 1:
            raise Exception("There are only twelve months")
        if day > self.days[month - 1] or day < 1:
            raise Exception(
                f"The maximum days for {self.months[month]} are {self.days[month]}"
            )
        self.day = str(day)
        self.month = str(month)
        self.year = str(year)
        self.forward = forward
        self.count = count

    def __iter__(self):
        return self

    def __next__(self) -> Date:
        if self.count > 0:
            day = int(self.day)
            month = int(self.month)
            year = int(self.year)
            date = Date(day, month, year)
            if self.forward:
                self.day, self.month, self.year = self.generateNextDay(day, month, year)
            else:
                self.day, self.month, self.year = self.generatePrevDay(day, month, year)
            self.count -= 1
            return date
        else:
            raise StopIteration()

    def pad(self, integer: int) -> str:
        res = str(integer)

        while len(res) < 2:
            res = "0" + res

        return res

    def generateNextDay(self, day: int, month: int, year: int) -> Tuple[str, str, str]:
        if (day + 1) > self.days[month - 1]:
            month = (month + 1) % 13
            if month == 0:
                year += 1
                month = 1
            day = 1
        else:
            day += 1

        day_f = self.pad(day)
        month_f = self.pad(month)
        year_f = self.pad(year)
        return day_f, month_f, year_f

    def generatePrevDay(self, day: int, month: int, year: int) -> Tuple[str, str, str]:
        if (day - 1) < 1:
            month = (month - 1) % 13
            if month == 0:
                year -= 1
                month = 12
            day = self.days[month - 1]
        else:
            day -= 1

        day_f = self.pad(day)
        month_f = self.pad(month)
        year_f = self.pad(year)
        return day_f, month_f, year_f
