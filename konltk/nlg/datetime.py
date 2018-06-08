# -*- coding: utf-8 -*-

from datetime import datetime

from konltk.nlg.exceptions import DateTimeOffsetNaiveException, UndefinedSituationException

import pytz


"""
A DateTimeExprGenerator is a tool to make time expressions in Korean from the given datetime considering
the reference time. It's a simple rule-based generator but useful in many cases.

It's based on following heuristics:
 * People omit year and month information if the date is close to today.
 * People frequently use relative time expressions.

This generator does not cover all possibilities. Check the following examples first to check if it's
suitable for your purpose.

```
from konltk.nlg.datetime import DateTimeExprGenerator
import pytz

tz = pytz.timezone('Asia/Seoul')
generator = DateTimeExprGenerator()

dt_base = tz.localize(datetime(2018, 6, 6, 15))         # 2018-06-06T15:00:00+09:00

dt = tz.localize(datetime(2018, 6, 6, 8))               # 2018-06-06T08:00:00+09:00
expr = dt_expr_generator.generate(dt, dt_base=dt_base)  # If dt_base=None, current time is used.
print(expr)                                             # "오늘 오전 8시"

dt_end = tz.localize(datetime(2018, 6, 6, 10))                  # 2018-06-06T08:00:00+09:00
expr = dt_expr_generator.generate(dt, dt_end, dt_base=dt_base)  # If dt_base=None, current time is used.
print(expr)                                                     # "오늘 오전 8시부터 10시"
```

More examples with the reference datetime(2018, 6, 6, 15):

datetime(2018, 6, 4, 10)            # "이번주 월요일(4일) 오전 10시"
datetime(2018, 6, 5, 18)            # "어제(5일) 오후 6시"
datetime(2018, 6, 7, 22, 10)        # "내일 오후 10시 10분"
datetime(2018, 6, 8, 23)            # "모레(8일) 오후 11시"
datetime(2018, 6, 9, 12)            # "토요일(9일) 오후 12시"
datetime(2018, 6, 11, 12)           # "다음주 월요일(11일) 오후 12시"
datetime(2018, 6, 1)                # "지난주 금요일(1일) 오전 12시"
datetime(2018, 5, 30, 8, 21)        # "2018년 5월 30일 수요일, 오전 8시 21분"
datetime(2018, 4, 1, 11)            # "2018년 4월 1일 일요일, 오전 11시"
datetime(2018, 7, 21, 15, 10, 30)   # "7월 21일 토요일, 오후 3시 10분 30초"
datetime(2018, 8, 4, 16, 0, 0)      # "8월 4일 토요일, 오후 4시"
datetime(2019, 1, 21, 15, 0, 10)    # "2019년 1월 21일 월요일, 오후 3시 0분 10초"
datetime(2019, 2, 4, 16)            # "2019년 2월 4일 월요일, 오후 4시"

"""


SCHEDULING_DIALOG = 0
SUMMING_UP = 1

