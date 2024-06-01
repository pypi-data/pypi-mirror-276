#! /usr/bin/env python
"""
Description:
    Programm zur Ausgabe einer Ansicht eines Monats wie gängige Kalender-Format

Usage:

```
$ python month_of_year.py 12 2024
```
"""
from typing import Final
import sys


# Calender setup
weekdays: Final[tuple[str, ...]] = ("So", "Mo", "Di", "Mi", "Do", "Fr", "Sa")
first_day_of_week: Final[int] = 1  # it is monday, common in Europa
months: Final[tuple[ tuple[str, int], ...]] = (("", 0),
                                             ("Januar", 31), ("Februar", 28), ("März", 31),
                                             ("April", 30), ("Mai", 31), ("Juni", 30),
                                             ("July", 31), ("August", 31), ("September", 30),
                                             ("Oktober", 31), ("November", 30), ("Dezember", 31))


def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def weekday_of_date(day: int, month: int, year: int) -> int:
    y0 = year - ((14 - month) // 12)
    x = y0 + (y0 // 4) - (y0 // 100) + (y0 // 400)
    m0 = month + 12 * ((14 - month) // 12) - 2
    return (day + x + (31 * m0) // 12) % 7


def count_days_in_month(month: int, year: int) -> int:
    count_days = months[month][1]
    if month == 2 and is_leap_year(year):
        count_days += 1
    return count_days


def build_calendar_head(month: int, year: int, calendar_width: int, fill_char: str =' ') -> str:
    head_line = f"{months[month][0]} {year}"
    return head_line.center(calendar_width, fill_char)


def build_weekdays_line(column_width) -> str:
    wd_line = ""
    for i in range(0, 7):
        d = (i + first_day_of_week) % 7
        wd_line += f"{weekdays[d]}".rjust(column_width, ' ')
    return wd_line


def format_day(day: int, column_width: int) -> str:
    return f"{day}".rjust(column_width)


def build_month_view(month: int, year: int, column_width: int) -> str:
    month_view = ""
    day = 1
    # the first week
    day_of_first_date = weekday_of_date(day, month, year)
    # how many columns before the first day of this month
    diff = (7 + day_of_first_date - first_day_of_week) % 7
    # -> empty column
    for _ in range(diff, 0, -1):
        month_view += ("-" + "#"*(column_width - 1) )
    # -> next days in the first week
    while day + diff <= 7:
        month_view += format_day(day, column_width)
        day += 1
    month_view += "\n"
    # next weeks
    days_in_month = count_days_in_month(month, year)
    while day <= days_in_month:
        month_view += format_day(day, column_width)
        if (day + diff) % 7 == 0 and (day < days_in_month):
            month_view += "\n"
        day += 1
    return month_view


def build_calendar(month: int, year: int, column_width: int = 3) -> str:
    calendar_width = 7 * column_width
    head_line = build_calendar_head(month, year, calendar_width, fill_char="-")
    calendar_view = f"{head_line}\n"
    weekdays_line = build_weekdays_line(column_width)
    calendar_view += f"{weekdays_line}\n"
    month_view = build_month_view(month, year, column_width)
    calendar_view += f"{month_view}"
    return calendar_view


if __name__ == "__main__":
    month = int(sys.argv[1])
    year = int(sys.argv[2])
    cal = build_calendar(month, year, 5)
    print(cal)