class DateTimeExprGenerator(object):
    """
        A simple rule based time expression generator.
    """

    def __init__(self, timezone="Asia/Seoul"):
        self.tz = pytz.timezone(timezone)

    def generate(self, dt, dt_end=None, dt_base=None, situation=SCHEDULING_DIALOG):
        """
        Generate a date time expression in Korean.

        :param dt: A datetime to generate an expression
        :type dt: datetime.datetime

        :param dt_end: A datetime to generate a time range expression
        :type dt_end: datetime.datetime

        :param dt_base: A reference datetime. If none, `datetime.now()` is used.
        :type dt: datetime.datetime
        """
        assert isinstance(dt, datetime), "`dt` should be a `datetime.datetime` instance"
        
        if dt_base:
            if dt_base.tzinfo is None:
                raise DateTimeOffsetNaiveException("`dt_base` has no tzinfo. All datetime objects should be offset-aware.")
            dt_base = dt_base.astimezone(self.tz)
        else:
            dt_base = datetime.now(tz=pytz.UTC).astimezone(self.tz)

        if dt.tzinfo is None:
            raise DateTimeOffsetNaiveException("`dt` has no tzinfo. All datetime objects should be offset-aware.")
        dt = dt.astimezone(self.tz)

        if dt_end:
            if dt_end.tzinfo is None:
                raise DateTimeOffsetNaiveException("`dt_end` has no tzinfo. All datetime objects should be offset-aware.")
            dt_end = dt_end.astimezone(self.tz)

        if situation == SCHEDULING_DIALOG:
            dt_expr = "{} {}".format(self.__str_date_for_scheduling_dialog(dt=dt, dt_base=dt_base),
                    self.__str_time_for_scheduling_dialog(dt=dt)).strip()
            if dt_end:
                dt_end_expr = "{} {}".format(self.__str_date_for_scheduling_dialog(dt=dt_end, dt_base=dt_base, dt_ref=dt),
                        self.__str_time_for_scheduling_dialog(dt=dt_end, dt_ref=dt)).strip()
                return "{}부터 {}".format(dt_expr, dt_end_expr)
            else:
                return dt_expr
        elif situation == SUMMING_UP:
            dt_expr = self.__str_datetime_for_summing_up(dt=dt, dt_base=dt_base)
            if dt_end:
                dt_end_expr = self.__str_datetime_for_summing_up(dt=dt_end, dt_base=dt_base, dt_ref=dt)
                return "{} ~ {}".format(dt_expr, dt_end_expr)
            else:
                return dt_expr
        else:
            raise UndefinedSituationException("Invalid situation provided.")


    def __str_date_for_scheduling_dialog(self, dt, dt_base, dt_ref=None):
        """
        Generate date expression for a schedule dialog.
        """
        dt_comp = dt_base if dt_ref is None else dt_ref
        if dt.year != dt_comp.year or dt.month < dt_comp.month:
            return "{}년 {}월 {}일 {},".format(dt.year, dt.month, dt.day, self.weekday(dt))
        elif dt.month != dt_comp.month:
            return "{}월 {}일 {},".format(dt.month, dt.day, self.weekday(dt))

        expr = []

        if dt_ref is None or (dt_ref.day != dt.day):
            day_diff = dt.day - dt_base.day
            if day_diff == 0:
                expr.append("오늘")
            elif day_diff == 1:
                expr.append("내일")
            elif day_diff == -1:
                expr.append("어제")
            elif day_diff == 2:
                expr.append("모레")
            else:
                if dt_ref is None or (dt_ref.isocalendar()[1] != dt.isocalendar()[1]):
                    week_diff = dt.isocalendar()[1] - dt_base.isocalendar()[1]
                    if week_diff not in (-1, 0, 1):
                        expr.append("{}일 {}".format(dt.day, self.weekday(dt)))
                    else:
                        if week_diff == 0:
                            if day_diff < 0:
                                expr.append("이번주")
                        elif week_diff == 1:
                            expr.append("다음주")
                        elif week_diff == -1:
                            expr.append("지난주")
                        expr.append(self.weekday(dt))
                else:
                    expr.append("{}일 {}".format(dt.day, self.weekday(dt)))

        return " ".join(expr)


    def __str_time_for_scheduling_dialog(self, dt, dt_ref=None):
        """
        Generate time expression for a schedule dialog.
        """
        expr = []

        if dt_ref is None or dt.year != dt_ref.year or dt.month != dt_ref.month or dt.day != dt_ref.day or \
            (dt.hour < 12 and dt_ref.hour >= 12) or (dt.hour >= 12 and dt_ref.hour < 12):
            if dt.hour < 12:
                expr.append("오전")
            else:
                expr.append("오후")

        if dt.hour == 0:
            expr.append("12시")
        elif dt.hour < 13:
            expr.append("{}시".format(dt.hour))
        else:
            expr.append("{}시".format(dt.hour - 12))

        if dt.minute > 0 or dt.second > 0:
            expr.append("{}분".format(dt.minute))
        if dt.second > 0:
            expr.append("{}초".format(dt.second))

        return " ".join(expr)


    def __str_datetime_for_summing_up(self, dt, dt_base, dt_ref=None):
        """
        Generate date expression for a schedule summary.
        """
        expr = []
        dt_comp = dt_base if dt_ref is None else dt_ref

        if dt.year != dt_comp.year or dt.month < dt_comp.month:
            expr.append("{}/{}/{}({})".format(dt.year, dt.month, dt.day, self.weekday(dt, simple=True)))
        elif dt_ref is None or dt.month != dt_ref.month:
            expr.append("{}/{}({})".format(dt.month, dt.day, self.weekday(dt, simple=True)))
        elif dt_ref is None or dt.day != dt_comp.day:
            expr.append("{}({})".format(dt.day, self.weekday(dt, simple=True)))

        expr.append("{:02}:{:02}".format(dt.hour, dt.minute))

        return " ".join(expr)


    def weekday(self, dt, simple=False):
        """
        Return weekday in Korean.

        :param simple: Simple version (월, 화, 수) or full version (월요일, 화요일, 수요일)
        :type simple: bool
        """
        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        if simple:
            return weekdays[dt.weekday()][0]
        else:
            return weekdays[dt.weekday()]

